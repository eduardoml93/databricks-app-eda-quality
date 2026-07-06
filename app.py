import os
from databricks import sql
from databricks.sdk.core import Config
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

# =========================
# Configuração Databricks
# =========================
assert os.getenv('DATABRICKS_WAREHOUSE_ID'), "DATABRICKS_WAREHOUSE_ID must be set in app.yaml."

def sqlQuery(query: str) -> pd.DataFrame:
    cfg = Config()
    with sql.connect(
        server_hostname=cfg.host,
        http_path=f"/sql/1.0/warehouses/{os.getenv('DATABRICKS_WAREHOUSE_ID')}",
        credentials_provider=lambda: cfg.authenticate
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall_arrow().to_pandas()

st.set_page_config(layout="wide")

# =========================
# INPUT DO USUÁRIO
# =========================
st.sidebar.title("⚙️ Configuração")

table_name = st.sidebar.text_input(
    "Tabela (catalog.schema.table)",
    value="workspace.default.titanic"
)

limit = st.sidebar.slider("Limite de linhas", 1000, 100000, 5000)

# =========================
# CACHE
# =========================
@st.cache_data(ttl=60)
def getData(table, limit):
    query = f"SELECT * FROM {table} LIMIT {limit}"
    return sqlQuery(query)

# =========================
# LOAD DATA
# =========================
try:
    data = getData(table_name, limit)
    st.success(f"Tabela carregada: {table_name}")
except Exception as e:
    st.error(f"Erro ao carregar tabela: {e}")
    st.stop()

# =========================
# HEADER
# =========================
st.title("🔍 Data Quality Analyzer")

# =========================
# KPIs GERAIS
# =========================
total_rows = len(data)
total_cols = len(data.columns)
missing_cells = data.isna().sum().sum()
duplicate_rows = data.duplicated().sum()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Rows", total_rows)
col2.metric("Columns", total_cols)
col3.metric("Missing Values", missing_cells)
col4.metric("Duplicate Rows", duplicate_rows)

# =========================
# INFO COLUNAS
# =========================
st.header("📋 Column Summary")

summary = pd.DataFrame({
    "column": data.columns,
    "dtype": data.dtypes.astype(str),
    "missing": data.isna().sum(),
    "missing_%": (data.isna().sum() / total_rows * 100).round(2),
    "unique": data.nunique()
})

st.dataframe(summary, use_container_width=True)

# =========================
# DISTRIBUIÇÃO DE NULOS
# =========================
st.header("🚫 Missing Values Distribution")

missing_df = summary[['column', 'missing']]

chart = alt.Chart(missing_df).mark_bar().encode(
    x='column:N',
    y='missing:Q'
)

st.altair_chart(chart, use_container_width=True)

# =========================
# TIPOS DE DADOS
# =========================
st.header("🧬 Data Types")

dtype_count = summary['dtype'].value_counts().reset_index()
dtype_count.columns = ['dtype', 'count']

chart = alt.Chart(dtype_count).mark_bar().encode(
    x='dtype:N',
    y='count:Q'
)

st.altair_chart(chart, use_container_width=True)

# =========================
# NUMÉRICOS
# =========================
numeric_cols = data.select_dtypes(include=np.number).columns

if len(numeric_cols) > 0:
    st.header("📊 Numeric Analysis")

    col = st.selectbox("Escolha coluna numérica", numeric_cols)

    col1, col2 = st.columns(2)

    with col1:
        hist = alt.Chart(data).mark_bar().encode(
            alt.X(col, bin=alt.Bin(maxbins=50)),
            y='count()'
        )
        st.altair_chart(hist, use_container_width=True)

    with col2:
        box = alt.Chart(data).mark_boxplot().encode(
            y=col
        )
        st.altair_chart(box, use_container_width=True)

    # Outliers
    q1 = data[col].quantile(0.25)
    q3 = data[col].quantile(0.75)
    iqr = q3 - q1

    outliers = data[(data[col] < q1 - 1.5 * iqr) | (data[col] > q3 + 1.5 * iqr)]

    st.write(f"⚠️ Outliers em {col}: {len(outliers)}")

# =========================
# CATEGÓRICOS
# =========================
cat_cols = data.select_dtypes(include='object').columns

if len(cat_cols) > 0:
    st.header("🏷️ Categorical Analysis")

    col = st.selectbox("Escolha coluna categórica", cat_cols)

    top_values = data[col].value_counts().head(20).reset_index()
    top_values.columns = [col, 'count']

    chart = alt.Chart(top_values).mark_bar().encode(
        x=f'{col}:N',
        y='count:Q'
    )

    st.altair_chart(chart, use_container_width=True)

# =========================
# CORRELAÇÃO
# =========================
if len(numeric_cols) > 1:
    st.header("🧠 Correlation Matrix")

    corr = data[numeric_cols].corr()
    st.dataframe(corr, use_container_width=True)

# =========================
# DUPLICADOS
# =========================
st.header("🔁 Duplicate Rows")

if duplicate_rows > 0:
    st.write(f"Encontrados {duplicate_rows} registros duplicados")
    st.dataframe(data[data.duplicated()].head(20))
else:
    st.write("Nenhum duplicado encontrado ✅")

# =========================
# DATA PREVIEW
# =========================
st.header("📄 Data Preview")
st.dataframe(data.head(100), use_container_width=True)