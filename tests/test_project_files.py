
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

REQUIRED_FILES = [
    "scripts/db.py",
    "scripts/load.py",
    "scripts/run_sql.py",
    "scripts/pipeline.py",

    "sql/ddl/01_create_schemas.sql",

    "sql/staging/01_clean_customers.sql",
    "sql/staging/02_clean_accounts.sql",
    "sql/staging/03_clean_transactions.sql",

    "sql/core/01_create_dimensions.sql",
    "sql/core/02_create_fact.sql",
    "sql/core/03_load_warehouse.sql",

    "sql/marts/01_customer_analytics.sql",
    "sql/marts/02_transaction_analytics.sql",
    "sql/marts/03_branch_performance.sql",
    "sql/marts/04_executive_kpis.sql",

    "sql/dq/01_validation_checks.sql",
    "sql/fraud/01_fraud_indicators.sql",
    "sql/audit/01_pipeline_audit.sql",
]


def test_required_project_files_exist():
    for file_name in REQUIRED_FILES:
        assert (ROOT / file_name).exists(), (
            f"Missing project file: {file_name}"
        )


def test_sql_files_are_not_empty():
    sql_files = [
        ROOT / file_name
        for file_name in REQUIRED_FILES
        if file_name.endswith(".sql")
    ]

    for file_path in sql_files:
        assert file_path.stat().st_size > 0, (
            f"Empty SQL file: {file_path}"
        )


def test_pipeline_script_exists():
    assert (ROOT / "scripts/pipeline.py").exists()
