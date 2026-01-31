import pandas as pd

def daily_demand(df):
    return df.groupby('date').size().reset_index(name='rides')

if __name__ == "__main__":
    df = pd.read_csv("UberAI/Dataset/cleaned_data.csv")
    trend = daily_demand(df)
    trend.to_csv("UberAI/Dataset/daily_demand.csv", index=False)
