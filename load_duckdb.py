import duckdb

conn = duckdb.connect("fraud.db")

conn.execute("""
CREATE OR REPLACE TABLE transactions AS
SELECT *
FROM read_csv_auto('transactions.csv')
""")

count = conn.execute("""
SELECT COUNT(*) FROM transactions
""").fetchone()[0]

print(f"Loaded rows: {count}")

conn.close()