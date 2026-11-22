# ☁️ CloudCost AI – AWS Cost Optimization & Intelligence Platform

## Overview

CloudCost AI is a cloud cost analytics and optimization platform designed to analyze AWS billing data, identify spending patterns, and generate AI-powered cost optimization recommendations.

The project uses Python, Pandas, SQLite, SQL, Streamlit, and Google's Gemini API to build an end-to-end data analytics pipeline.

**Note:** This project currently uses simulated AWS billing data for demonstration. It is not connected to a live AWS account.

## Key Features

- **Data Ingestion:** Reads AWS billing data from CSV files.
- **Data Transformation:** Cleans and processes billing data using Pandas.
- **Data Storage:** Stores processed billing records in an SQLite database.
- **SQL Analytics:** Analyzes total expenditure, service-wise spending, region-wise spending, daily costs, and high-cost services.
- **AI-Powered Insights:** Uses Gemini API to generate spending analysis and optimization recommendations.
- **Interactive Dashboard:** Visualizes billing information through Streamlit and Plotly.
- **Anomaly Detection:** Identifies potential unusual spending patterns using the IQR statistical method.

## Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| Data Processing | Pandas |
| Database | SQLite |
| Query Language | SQL |
| Dashboard | Streamlit |
| Visualization | Plotly |
| Generative AI | Google Gemini API |
| Anomaly Detection | IQR Method |

## Project Architecture

```text
CSV Billing Data
       |
       v
Data Ingestion
       |
       v
Data Transformation
       |
       v
SQLite Database
       |
       v
SQL Analytics
       |
       v
Streamlit Dashboard
       |
       v
Gemini AI Cost Insights
```

## Project Structure

```text
CloudCost-AI/
│
├── data/
│   ├── aws_billing.csv
│   ├── processed_billing.csv
│   └── cloudcost.db
│
├── src/
│   ├── data_ingestion.py
│   ├── data_transformation.py
│   ├── database.py
│   ├── analytics.py
│   ├── ai_insights.py
│   └── anomaly_detection.py
│
├── app.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd CloudCost-AI
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure Gemini API

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
```

Keep your API key private. Never commit `.env` to GitHub.

### 5. Run the data pipeline

Run the scripts in this order:

```bash
python src/data_ingestion.py
python src/data_transformation.py
python src/database.py
python src/analytics.py
python src/ai_insights.py
```

### 6. Launch the dashboard

```bash
python -m streamlit run app.py
```

## SQL Analytics

The project performs the following analytical operations:

1. Calculate total AWS expenditure.
2. Calculate service-wise expenditure.
3. Calculate region-wise expenditure.
4. Analyze daily expenditure.
5. Identify high-cost services with expenditure above $50.

## AI Integration

CloudCost AI integrates Google's Gemini API to:

- Explain billing and spending patterns.
- Identify the highest expenditure service.
- Generate potential cost optimization recommendations.
- Describe additional information required to verify actual savings.

The recommendations are advisory and are not verified savings.

## Sample Dataset

The demonstration dataset contains:

- 20 billing records.
- 5 AWS services: EC2, S3, RDS, Lambda, and CloudWatch.
- 3 AWS regions.
- 7 days of simulated billing information.

**Total simulated expenditure: $643.20**

## Future Scope

- Integration with live AWS billing data.
- AWS S3 for cloud data storage.
- AWS Glue for data transformation.
- AWS Athena for cloud-based SQL analytics.
- Enhanced cost forecasting and monitoring.

## Disclaimer

This is an educational and demonstration project. The billing dataset is simulated and does not represent actual AWS account expenditure.

---

**CloudCost AI – Turning Cloud Billing Data into Actionable Insights.**