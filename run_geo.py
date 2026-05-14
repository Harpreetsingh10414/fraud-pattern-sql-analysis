import duckdb

conn = duckdb.connect("fraud.db")

with open("sql/geo_fraud.sql") as f:
    query = f.read()

df = conn.execute(query).fetchdf()

print("Geo Fraud Results:\n")
print(df.head())

print(f"\nTotal Flags: {len(df)}")

conn.close()