from faker import Faker
import pandas as pd
import random
import uuid
from datetime import datetime, timedelta

fake = Faker("en_IN")

NUM_CUSTOMERS = 10000
NUM_TRANSACTIONS = 1_000_000

cities = [
    "Delhi",
    "Mumbai",
    "Bangalore",
    "Chennai",
    "Hyderabad",
    "Pune",
    "Kolkata",
    "Ahmedabad",
    "Jaipur",
    "Lucknow"
]

merchants = [
    "Amazon",
    "Flipkart",
    "Swiggy",
    "Zomato",
    "Uber",
    "Reliance Fresh",
    "DMart",
    "Myntra",
    "BigBasket",
    "Croma"
]

print("Creating customer profiles...")

customers = []

for i in range(NUM_CUSTOMERS):

    customer_id = f"CUST_{i}"

    home_city = random.choice(cities)

    avg_spend = random.randint(500, 5000)

    cards = [
        f"CARD_{uuid.uuid4().hex[:10]}"
        for _ in range(random.randint(1, 3))
    ]

    customers.append({
        "customer_id": customer_id,
        "home_city": home_city,
        "avg_spend": avg_spend,
        "cards": cards
    })

print("Generating transactions...")

transactions = []

start_date = datetime.now() - timedelta(days=90)

for i in range(NUM_TRANSACTIONS):

    customer = random.choice(customers)

    card_id = random.choice(customer["cards"])

    amount = round(
        random.gauss(
            customer["avg_spend"],
            customer["avg_spend"] * 0.3
        ),
        2
    )

    amount = max(amount, 50)

    txn_time = start_date + timedelta(
        minutes=random.randint(0, 90 * 24 * 60)
    )

    transactions.append({
        "transaction_id": str(uuid.uuid4()),
        "card_id": card_id,
        "customer_id": customer["customer_id"],
        "amount": amount,
        "merchant": random.choice(merchants),
        "city": customer["home_city"],
        "timestamp": txn_time,
        "is_fraud_seed": False
    })

print("Injecting fraud seeds...")

# -------------------------------------------------
# FRAUD TYPE 1 — Velocity Fraud
# same card many txns in short time
# -------------------------------------------------

for _ in range(3000):

    customer = random.choice(customers)

    card_id = random.choice(customer["cards"])

    base_time = start_date + timedelta(
        minutes=random.randint(0, 90 * 24 * 60)
    )

    for i in range(8):

        transactions.append({
            "transaction_id": str(uuid.uuid4()),
            "card_id": card_id,
            "customer_id": customer["customer_id"],
            "amount": random.randint(100, 1000),
            "merchant": random.choice(merchants),
            "city": customer["home_city"],
            "timestamp": base_time + timedelta(minutes=i),
            "is_fraud_seed": True
        })

# -------------------------------------------------
# FRAUD TYPE 2 — Geo Fraud
# same card in two cities quickly
# -------------------------------------------------

for _ in range(2000):

    customer = random.choice(customers)

    card_id = random.choice(customer["cards"])

    city1, city2 = random.sample(cities, 2)

    base_time = start_date + timedelta(
        minutes=random.randint(0, 90 * 24 * 60)
    )

    transactions.append({
        "transaction_id": str(uuid.uuid4()),
        "card_id": card_id,
        "customer_id": customer["customer_id"],
        "amount": random.randint(500, 3000),
        "merchant": random.choice(merchants),
        "city": city1,
        "timestamp": base_time,
        "is_fraud_seed": True
    })

    transactions.append({
        "transaction_id": str(uuid.uuid4()),
        "card_id": card_id,
        "customer_id": customer["customer_id"],
        "amount": random.randint(500, 3000),
        "merchant": random.choice(merchants),
        "city": city2,
        "timestamp": base_time + timedelta(minutes=30),
        "is_fraud_seed": True
    })

# -------------------------------------------------
# FRAUD TYPE 3 — Amount Spike
# -------------------------------------------------

for _ in range(3000):

    customer = random.choice(customers)

    card_id = random.choice(customer["cards"])

    txn_time = start_date + timedelta(
        minutes=random.randint(0, 90 * 24 * 60)
    )

    transactions.append({
        "transaction_id": str(uuid.uuid4()),
        "card_id": card_id,
        "customer_id": customer["customer_id"],
        "amount": customer["avg_spend"] * random.randint(8, 15),
        "merchant": "Luxury Store",
        "city": customer["home_city"],
        "timestamp": txn_time,
        "is_fraud_seed": True
    })

print("Creating DataFrame...")

df = pd.DataFrame(transactions)

df["timestamp"] = pd.to_datetime(df["timestamp"])

print(df.head())

print(f"Total rows: {len(df)}")

print("Saving CSV...")

df.to_csv("transactions.csv", index=False)

print("Done.")