
import os
import sqlite3
import pandas as pd

from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing. Check your .env file.")

# Connect to billing database
connection = sqlite3.connect("data/cloudcost.db")

# Get service-wise billing information
query = """
SELECT service,
       ROUND(SUM(cost), 2) AS total_cost
FROM billing
GROUP BY service
ORDER BY total_cost DESC;
"""

service_data = pd.read_sql_query(query, connection)

# Get total expenditure
total_cost = service_data["total_cost"].sum()

connection.close()

# Prepare billing information for AI
billing_summary = service_data.to_string(index=False)

prompt = f"""
You are an AWS Cloud Cost Optimization Advisor.

Analyse the following sample AWS billing data.

Total expenditure: ${total_cost:.2f}

Service-wise expenditure:
{billing_summary}

Please provide:

1. A simple explanation of the spending pattern.
2. Which service has the highest expenditure?
3. Three possible cost optimization suggestions.
4. What additional information would be needed
   before confirming actual savings.

Important:
- This is simulated billing data.
- Do not claim that any resource is unused.
- Do not invent actual savings or utilization metrics.
- Clearly distinguish suggestions from verified findings.
"""

# Connect to Gemini
client = genai.Client(api_key=api_key)

print("\n===== CLOUDCOST AI ADVISOR =====")

response = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents=prompt
)

print(response.text)

print("\nAI ANALYSIS COMPLETED!")
