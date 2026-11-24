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

# Transaction categories
transaction_types = [
    "Deposit",
    "Withdrawal",
    "Transfer",
    "Payment"
]

transaction_statuses = [
    "Success",
    "Failed",
    "Pending"
]


def generate_transactions(number_of_transactions):

    print("Reading bank accounts...")

    accounts_file = DATA_DIR / "accounts.csv"

    if not accounts_file.exists():
        raise FileNotFoundError(
            f"Accounts file not found: {accounts_file}. "
            "Run generate_accounts.py first."
        )

    accounts = pd.read_csv(accounts_file)

    transactions = []

    print("Generating transactions...")

    for i in range(1, number_of_transactions + 1):

        # Select a random bank account
        account = accounts.sample(1).iloc[0]

        transaction = {
            "transaction_id": f"TXN{i:09d}",
            "account_id": account["account_id"],
            "customer_id": account["customer_id"],
            "transaction_type": random.choice(transaction_types),
            "amount": round(random.uniform(10, 50000), 2),
            "currency": "SAR",
            "transaction_date": fake.date_time_between(
                start_date="-2y",
                end_date="now"
            ),
            "transaction_status": random.choice(transaction_statuses),
            "branch_id": f"BR{random.randint(1, 100):03d}"
        }

        transactions.append(transaction)

        if i % 10000 == 0:
            print(f"Generated {i:,} transactions")

    return transactions


if __name__ == "__main__":

    print("Starting banking transaction generator...")

    transaction_data = generate_transactions(30000)

    print("Converting data to DataFrame...")

    df = pd.DataFrame(transaction_data)

    output_file = DATA_DIR / "transactions.csv"

    print("Saving transactions CSV...")

    df.to_csv(output_file, index=False)

    print("Transaction generation completed!")
    print("Total transactions:", len(df))
    print("Saved to:", output_file)
    print(df.head())