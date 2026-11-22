import pandas as pd

# Read billing data
df = pd.read_csv("data/aws_billing.csv")

print("\n===== AWS BILLING DATA =====")
print(df.head())

print("\n===== DATASET INFORMATION =====")
df.info()

print("\nTotal Records:", len(df))

total_cost = df["cost"].sum()
print("\nTotal AWS Cost: $", round(total_cost, 2))