import pandas as pd


def detect_cost_anomalies(df):

    # Calculate daily cost for each AWS service
    daily_service_cost = (
        df.groupby(["date", "service"], as_index=False)["cost"]
        .sum()
    )

    results = []

    # Analyze each service separately
    for service in daily_service_cost["service"].unique():

        service_data = daily_service_cost[
            daily_service_cost["service"] == service
        ].copy()

        # Need at least 4 observations for a basic IQR check
        if len(service_data) < 4:
            continue

        q1 = service_data["cost"].quantile(0.25)
        q3 = service_data["cost"].quantile(0.75)

        iqr = q3 - q1
        upper_limit = q3 + (1.5 * iqr)

        anomalies = service_data[
            service_data["cost"] > upper_limit
        ].copy()

        for _, row in anomalies.iterrows():

            results.append({
                "date": row["date"],
                "service": service,
                "daily_cost": round(row["cost"], 2),
                "normal_upper_limit": round(upper_limit, 2),
                "excess_amount": round(
                    row["cost"] - upper_limit, 2
                )
            })

    return pd.DataFrame(results)


if __name__ == "__main__":

    df = pd.read_csv("data/processed_billing.csv")
    df["date"] = pd.to_datetime(df["date"])

    anomalies = detect_cost_anomalies(df)

    print("\n===== AWS COST ANOMALY REPORT =====")

    if anomalies.empty:
        print("No unusual cost spikes detected.")

    else:
        print(anomalies.to_string(index=False))