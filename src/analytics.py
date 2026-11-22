
import sqlite3
import pandas as pd

# Connect to our existing database
connection = sqlite3.connect("data/cloudcost.db")

# 1. Total AWS expenditure
query1 = """
SELECT ROUND(SUM(cost), 2) AS total_cost
FROM billing;
"""

# 2. Service-wise expenditure
query2 = """
SELECT service,
       ROUND(SUM(cost), 2) AS total_cost
FROM billing
GROUP BY service
ORDER BY total_cost DESC;
"""

# 3. Region-wise expenditure
query3 = """
SELECT region,
       ROUND(SUM(cost), 2) AS total_cost
FROM billing
GROUP BY region
ORDER BY total_cost DESC;
"""

# 4. Daily expenditure
query4 = """
SELECT date,
       ROUND(SUM(cost), 2) AS daily_cost
FROM billing
GROUP BY date
ORDER BY date;
"""

# 5. Services spending more than $50
query5 = """
SELECT service,
       ROUND(SUM(cost), 2) AS total_cost
FROM billing
GROUP BY service
HAVING SUM(cost) > 50
ORDER BY total_cost DESC;
"""

# Execute and display all queries
queries = [
    ("TOTAL AWS EXPENDITURE", query1),
    ("SERVICE-WISE EXPENDITURE", query2),
    ("REGION-WISE EXPENDITURE", query3),
    ("DAILY EXPENDITURE", query4),
    ("HIGH-COST SERVICES (ABOVE $50)", query5)
]

for title, query in queries:
    print("\n" + "=" * 45)
    print(title)
    print("=" * 45)

    result = pd.read_sql_query(query, connection)
    print(result.to_string(index=False))

connection.close()

print("\nSQL ANALYTICS COMPLETED SUCCESSFULLY!")
