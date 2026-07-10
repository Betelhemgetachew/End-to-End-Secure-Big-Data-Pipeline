import random

import pandas as pd
from faker import Faker

fake = Faker()

NUM_RECORDS = 100_000

ACCOUNT_TYPES = [
    "standard",
    "premium",
    "business"
]

KENYAN_CITIES = [
    "Nairobi",
    "Mombasa",
    "Kisumu",
    "Nakuru",
    "Eldoret",
    "Thika",
    "Nyeri",
    "Machakos",
    "Meru",
    "Kitale"
]

used_emails = set()
used_phones = set()
used_ids = set()


def generate_phone():
    """Generate a unique Kenyan phone number."""

    while True:
        prefix = random.choice(
            ["70", "71", "72", "74", "75", "76", "77", "78", "79"]
        )

        number = random.randint(1000000, 9999999)

        phone = f"+254{prefix}{number}"

        if phone not in used_phones:
            used_phones.add(phone)
            return phone


def generate_national_id():
    """Generate a unique 8-digit national ID."""

    while True:
        national_id = str(random.randint(10000000, 99999999))

        if national_id not in used_ids:
            used_ids.add(national_id)
            return national_id


def generate_account_number(index):
    """Generate sequential account numbers."""

    return f"ACC{index:06d}"


def generate_email(first_name, last_name):
    """Generate a unique email address."""

    while True:
        email = (
            f"{first_name.lower()}."
            f"{last_name.lower()}"
            f"{random.randint(1,9999)}@example.com"
        )

        if email not in used_emails:
            used_emails.add(email)
            return email


def generate_customer(index):
    """Generate one customer record."""

    first_name = fake.first_name()
    last_name = fake.last_name()

    return {
        "first_name": first_name,
        "last_name": last_name,
        "email": generate_email(first_name, last_name),
        "phone": generate_phone(),
        "national_id": generate_national_id(),
        "city": random.choice(KENYAN_CITIES),
        "account_number": generate_account_number(index),
        "account_type": random.choice(ACCOUNT_TYPES),
        "account_balance": round(random.uniform(1000, 500000), 2),
    }


def main():

    customers = []

    print(f"Generating {NUM_RECORDS:,} customer records...")

    for i in range(1, NUM_RECORDS + 1):
        customers.append(generate_customer(i))

    df = pd.DataFrame(customers)

    output_file = "dataset/customers.csv"

    df.to_csv(output_file, index=False)

    print(f"\nDataset successfully generated.")
    print(f"Records: {len(df):,}")
    print(f"Saved to: {output_file}")


if __name__ == "__main__":
    main()