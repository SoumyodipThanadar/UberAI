import pandas as pd

def growth_index(df):
    zone_growth = df.groupby('pickup_zone').size().reset_index(name='rides')
    zone_growth['growth_index'] = zone_growth['rides'] / zone_growth['rides'].max()
    return zone_growth

if __name__ == "__main__":
    df = pd.read_csv("Dataset/cleaned_data.csv")
    growth = growth_index(df)
    growth.to_csv("Dataset/growth_index.csv", index=False)
