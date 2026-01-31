import pandas as pd

def seasonality(df):
    return df.groupby('weekday').size().reset_index(name='rides')

if __name__ == "__main__":
    df = pd.read_csv("Dataset/cleaned_data.csv")
    season = seasonality(df)
    season.to_csv("Dataset/seasonality.csv", index=False)
