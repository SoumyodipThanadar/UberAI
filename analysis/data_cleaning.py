import pandas as pd

def load_and_clean_data(path):
    df = pd.read_csv(path)

    df['booking_time'] = pd.to_datetime(df['booking_time'])
    df.dropna(inplace=True)

    df['date'] = df['booking_time'].dt.date
    df['hour'] = df['booking_time'].dt.hour
    df['weekday'] = df['booking_time'].dt.weekday

    return df

if __name__ == "__main__":
    df = load_and_clean_data("Dataset/ncr_ride_bookings.csv")
    df.to_csv("Dataset/cleaned_data.csv", index=False)