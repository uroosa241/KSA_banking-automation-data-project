import os
import pandas as pd

def test_customers_file_exists():
    assert os.path.exists("data/raw/customers.csv")

def test_accounts_file_exists():
    assert os.path.exists("data/raw/accounts.csv")

def test_transactions_file_exists():
    assert os.path.exists("data/raw/transactions.csv")

def test_customer_columns():
    df = pd.read_csv("data/raw/customers.csv", nrows=5)
    assert "customer_id" in df.columns

def test_account_columns():
    df = pd.read_csv("data/raw/accounts.csv", nrows=5)
    assert "account_id" in df.columns


def test_transaction_columns():
    df = pd.read_csv("data/raw/transactions.csv", nrows=5)

    assert "transaction_id" in df.columns
    assert "account_id" in df.columns
    assert "customer_id" in df.columns
    assert "transaction_type" in df.columns
    assert "amount" in df.columns
    assert "currency" in df.columns
    assert "transaction_date" in df.columns
    assert "transaction_status" in df.columns
    assert "branch_id" in df.columns
