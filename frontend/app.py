import streamlit as st
import pandas as pd
import os

# -------- PAGE CONFIG --------
st.set_page_config(
    page_title="UberAI Dashboard",
    page_icon="🚕",
    layout="wide"
)

# -------- BETTER COLOR CSS --------
st.markdown("""
<style>

/* Background */
.stApp {
    background: linear-gradient(135deg, #1e3c72, #2a5298);
    color: white;
}

/* Main Title */
h1 {
    color: #FFD700;
    text-align: center;
    font-size: 42px;
}

/* Headers */
h2, h3 {
    color: #FF9966;
}

/* Metric cards */
[data-testid="stMetric"] {
    background: linear-gradient(135deg, #667eea, #764ba2);
    padding: 20px;
    border-radius: 15px;
    color: white;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.3);
}

/* Tables */
[data-testid="stDataFrame"] {
    background-color: white;
    border-radius: 10px;
}

/* Select box label */
label {
    color: #FFD700 !important;
    font-size: 18px !important;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)

# -------- FILE PATHS --------
base = os.path.dirname(os.path.abspath(__file__))

forecast_path = os.path.join(base, "..", "Dataset", "demand_forecast.csv")
insights_path = os.path.join(base, "..", "Dataset", "investment_insights.csv")
growth_path = os.path.join(base, "..", "Dataset", "growth_index.csv")

# -------- LOAD DATA --------
forecast = pd.read_csv(forecast_path)
insights = pd.read_csv(insights_path)
growth_df = pd.read_csv(growth_path)

# Clean columns
insights.columns = insights.columns.str.strip()
growth_df.columns = growth_df.columns.str.strip()

# -------- MERGE --------
if "zone" in insights.columns and "zone" in growth_df.columns:
    insights = insights.merge(growth_df, on="zone", how="left")

# -------- TITLE --------
st.title("🚕 UberAI Smart Demand Dashboard")

st.markdown(
    "<hr style='border: 3px solid gold; border-radius: 5px;'>",
    unsafe_allow_html=True
)

# -------- METRICS --------
col1, col2, col3 = st.columns(3)

col1.metric("📊 Avg Demand", round(forecast["yhat"].mean(), 1))
col2.metric("🔥 Max Demand", round(forecast["yhat"].max(), 1))
col3.metric("📍 Total Zones", insights["zone"].nunique())

# -------- DEMAND CHART --------
st.header("📈 Demand Forecast")

st.line_chart(
    forecast.set_index("ds")["yhat"],
    height=350
)

st.dataframe(forecast.tail(10), use_container_width=True)

# -------- ZONE FILTER --------
st.header("💡 Investment Insights")

zone = st.selectbox(
    "📍 Select Zone",
    insights["zone"].unique()
)

zone_data = insights[insights["zone"] == zone]

st.dataframe(zone_data, use_container_width=True)

# -------- TOP ZONES --------
st.header("🏆 Top Growth Zones")

if "growth_index" in insights.columns:
    top_zones = insights.sort_values(
        by="growth_index",
        ascending=False
    ).head(5)

    st.dataframe(top_zones, use_container_width=True)

else:
    st.warning("growth_index column not found!")


