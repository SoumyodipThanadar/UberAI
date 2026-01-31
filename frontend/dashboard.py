import pandas as pd

def dashboard():
    forecast = pd.read_csv("Dataset/demand_forecast.csv").tail(5)
    recommendations = pd.read_csv("Dataset/investment_insights.csv").head(5)

    print("=== FUTURE DEMAND ===")
    print(forecast)

    print("\n=== BUSINESS RECOMMENDATIONS ===")
    print(recommendations)

if __name__ == "__main__":
    dashboard()
