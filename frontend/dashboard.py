import os
import pandas as pd

def dashboard():
    base = os.path.dirname(os.path.abspath(__file__))

    forecast_path = os.path.join(base, "..", "Dataset", "demand_forecast.csv")
    rec_path = os.path.join(base, "..", "Dataset", "investment_insights.csv")

    forecast = pd.read_csv(forecast_path).tail(5)
    recommendations = pd.read_csv(rec_path).head(5)

    print("=== FUTURE DEMAND ===")
    print(forecast)

    print("\n=== BUSINESS RECOMMENDATIONS ===")
    print(recommendations)

dashboard()
