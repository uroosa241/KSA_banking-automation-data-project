# KSA Banking Automation – Data Engineering Project

## Project Overview

This project demonstrates an end-to-end banking data engineering pipeline designed to automate the ingestion, transformation, storage, validation, and analysis of banking data.

The solution uses Python, PostgreSQL, SQL, Docker, and Apache Airflow to build an automated data warehouse for banking analytics.

The pipeline processes customer, account, and transaction data and transforms raw records into structured analytical datasets for reporting, operational monitoring, and fraud analysis.

## Project Objectives

- Automate banking data ingestion using Python.
- Build a structured PostgreSQL data warehouse.
- Implement a multi-layer data architecture.
- Transform raw banking data using SQL.
- Orchestrate workflows using Apache Airflow.
- Implement data quality validation.
- Generate fraud indicators from transaction data.
- Create analytical data marts for business reporting.
- Automate code testing using GitHub Actions.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Data generation and ingestion |
| PostgreSQL | Data warehouse |
| SQL | Data transformation and analytics |
| Apache Airflow | Workflow orchestration |
| Docker | Containerization |
| Docker Compose | Multi-container management |
| Git | Version control |
| GitHub | Source code management |
| GitHub Actions | Continuous Integration |
| pytest | Automated testing |

## Architecture

The project follows a layered data warehouse architecture.

```text
Python Data Generation
          |
          v
      Raw CSV Files
          |
          v
   PostgreSQL RAW Layer
          |
          v
     STAGING Layer
   (Data Cleaning)
          |
          v
       CORE Layer
 (Dimensions and Facts)
          |
          v
       MARTS Layer
  (Business Analytics)
          |
          v
  Data Quality Validation
          |
          v
    Fraud Indicators
          |
          v
     Audit Logging
```

Apache Airflow orchestrates the pipeline execution.

## Data Sources

The project uses generated banking datasets:

| Dataset | Records |
|---|---:|
| Customers | 100,000 |
| Accounts | 150,000 |
| Transactions | 30,000 |

The datasets are generated using Python and Faker.

Note: Raw CSV data is excluded from this repository to avoid publishing potentially sensitive or large datasets.

## Data Warehouse Layers

### 1. RAW Layer

Stores the original ingested banking records.

- Customers
- Accounts
- Transactions

### 2. STAGING Layer

Cleans and standardizes the raw data.

- Data type conversion
- NULL handling
- Data standardization
- Data preparation

### 3. CORE Layer

Contains the central data warehouse models.

- Customer dimension
- Account dimension
- Other analytical dimensions
- Transaction fact table

### 4. MARTS Layer

Provides business-ready analytical datasets.

- Customer analytics
- Transaction analytics
- Branch performance
- Executive KPIs

## Pipeline Features

### Data Ingestion
Python scripts load CSV files into PostgreSQL.

### Data Transformation
SQL scripts transform raw data into staging, core, and marts layers.

### Workflow Orchestration
Apache Airflow manages pipeline execution and task dependencies.

### Data Quality
Validation scripts check data consistency and quality.

### Fraud Analysis
Fraud indicators identify potentially suspicious banking transactions.

### Audit Logging
Pipeline execution information is recorded for monitoring and troubleshooting.

## Project Structure

```text
ksa-banking-data-engineering/
│
├── dags/
│   └── banking_pipeline.py
│
├── scripts/
│   ├── db.py
│   ├── generate_accounts.py
│   ├── generate_customers.py
│   ├── generate_transactions.py
│   ├── load.py
│   ├── pipeline.py
│   └── run_sql.py
│
├── sql/
│   ├── ddl/
│   ├── staging/
│   ├── core/
│   ├── marts/
│   ├── dq/
│   ├
