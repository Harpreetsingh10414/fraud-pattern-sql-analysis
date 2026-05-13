import duckdb

conn = duckdb.connect("fraud.db")

# Load SQL file
with open("sql/velocity_fraud.sql", "r") as f:
    query = f.read()

df = conn.execute(query).fetchdf()

print("Velocity Fraud Results:\n")
print(df.head())

print(f"\nTotal Flags: {len(df)}")

conn.close()