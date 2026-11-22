
import pandas as pd
import sqlite3

# Step 1: Read cleaned billing data
df = pd.read_csv("data/processed_billing.csv")

# Step 2: Connect to SQLite database
connection = sqlite3.connect("data/cloudcost.db")

# Step 3: Create a table and store billing records
df.to_sql(
    "billing",
    connection,
    if_exists="replace",
    index=False
)

print("Billing data stored successfully!")

# Step 4: Retrieve records using SQL
query = """
SELECT * FROM billing
LIMIT 5;
"""

result = pd.read_sql_query(query, connection)

print("\n===== BILLING RECORDS FROM DATABASE =====")
print(result)

# Step 5: Calculate total AWS expenditure using SQL
cost_query = """
SELECT SUM(cost) AS total_cost
FROM billing;
"""

total = pd.read_sql_query(cost_query, connection)

print("\n===== TOTAL AWS EXPENDITURE =====")
print(total)

# Step 6: Count total records
count_query = """
SELECT COUNT(*) AS total_records
FROM billing;
"""

count = pd.read_sql_query(count_query, connection)

print("\nTotal Records:", count.iloc[0]["total_records"])

# Step 7: Close database connection
connection.close()

print("\nDatabase connection closed!")
