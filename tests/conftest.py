import pytest
import duckdb
import pandas as pd
from datetime import datetime, timedelta


@pytest.fixture(scope="module")
def test_db():

    conn = duckdb.connect(":memory:")

    data = []

    base_time = datetime.now()

    # ----------------------------
    # NORMAL DATA
    # ----------------------------
    for i in range(20):
        data.append({
            "transaction_id": f"T{i}",
            "card_id": "CARD_NORMAL",
            "customer_id": "C1",
            "amount": 1000,
            "merchant": "Amazon",
            "city": "Delhi",
            "timestamp": base_time + timedelta(minutes=i),
            "is_fraud_seed": False
        })

    # ----------------------------
    # VELOCITY FRAUD
    # ----------------------------
    for i in range(8):
        data.append({
            "transaction_id": f"V{i}",
            "card_id": "CARD_VELOCITY",
            "customer_id": "C2",
            "amount": 200,
            "merchant": "Swiggy",
            "city": "Mumbai",
            "timestamp": base_time + timedelta(minutes=i),
            "is_fraud_seed": True
        })

    # ----------------------------
    # GEO FRAUD
    # ----------------------------
    data.append({
        "transaction_id": "G1",
        "card_id": "CARD_GEO",
        "customer_id": "C3",
        "amount": 500,
        "merchant": "Uber",
        "city": "Delhi",
        "timestamp": base_time,
        "is_fraud_seed": True
    })

    data.append({
        "transaction_id": "G2",
        "card_id": "CARD_GEO",
        "customer_id": "C3",
        "amount": 600,
        "merchant": "Uber",
        "city": "Mumbai",
        "timestamp": base_time + timedelta(minutes=30),
        "is_fraud_seed": True
    })

    # ----------------------------
    # AMOUNT FRAUD
    # ----------------------------
    for i in range(15):
        data.append({
            "transaction_id": f"A{i}",
            "card_id": "CARD_AMOUNT",
            "customer_id": "C4",
            "amount": 1000,
            "merchant": "Amazon",
            "city": "Delhi",
            "timestamp": base_time + timedelta(minutes=i),
            "is_fraud_seed": False
        })

    data.append({
        "transaction_id": "A_BIG",
        "card_id": "CARD_AMOUNT",
        "customer_id": "C4",
        "amount": 20000,
        "merchant": "Luxury",
        "city": "Delhi",
        "timestamp": base_time + timedelta(minutes=20),
        "is_fraud_seed": True
    })

    df = pd.DataFrame(data)

    conn.execute("""
        CREATE TABLE transactions AS
        SELECT * FROM df
    """)

    yield conn

    conn.close()