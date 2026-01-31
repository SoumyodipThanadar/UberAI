# import pandas as pd

# def load_and_clean_data(path):
#     df = pd.read_csv(path)

#     df['booking_time'] = pd.to_datetime(df['booking_time'])
#     df.dropna(inplace=True)

#     df['date'] = df['booking_time'].dt.date
#     df['hour'] = df['booking_time'].dt.hour
#     df['weekday'] = df['booking_time'].dt.weekday

#     return df

# if __name__ == "__main__":
#     df = load_and_clean_data("UberAI/Dataset/ncr_ride_bookings.csv")
#     df.to_csv("UberAI/Dataset/cleaned_data.csv", index=False)

import pandas as pd
import numpy as np
from datetime import datetime

def load_and_clean_data(path):
    """
    Load and clean Uber ride booking data with proper handling of missing values
    and data type conversions.
    """
    # Load the data
    df = pd.read_csv(path)
    
    print(f"Original dataset shape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")
    
    # Standardize column names (remove spaces, make lowercase)
    df.columns = [col.strip().lower().replace(' ', '_') for col in df.columns]
    
    # Convert booking_time to datetime (handle the time column properly)
    # First, combine date and time columns if they're separate
    if 'date' in df.columns and 'time' in df.columns:
        df['booking_time'] = pd.to_datetime(df['date'] + ' ' + df['time'])
    elif 'booking_time' in df.columns:
        # If there's already a booking_time column, convert it
        df['booking_time'] = pd.to_datetime(df['booking_time'], errors='coerce')
    else:
        # Try to find datetime columns
        datetime_cols = [col for col in df.columns if 'date' in col or 'time' in col]
        if datetime_cols:
            df['booking_time'] = pd.to_datetime(df[datetime_cols[0]], errors='coerce')
    
    # Remove quotes from string columns
    string_cols = df.select_dtypes(include=['object']).columns
    for col in string_cols:
        df[col] = df[col].astype(str).str.replace('"', '')
    
    # Handle missing values more intelligently
    print("\nMissing values per column:")
    print(df.isnull().sum())
    
    # Create a copy before dropping rows for analysis
    original_count = len(df)
    
    # Only drop rows where booking_time is null (critical for analysis)
    df_clean = df.dropna(subset=['booking_time']).copy()
    
    # For other columns, we'll handle missing values based on column type
    # Numeric columns: fill with median or 0
    numeric_cols = df_clean.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        if df_clean[col].isnull().any():
            df_clean[col] = df_clean[col].fillna(df_clean[col].median() if df_clean[col].notna().sum() > 0 else 0)
    
    # Categorical columns: fill with mode or 'Unknown'
    categorical_cols = df_clean.select_dtypes(include=['object']).columns
    for col in categorical_cols:
        if df_clean[col].isnull().any() and col != 'booking_time':
            mode_val = df_clean[col].mode()[0] if not df_clean[col].mode().empty else 'Unknown'
            df_clean[col] = df_clean[col].fillna(mode_val)
    
    # Extract datetime features
    df_clean['date'] = df_clean['booking_time'].dt.date
    df_clean['hour'] = df_clean['booking_time'].dt.hour
    df_clean['weekday'] = df_clean['booking_time'].dt.weekday
    df_clean['month'] = df_clean['booking_time'].dt.month
    df_clean['year'] = df_clean['booking_time'].dt.year
    df_clean['day_of_month'] = df_clean['booking_time'].dt.day
    
    # Create time of day categories
    def get_time_of_day(hour):
        if 5 <= hour < 12:
            return 'Morning'
        elif 12 <= hour < 17:
            return 'Afternoon'
        elif 17 <= hour < 21:
            return 'Evening'
        else:
            return 'Night'
    
    df_clean['time_of_day'] = df_clean['hour'].apply(get_time_of_day)
    
    # Convert weekday number to name
    weekday_map = {
        0: 'Monday',
        1: 'Tuesday',
        2: 'Wednesday',
        3: 'Thursday',
        4: 'Friday',
        5: 'Saturday',
        6: 'Sunday'
    }
    df_clean['weekday_name'] = df_clean['weekday'].map(weekday_map)
    
    # Clean numeric columns - convert to appropriate types
    # Handle ride distance - ensure it's numeric
    if 'ride_distance' in df_clean.columns:
        df_clean['ride_distance'] = pd.to_numeric(df_clean['ride_distance'], errors='coerce')
        df_clean['ride_distance'] = df_clean['ride_distance'].fillna(df_clean['ride_distance'].median())
    
    # Handle booking value - ensure it's numeric
    if 'booking_value' in df_clean.columns:
        df_clean['booking_value'] = pd.to_numeric(df_clean['booking_value'], errors='coerce')
        df_clean['booking_value'] = df_clean['booking_value'].fillna(df_clean['booking_value'].median())
    
    # Clean ratings - ensure they're numeric
    rating_cols = [col for col in df_clean.columns if 'rating' in col.lower()]
    for col in rating_cols:
        df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
        df_clean[col] = df_clean[col].fillna(df_clean[col].median())
    
    print(f"\nData cleaning summary:")
    print(f"Original rows: {original_count}")
    print(f"Cleaned rows: {len(df_clean)}")
    print(f"Rows removed: {original_count - len(df_clean)}")
    print(f"\nCleaned dataset shape: {df_clean.shape}")
    
    return df_clean

def analyze_data(df):
    """
    Perform basic analysis on the cleaned data
    """
    print("\n" + "="*50)
    print("DATA ANALYSIS")
    print("="*50)
    
    # Booking status distribution
    if 'booking_status' in df.columns:
        print("\nBooking Status Distribution:")
        print(df['booking_status'].value_counts())
        print(f"\nCompletion Rate: {(df['booking_status'] == 'Completed').sum() / len(df) * 100:.2f}%")
    
    # Vehicle type distribution
    if 'vehicle_type' in df.columns:
        print("\nVehicle Type Distribution:")
        print(df['vehicle_type'].value_counts())
    
    # Time patterns
    print("\nBookings by Hour of Day:")
    print(df['hour'].value_counts().sort_index())
    
    print("\nBookings by Weekday:")
    print(df['weekday_name'].value_counts().reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']))
    
    # Payment method analysis
    if 'payment_method' in df.columns:
        print("\nPayment Method Distribution:")
        print(df['payment_method'].value_counts())
    
    # Basic statistics for numeric columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 0:
        print("\nBasic Statistics for Numeric Columns:")
        print(df[numeric_cols].describe())

if __name__ == "__main__":
    # Load and clean the data
    df = load_and_clean_data("UberAI/Dataset/ncr_ride_bookings.csv")
    
    # Perform basic analysis
    analyze_data(df)
    
    # Save cleaned data
    output_path = "UberAI/Dataset/cleaned_data.csv"
    df.to_csv(output_path, index=False)
    print(f"\nCleaned data saved to: {output_path}")
    
    # Save a summary file
    summary_path = "UberAI/Dataset/data_summary.txt"
    with open(summary_path, 'w') as f:
        f.write(f"Dataset Summary\n")
        f.write(f"Total records: {len(df)}\n")
        f.write(f"Date range: {df['date'].min()} to {df['date'].max()}\n")
        f.write(f"Columns: {', '.join(df.columns.tolist())}\n")
    
    print(f"Summary saved to: {summary_path}")


