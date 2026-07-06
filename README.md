# 🔍 Data Quality Analyzer

Aplicação desenvolvida com **Streamlit** para análise rápida da qualidade de dados armazenados no **Databricks Unity Catalog**.

O objetivo é permitir que analistas e engenheiros de dados explorem tabelas, identifiquem problemas de qualidade e obtenham métricas básicas sem precisar escrever consultas SQL manualmente.

---

## 🚀 Funcionalidades

- Conexão direta com Databricks SQL Warehouse
- Leitura de qualquer tabela do Unity Catalog
- Configuração da tabela pela interface
- Definição do limite de registros carregados
- Cache dos dados para melhorar a performance
- Indicadores gerais de qualidade
  - Total de linhas
  - Total de colunas
  - Valores nulos
  - Registros duplicados
- Resumo das colunas
  - Tipo de dado
  - Quantidade de valores nulos
  - Percentual de nulos
  - Valores únicos
- Distribuição de valores nulos
- Distribuição dos tipos de dados
- Análise de colunas numéricas
  - Histograma
  - Boxplot
  - Detecção de outliers (IQR)
- Análise de colunas categóricas
- Matriz de correlação
- Visualização de registros duplicados
- Prévia dos dados

---

## 🛠️ Tecnologias

- Python
- Streamlit
- Pandas
- NumPy
- Altair
- Databricks SQL Connector
- Databricks SDK

---

## 📦 Instalação

Clone o repositório:

```bash
git clone https://github.com/seu-usuario/data-quality-analyzer.git

cd data-quality-analyzer
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

---

## ⚙️ Configuração

A aplicação utiliza um **Databricks SQL Warehouse**.

Configure a variável de ambiente:

```bash
DATABRICKS_WAREHOUSE_ID
```

Também é necessário possuir autenticação configurada no Databricks SDK (Profile ou Token).

---

## ▶️ Executando

```bash
streamlit run app.py
```

---

## 📊 Como utilizar

1. Informe o nome da tabela no formato:

```
catalog.schema.table
```

Exemplo:

```
workspace.default.titanic
```

2. Escolha a quantidade máxima de linhas para análise.

3. A aplicação carregará automaticamente os dados e exibirá todas as métricas e gráficos.

---

## 📈 Métricas disponíveis

- Número de linhas
- Número de colunas
- Valores ausentes
- Linhas duplicadas
- Resumo das colunas
- Distribuição de nulos
- Distribuição dos tipos de dados
- Histogramas
- Boxplots
- Outliers
- Frequência de categorias
- Correlação entre variáveis numéricas
- Prévia dos dados

---

## 📂 Estrutura

```
.
├── app.py
├── requirements.txt
└── README.md
```

---

## 🎯 Objetivo

Este projeto foi criado para facilitar análises exploratórias e verificações rápidas da qualidade de dados em tabelas armazenadas no Databricks, permitindo identificar inconsistências antes do consumo em pipelines de dados ou ferramentas de BI.

---

## 📄 Licença

Este projeto está disponível sob a licença MIT.
