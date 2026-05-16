import duckdb

conn = duckdb.connect("fraud.db")

df = conn.execute("""
SELECT * FROM amount_flags LIMIT 10
""").fetchdf()

print(df)

conn.close()