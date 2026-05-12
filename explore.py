import duckdb

conn = duckdb.connect("fraud.db")

print("\nTop Cities\n")

print(conn.execute("""
SELECT city, COUNT(*) as total
FROM transactions
GROUP BY city
ORDER BY total DESC
LIMIT 10
""").fetchdf())

print("\nAverage Amount By Card\n")

print(conn.execute("""
SELECT card_id,
       ROUND(AVG(amount),2) as avg_amt
FROM transactions
GROUP BY card_id
LIMIT 10
""").fetchdf())

conn.close()