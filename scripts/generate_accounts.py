import pandas as pd
import random
from faker import Faker
from pathlib import Path

fake = Faker()

Faker.seed(42)
random.seed(42)

# Define absolute output directory
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data" / "raw"

# Create directory if it does not exist
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Account categories
account_types = ["Savings", "Current"]

# Account statuses
account_statuses = ["Active", "Inactive", "Blocked"]


def generate_accounts(number_of_accounts):

    # Read existing customers
    customers_file = DATA_DIR / "customers.csv"

    if not customers_file.exists():
        raise FileNotFoundError(
            f"Customers file not found: {customers_file}. "
            "Run generate_customers.py first."
        )

    customers = pd.read_csv(customers_file)

    accounts = []

    for i in range(1, number_of_accounts + 1):

        # Select a random existing customer
        customer = customers.sample(1).iloc[0]

        account = {
            "account_id": f"ACC{i:07d}",
            "customer_id": customer["customer_id"],
            "account_type": random.choice(account_types),
            "iban": f"SA{random.randint(1000000000000000000000, 9999999999999999999999)}",
            "balance": round(random.uniform(100, 100000), 2),
            "currency": "SAR",
            "account_status": random.choice(account_statuses),
            "opening_date": fake.date_between(
                start_date="-5y",
                end_date="today"
            )
        }

        accounts.append(account)

    return accounts


if __name__ == "__main__":

    print("Generating bank accounts...")

    account_data = generate_accounts(150000)

    df = pd.DataFrame(account_data)

    output_file = DATA_DIR / "accounts.csv"

    df.to_csv(output_file, index=False)

    print("Account generation completed!")
    print("Total accounts:", len(df))
    print("Saved to:", output_file)
    print(df.head())