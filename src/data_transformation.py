
import pandas as pd

# 1. Load original billing data
df = pd.read_csv("data/aws_billing.csv")

print("Original records:", len(df))

# 2. Remove duplicate records
df = df.drop_duplicates()

# 3. Convert date column into datetime format
df["date"] = pd.to_datetime(df["date"], errors="coerce")

# 4. Convert numerical columns into numeric format
df["cost"] = pd.to_numeric(df["cost"], errors="coerce")
df["usage_hours"] = pd.to_numeric(
    df["usage_hours"], errors="coerce"
)

# 5. Remove rows with missing or invalid required values
required_columns = [
    "date", "service", "region", "usage_hours", "cost"
]

df = df.dropna(subset=required_columns)

# 6. Remove negative cost or usage values
df = df[
    (df["cost"] >= 0) &
    (df["usage_hours"] >= 0)
]

# 7. Standardize service and region names
df["service"] = df["service"].str.strip()
df["region"] = df["region"].str.strip()

# 8. Save cleaned data
df.to_csv("data/processed_billing.csv", index=False)

# 9. Display results
print("\n===== CLEANED BILLING DATA =====")
print(df.head())

print("\n===== TRANSFORMATION SUMMARY =====")
print("Cleaned records:", len(df))
print("Missing values:", df.isnull().sum().sum())
print("Total AWS Cost: $", round(df["cost"].sum(), 2))

print("\nCleaned data saved successfully!")
