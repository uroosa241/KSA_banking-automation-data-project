import pandas as pd
from faker import Faker
import random
from pathlib import Path

# Initialize Faker
fake = Faker()

# Make results reproducible
Faker.seed(42)
random.seed(42)

# Define absolute output directory
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data" / "raw"

# Create directory if it does not exist
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Saudi cities
cities = [
    "Riyadh",
    "Jeddah",
    "Dammam",
    "Madinah",
    "Makkah",
    "Khobar",
    "Taif",
    "Abha"
]


def generate_customers(number_of_customers):

    customers = []

    for i in range(1, number_of_customers + 1):

        customer = {
            "customer_id": f"CUST{i:06d}",
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": fake.email(),
            "phone": fake.phone_number(),
            "city": random.choice(cities),
            "gender": random.choice(["Male", "Female"]),
            "date_of_birth": fake.date_of_birth(
                minimum_age=18,
                maximum_age=80
            ),
            "registration_date": fake.date_between(
                start_date="-5y",
                end_date="today"
            )
        }

        customers.append(customer)

    return customers


if __name__ == "__main__":

    print("Generating banking customers...")

    customer_data = generate_customers(100000)

    df = pd.DataFrame(customer_data)

    output_file = DATA_DIR / "customers.csv"

    df.to_csv(output_file, index=False)

    print("Customer generation completed!")
    print("Total customers:", len(df))
    print("Saved to:", output_file)
    print(df.head())