import duckdb

conn = duckdb.connect("fraud.db")

with open("sql/amount_deviation.sql") as f:
    query = f.read()

df = conn.execute(query).fetchdf()

print("Amount Fraud Results:\n")
print(df.head())

print(f"\nTotal Flags: {len(df)}")

conn.close()