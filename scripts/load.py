
import os
from scripts.db import get_conn

FILES = {
    "customers": {
        "path": "data/raw/customers.csv",
        "table": "raw.customers",
        "columns": """
            customer_id, first_name, last_name, email,
            phone, city, gender, date_of_birth, registration_date
        """
    },

    "accounts": {
        "path": "data/raw/accounts.csv",
        "table": "raw.accounts",
        "columns": """
            account_id, customer_id, account_type, iban,
            balance, currency, account_status, opening_date
        """
    },

    "transactions": {
        "path": "data/raw/transactions.csv",
        "table": "raw.transactions",
        "columns": """
            transaction_id, account_id, customer_id,
            transaction_type, amount, currency,
            transaction_date, transaction_status, branch_id
        """
    }
}


def load_csv(conn, file_path, table_name, columns):

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    print(f"Loading {file_path}...")

    query = f"""
        COPY {table_name} ({columns})
        FROM STDIN
        WITH (FORMAT CSV, HEADER TRUE)
    """

    with conn.cursor() as cursor:
        with open(file_path, "r", encoding="utf-8") as file:
            cursor.copy_expert(query, file)

    print(f"Successfully loaded {table_name}")


def main():

    conn = get_conn()

    try:

        with conn.cursor() as cursor:
            cursor.execute("""
                TRUNCATE TABLE
                    raw.transactions,
                    raw.accounts,
                    raw.customers;
            """)

        for item in FILES.values():

            load_csv(
                conn,
                item["path"],
                item["table"],
                item["columns"]
            )

        conn.commit()

        print("\nAll CSV files loaded successfully!")

    except Exception as error:

        conn.rollback()

        print("Loading failed:", error)

        raise

    finally:

        conn.close()


if __name__ == "__main__":
    main()
