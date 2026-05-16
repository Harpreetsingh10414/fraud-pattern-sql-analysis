import duckdb

conn = duckdb.connect("fraud.db")

with open("sql/create_amount_view.sql") as f:
    conn.execute(f.read())

print("View created: amount_flags")

conn.close()