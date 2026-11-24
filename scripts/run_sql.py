
from pathlib import Path
from scripts.db import get_conn

ROOT = Path(__file__).resolve().parent.parent

SQL_FILES = [
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


def run_sql_file(conn, relative_path):
    file_path = ROOT / relative_path

    if not file_path.exists():
        raise FileNotFoundError(f"SQL file not found: {file_path}")

    print(f"Running: {relative_path}")

    sql = file_path.read_text(encoding="utf-8")

    with conn.cursor() as cursor:
        cursor.execute(sql)

    conn.commit()

    print(f"Completed: {relative_path}")


def main():
    conn = get_conn()

    try:
        for sql_file in SQL_FILES:
            run_sql_file(conn, sql_file)

        print("\nAll SQL files executed successfully.")

    except Exception as error:
        conn.rollback()
        print(f"\nSQL execution failed: {error}")
        raise

    finally:
        conn.close()


if __name__ == "__main__":
    main()
