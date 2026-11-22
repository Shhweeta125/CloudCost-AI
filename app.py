
import os
import sqlite3
import pandas as pd
import plotly.express as px
import streamlit as st

from dotenv import load_dotenv
from google import genai
from src.anomaly_detection import detect_cost_anomalies


# =====================================
# PAGE CONFIGURATION
# =====================================

st.set_page_config(
    page_title="CloudCost AI",
    page_icon="☁️",
    layout="wide"
)

st.title("☁️ CloudCost AI")
st.subheader("AWS Cloud Cost & Usage Intelligence Platform")

st.info(
    "Demo project: This dashboard uses simulated AWS billing data, "
    "not live billing data from an AWS account."
)


# =====================================
# DATA LOADING
# =====================================

@st.cache_data
def load_data():

    connection = sqlite3.connect("data/cloudcost.db")

    df = pd.read_sql_query(
        "SELECT * FROM billing",
        connection
    )

    connection.close()

    df["date"] = pd.to_datetime(df["date"])

    return df


try:

    df = load_data()

    if df.empty:
        st.warning("No billing records found.")
        st.stop()

    total_cost = df["cost"].sum()
    total_services = df["service"].nunique()
    total_records = len(df)


    # =====================================
    # COST OVERVIEW
    # =====================================

    st.divider()
    st.markdown("## 📊 Cost Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total AWS Cost",
        f"${total_cost:,.2f}"
    )

    col2.metric(
        "Total Services",
        total_services
    )

    col3.metric(
        "Billing Records",
        total_records
    )


    # =====================================
    # SERVICE-WISE COST ANALYSIS
    # =====================================

    st.divider()
    st.markdown("## 💰 Service-wise Cost Analysis")

    service_cost = (
        df.groupby("service", as_index=False)["cost"]
        .sum()
        .sort_values("cost", ascending=False)
    )

    fig_service = px.bar(
        service_cost,
        x="service",
        y="cost",
        color="service",
        title="AWS Cost by Service",
        labels={
            "cost": "Cost ($)",
            "service": "AWS Service"
        }
    )

    st.plotly_chart(
        fig_service,
        width="stretch"
    )


    # =====================================
    # REGION-WISE COST ANALYSIS
    # =====================================

    st.divider()
    st.markdown("## 🌍 Region-wise Cost Analysis")

    region_cost = (
        df.groupby("region", as_index=False)["cost"]
        .sum()
    )

    fig_region = px.pie(
        region_cost,
        names="region",
        values="cost",
        title="AWS Spending by Region"
    )

    st.plotly_chart(
        fig_region,
        width="stretch"
    )


    # =====================================
    # DAILY COST TREND
    # =====================================

    st.divider()
    st.markdown("## 📅 Daily Cost Trend")

    daily_cost = (
        df.groupby("date", as_index=False)["cost"]
        .sum()
        .sort_values("date")
    )

    fig_daily = px.line(
        daily_cost,
        x="date",
        y="cost",
        markers=True,
        title="Daily AWS Expenditure",
        labels={
            "cost": "Cost ($)",
            "date": "Date"
        }
    )

    st.plotly_chart(
        fig_daily,
        width="stretch"
    )


    # =====================================
    # COST ANOMALY DETECTION
    # =====================================

    st.divider()
    st.markdown("## 🚨 AWS Cost Anomaly Detection")

    st.write(
        "Identify unusual daily spending patterns "
        "across AWS services using statistical analysis."
    )

    anomalies = detect_cost_anomalies(df)

    if anomalies.empty:

        st.success(
            "No unusual cost spikes detected in the current dataset."
        )

    else:

        st.warning(
            f"{len(anomalies)} potential cost anomalies detected!"
        )

        st.dataframe(
            anomalies,
            width="stretch"
        )

        st.download_button(
            label="Download Anomaly Report",
            data=anomalies.to_csv(index=False).encode("utf-8"),
            file_name="aws_cost_anomaly_report.csv",
            mime="text/csv"
        )


    # =====================================
    # GENERATIVE AI COST OPTIMIZATION
    # =====================================

    st.divider()

    st.markdown("## 🤖 AI-Powered Cost Optimization")

    st.write(
        "Get intelligent AWS spending analysis and "
        "cost optimization recommendations using Gemini AI."
    )

    if "ai_insights" not in st.session_state:
        st.session_state.ai_insights = ""

    if st.button("✨ Generate AI Cost Insights"):

        load_dotenv()

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:

            st.error(
                "Gemini API key not found. Check your .env file."
            )

        else:

            try:

                service_summary = (
                    df.groupby("service")["cost"]
                    .sum()
                    .sort_values(ascending=False)
                    .to_string()
                )

                prompt = f"""
                You are an AWS Cloud Cost Optimization Advisor.

                Analyse this simulated AWS billing data.

                Total expenditure: ${total_cost:.2f}

                Service-wise expenditure:
                {service_summary}

                Provide:

                1. Summary of spending patterns.
                2. Highest spending AWS service.
                3. Three practical cost optimization suggestions.
                4. Additional metrics needed to verify actual savings.

                Important:
                - This is simulated billing data.
                - Do not claim any resource is unused.
                - Do not invent actual savings.
                - Clearly distinguish recommendations from verified findings.
                """

                client = genai.Client(api_key=api_key)

                with st.spinner(
                    "Gemini is analysing your billing data..."
                ):

                    response = client.models.generate_content(
                        model="gemini-3.8-flash",
                        contents=prompt
                    )

                    st.session_state.ai_insights = response.text

            except Exception as e:

                st.error(f"AI analysis failed: {e}")

    if st.session_state.ai_insights:

        st.markdown("### 📋 AI Analysis Report")

        st.markdown(
            st.session_state.ai_insights
        )


    # =====================================
    # DETAILED BILLING DATA
    # =====================================

    st.divider()

    st.markdown("## 📋 Detailed Billing Data")

    st.dataframe(
        df,
        width="stretch"
    )

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇️ Download Billing CSV",
        data=csv,
        file_name="aws_billing_report.csv",
        mime="text/csv"
    )

    st.success(
        "CloudCost AI Dashboard Loaded Successfully!"
    )


except Exception as e:

    st.error(
        f"Unable to load dashboard: {e}"
    )

    st.info(
        "First run the data ingestion, transformation and database "
        "modules to generate data/cloudcost.db."
    )
