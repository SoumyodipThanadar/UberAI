# import pandas as pd

# def growth_index(df):
#     zone_growth = df.groupby('pickup_zone').size().reset_index(name='rides')
#     zone_growth['growth_index'] = zone_growth['rides'] / zone_growth['rides'].max()
#     return zone_growth

# if __name__ == "__main__":
#     df = pd.read_csv("Dataset/cleaned_data.csv")
#     growth = growth_index(df)
#     growth.to_csv("Dataset/growth_index.csv", index=False)

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns

def calculate_growth_index(df):
    """
    Calculate comprehensive growth indices for different zones
    """
    # Ensure we have the required date column
    if 'booking_time' not in df.columns and 'date' not in df.columns:
        print("Error: Date/time column not found")
        return None
    
    # Use 'date' column if available, otherwise extract from 'booking_time'
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
    else:
        df['date'] = pd.to_datetime(df['booking_time']).dt.date
        df['date'] = pd.to_datetime(df['date'])
    
    # Determine the pickup zone column name
    zone_col = None
    possible_zone_cols = ['pickup_zone', 'pickup_location', 'pickup_area']
    for col in possible_zone_cols:
        if col in df.columns:
            zone_col = col
            break
    
    if zone_col is None:
        print("Error: No pickup zone/location column found")
        print(f"Available columns: {df.columns.tolist()}")
        return None
    
    print(f"Using '{zone_col}' as zone column")
    print(f"Date range: {df['date'].min()} to {df['date'].max()}")
    
    # Calculate monthly trends
    df['year_month'] = df['date'].dt.to_period('M')
    monthly_data = df.groupby([zone_col, 'year_month']).agg({
        'booking_id': 'count',
        'booking_value': 'sum',
        'ride_distance': 'sum'
    }).reset_index()
    
    monthly_data = monthly_data.rename(columns={
        'booking_id': 'monthly_rides',
        'booking_value': 'monthly_revenue',
        'ride_distance': 'monthly_distance'
    })
    
    # Calculate growth metrics
    zones = monthly_data[zone_col].unique()
    growth_metrics = []
    
    for zone in zones:
        zone_data = monthly_data[monthly_data[zone_col] == zone].sort_values('year_month')
        
        if len(zone_data) < 2:
            continue  # Need at least 2 months for growth calculation
        
        # Basic metrics
        total_rides = zone_data['monthly_rides'].sum()
        total_revenue = zone_data['monthly_revenue'].sum()
        
        # Growth rates (month-over-month)
        zone_data['ride_growth_rate'] = zone_data['monthly_rides'].pct_change() * 100
        zone_data['revenue_growth_rate'] = zone_data['monthly_revenue'].pct_change() * 100
        
        # Average growth rates
        avg_ride_growth = zone_data['ride_growth_rate'].mean()
        avg_revenue_growth = zone_data['revenue_growth_rate'].mean()
        
        # Consistency (standard deviation of growth)
        ride_growth_std = zone_data['ride_growth_rate'].std()
        revenue_growth_std = zone_data['revenue_growth_rate'].std()
        
        # Recent growth (last month vs previous month)
        if len(zone_data) >= 2:
            recent_ride_growth = zone_data['ride_growth_rate'].iloc[-1]
            recent_revenue_growth = zone_data['revenue_growth_rate'].iloc[-1]
        else:
            recent_ride_growth = np.nan
            recent_revenue_growth = np.nan
        
        # Trend direction (positive/negative growth months)
        positive_growth_months = (zone_data['ride_growth_rate'] > 0).sum()
        total_months = len(zone_data) - 1  # Exclude first month (no growth rate)
        growth_consistency = positive_growth_months / total_months if total_months > 0 else 0
        
        # Market share metrics
        overall_total_rides = monthly_data['monthly_rides'].sum()
        market_share = (total_rides / overall_total_rides) * 100
        
        # Compile metrics
        growth_metrics.append({
            'zone': zone,
            'total_rides': total_rides,
            'total_revenue': total_revenue,
            'avg_monthly_rides': zone_data['monthly_rides'].mean(),
            'avg_monthly_revenue': zone_data['monthly_revenue'].mean(),
            'avg_ride_growth_rate': avg_ride_growth,
            'avg_revenue_growth_rate': avg_revenue_growth,
            'recent_ride_growth_rate': recent_ride_growth,
            'recent_revenue_growth_rate': recent_revenue_growth,
            'ride_growth_volatility': ride_growth_std,
            'revenue_growth_volatility': revenue_growth_std,
            'growth_consistency': growth_consistency,
            'market_share_percent': market_share,
            'data_months': len(zone_data)
        })
    
    # Create growth metrics DataFrame
    growth_df = pd.DataFrame(growth_metrics)
    
    if growth_df.empty:
        print("Error: No growth metrics calculated")
        return None
    
    # Calculate growth indices
    # 1. Volume Index (based on total rides)
    growth_df['volume_index'] = (growth_df['total_rides'] / growth_df['total_rides'].max()) * 100
    
    # 2. Growth Rate Index (combination of avg and recent growth)
    growth_df['normalized_avg_growth'] = (growth_df['avg_ride_growth_rate'] - growth_df['avg_ride_growth_rate'].min()) / \
                                        (growth_df['avg_ride_growth_rate'].max() - growth_df['avg_ride_growth_rate'].min())
    growth_df['normalized_recent_growth'] = (growth_df['recent_ride_growth_rate'] - growth_df['recent_ride_growth_rate'].min()) / \
                                          (growth_df['recent_ride_growth_rate'].max() - growth_df['recent_ride_growth_rate'].min())
    
    # Fill NaN values with 0.5 (neutral)
    growth_df['normalized_avg_growth'] = growth_df['normalized_avg_growth'].fillna(0.5)
    growth_df['normalized_recent_growth'] = growth_df['normalized_recent_growth'].fillna(0.5)
    
    # Combined growth index (weighted average)
    growth_df['growth_rate_index'] = (growth_df['normalized_avg_growth'] * 0.6 + 
                                     growth_df['normalized_recent_growth'] * 0.4) * 100
    
    # 3. Consistency Index (lower volatility, higher consistency = better)
    growth_df['normalized_volatility'] = 1 - (growth_df['ride_growth_volatility'] / 
                                             growth_df['ride_growth_volatility'].max())
    growth_df['consistency_index'] = (growth_df['normalized_volatility'] * 0.7 + 
                                     growth_df['growth_consistency'] * 0.3) * 100
    
    # 4. Overall Growth Index (weighted combination)
    growth_df['overall_growth_index'] = (
        growth_df['volume_index'] * 0.3 +      # Current volume (30%)
        growth_df['growth_rate_index'] * 0.4 + # Growth rate (40%)
        growth_df['consistency_index'] * 0.3    # Consistency (30%)
    )
    
    # Add rankings
    growth_df['volume_rank'] = growth_df['volume_index'].rank(ascending=False, method='min')
    growth_df['growth_rank'] = growth_df['growth_rate_index'].rank(ascending=False, method='min')
    growth_df['consistency_rank'] = growth_df['consistency_index'].rank(ascending=False, method='min')
    growth_df['overall_rank'] = growth_df['overall_growth_index'].rank(ascending=False, method='min')
    
    # Add growth category
    def categorize_growth(overall_index):
        if overall_index >= 80:
            return 'High Growth'
        elif overall_index >= 60:
            return 'Medium Growth'
        elif overall_index >= 40:
            return 'Stable'
        elif overall_index >= 20:
            return 'Declining'
        else:
            return 'Low Activity'
    
    growth_df['growth_category'] = growth_df['overall_growth_index'].apply(categorize_growth)
    
    # Sort by overall growth index
    growth_df = growth_df.sort_values('overall_growth_index', ascending=False).reset_index(drop=True)
    
    return growth_df

def visualize_growth_analysis(growth_df, top_n=20):
    """
    Create visualizations for growth analysis
    """
    if growth_df is None or len(growth_df) == 0:
        print("No data to visualize")
        return
    
    plt.figure(figsize=(15, 10))
    
    # 1. Top zones by overall growth index
    plt.subplot(2, 2, 1)
    top_zones = growth_df.head(top_n)
    colors = plt.cm.viridis(np.linspace(0.2, 0.8, len(top_zones)))
    bars = plt.barh(top_zones['zone'], top_zones['overall_growth_index'], color=colors)
    plt.xlabel('Overall Growth Index')
    plt.title(f'Top {top_n} Zones by Growth Index')
    plt.gca().invert_yaxis()
    
    # Add value labels
    for bar in bars:
        width = bar.get_width()
        plt.text(width, bar.get_y() + bar.get_height()/2, 
                f'{width:.1f}', ha='left', va='center')
    
    # 2. Growth categories distribution
    plt.subplot(2, 2, 2)
    category_counts = growth_df['growth_category'].value_counts()
    plt.pie(category_counts.values, labels=category_counts.index, autopct='%1.1f%%')
    plt.title('Distribution of Growth Categories')
    
    # 3. Scatter plot: Volume vs Growth Rate
    plt.subplot(2, 2, 3)
    scatter = plt.scatter(growth_df['volume_index'], growth_df['growth_rate_index'],
                         c=growth_df['overall_growth_index'], cmap='viridis', alpha=0.6)
    plt.colorbar(scatter, label='Overall Growth Index')
    plt.xlabel('Volume Index')
    plt.ylabel('Growth Rate Index')
    plt.title('Volume vs Growth Rate (Color: Overall Index)')
    
    # Add quadrant lines
    plt.axhline(y=50, color='gray', linestyle='--', alpha=0.5)
    plt.axvline(x=50, color='gray', linestyle='--', alpha=0.5)
    
    # 4. Top zones by recent growth
    plt.subplot(2, 2, 4)
    top_recent = growth_df.nlargest(10, 'recent_ride_growth_rate')
    plt.barh(top_recent['zone'], top_recent['recent_ride_growth_rate'], color='skyblue')
    plt.xlabel('Recent Growth Rate (%)')
    plt.title('Top Zones by Recent Growth Rate')
    plt.gca().invert_yaxis()
    
    plt.tight_layout()
    plt.savefig('UberAI/Dataset/growth_analysis_visualization.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"Visualization saved to: UberAI/Dataset/growth_analysis_visualization.png")

def generate_growth_recommendations(growth_df):
    """
    Generate actionable recommendations based on growth analysis
    """
    if growth_df is None or len(growth_df) == 0:
        print("No data for recommendations")
        return
    
    print("\n" + "="*60)
    print("GROWTH ANALYSIS RECOMMENDATIONS")
    print("="*60)
    
    # Identify top performers
    top_growth = growth_df[growth_df['growth_category'] == 'High Growth']
    medium_growth = growth_df[growth_df['growth_category'] == 'Medium Growth']
    stable_zones = growth_df[growth_df['growth_category'] == 'Stable']
    declining_zones = growth_df[growth_df['growth_category'] == 'Declining']
    
    # Recommendations for each category
    print(f"\n1. HIGH GROWTH ZONES ({len(top_growth)} zones):")
    if not top_growth.empty:
        print("   - Double down on successful strategies")
        print("   - Consider adding more capacity")
        print("   - Monitor for market saturation")
        print("   - Top zones:", ", ".join(top_growth['zone'].head(5).tolist()))
    
    print(f"\n2. MEDIUM GROWTH ZONES ({len(medium_growth)} zones):")
    if not medium_growth.empty:
        print("   - Analyze what's working in high-growth zones")
        print("   - Test promotional offers")
        print("   - Improve service quality")
    
    print(f"\n3. STABLE ZONES ({len(stable_zones)} zones):")
    if not stable_zones.empty:
        print("   - Maintain current operations")
        print("   - Look for incremental improvements")
        print("   - Consider loyalty programs")
    
    print(f"\n4. DECLINING ZONES ({len(declining_zones)} zones):")
    if not declining_zones.empty:
        print("   - Investigate reasons for decline")
        print("   - Consider targeted promotions")
        print("   - Assess competitive landscape")
        if not declining_zones.empty:
            print("   - Priority zones to investigate:", 
                  ", ".join(declining_zones.nlargest(3, 'volume_index')['zone'].tolist()))
    
    # Special recommendations
    print("\n5. SPECIAL OPPORTUNITIES:")
    
    # High volume but low growth (mature markets)
    high_volume_low_growth = growth_df[
        (growth_df['volume_index'] > 70) & 
        (growth_df['growth_rate_index'] < 40)
    ]
    if not high_volume_low_growth.empty:
        print(f"   - {len(high_volume_low_growth)} mature markets with slowing growth")
        print("     Consider: Market penetration strategies, upselling, cross-selling")
    
    # Low volume but high growth (emerging markets)
    low_volume_high_growth = growth_df[
        (growth_df['volume_index'] < 30) & 
        (growth_df['growth_rate_index'] > 70)
    ]
    if not low_volume_high_growth.empty:
        print(f"   - {len(low_volume_high_growth)} emerging markets with high growth")
        print("     Consider: Scaling operations, market education, partnerships")
    
    # High growth volatility (risky markets)
    high_volatility = growth_df[growth_df['ride_growth_volatility'] > growth_df['ride_growth_volatility'].median()]
    if not high_volatility.empty:
        print(f"   - {len(high_volatility)} zones with high growth volatility")
        print("     Consider: Risk mitigation, diversified strategies")

if __name__ == "__main__":
    try:
        # Load the cleaned data
        file_path = "UberAI/Dataset/cleaned_data.csv"
        print(f"Loading data from: {file_path}")
        
        df = pd.read_csv(file_path)
        print(f"Data loaded successfully. Shape: {df.shape}")
        print(f"Columns: {df.columns.tolist()}")
        
        # Calculate growth indices
        growth_df = calculate_growth_index(df)
        
        if growth_df is not None:
            # Save the growth analysis
            output_path = "UberAI/Dataset/growth_index.csv"
            growth_df.to_csv(output_path, index=False)
            print(f"\nGrowth analysis saved to: {output_path}")
            
            # Print summary
            print(f"\nGrowth Analysis Summary:")
            print(f"Total zones analyzed: {len(growth_df)}")
            print(f"\nGrowth Categories Distribution:")
            print(growth_df['growth_category'].value_counts())
            
            print(f"\nTop 10 Zones by Growth Index:")
            top_10 = growth_df.head(10)
            for idx, row in top_10.iterrows():
                print(f"{idx+1}. {row['zone']}: {row['overall_growth_index']:.1f} "
                      f"({row['growth_category']})")
            
            # Create visualizations
            visualize_growth_analysis(growth_df)
            
            # Generate recommendations
            generate_growth_recommendations(growth_df)
            
            # Save a simplified version for dashboard use
            simplified_df = growth_df[[
                'zone', 'total_rides', 'total_revenue', 'avg_ride_growth_rate',
                'recent_ride_growth_rate', 'overall_growth_index', 'growth_category',
                'volume_rank', 'growth_rank', 'overall_rank'
            ]]
            simplified_path = "UberAI/Dataset/simplified_growth_index.csv"
            simplified_df.to_csv(simplified_path, index=False)
            print(f"\nSimplified growth index saved to: {simplified_path}")
            
        else:
            print("Failed to calculate growth indices. Check the data format.")
            
    except FileNotFoundError as e:
        print(f"Error: File not found at path: {file_path}")
        print("Please ensure the cleaned_data.csv file exists.")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
