import pandas as pd
from prophet import Prophet

def forecast_demand(path):
    df = pd.read_csv(path)
    df.columns = ['ds', 'y']

    model = Prophet()
    model.fit(df)

    future = model.make_future_dataframe(periods=30)
    forecast = model.predict(future)

    return forecast[['ds', 'yhat']]

if __name__ == "__main__":
    forecast = forecast_demand("Dataset/daily_demand.csv")
    forecast.to_csv("Dataset/demand_forecast.csv", index=False)
