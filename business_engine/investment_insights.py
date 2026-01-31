import pandas as pd

df = pd.read_csv("Dataset/business_recommendations.csv")

df['investment_action'] = df['recommendation'].apply(
    lambda x: "Add Drivers" if "High" in x else "Monitor"
)

df.to_csv("Dataset/investment_insights.csv", index=False)
