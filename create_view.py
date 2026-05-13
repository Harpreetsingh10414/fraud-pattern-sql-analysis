import duckdb

conn = duckdb.connect("fraud.db")

with open("sql/create_velocity_view.sql") as f:
    conn.execute(f.read())

print("View created: velocity_flags")

conn.close()