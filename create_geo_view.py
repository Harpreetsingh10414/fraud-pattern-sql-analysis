import duckdb

conn = duckdb.connect("fraud.db")

with open("sql/create_geo_view.sql") as f:
    conn.execute(f.read())

print("View created: geo_flags")

conn.close()