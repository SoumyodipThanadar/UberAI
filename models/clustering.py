# import pandas as pd
# from sklearn.cluster import KMeans

# def cluster_zones(df):
#     zone_data = df.groupby('pickup_zone').size().reset_index(name='rides')

#     kmeans = KMeans(n_clusters=3, random_state=42)
#     zone_data['cluster'] = kmeans.fit_predict(zone_data[['rides']])

#     return zone_data

# if __name__ == "__main__":
#     df = pd.read_csv("pip install clusterDataset/UberAI/Dataset/cleaned_data.csv")
#     zones = cluster_zones(df)
#     zones.to_csv("UberAI/Dataset/zone_clusters.csv", index=False)

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns

def cluster_zones(df):
    """
    Cluster zones based on ride demand patterns
    """
    # Check if the required columns exist
    if 'pickup_location' not in df.columns:
        print("Error: 'pickup_location' column not found in dataset")
        print(f"Available columns: {df.columns.tolist()}")
        return None
    
    # Group by pickup location to get ride counts
    zone_data = df.groupby('pickup_location').agg({
        'booking_id': 'count',  # Number of rides
        'booking_value': 'mean',  # Average booking value
        'ride_distance': 'mean'   # Average ride distance
    }).reset_index()
    
    zone_data = zone_data.rename(columns={
        'booking_id': 'rides',
        'booking_value': 'avg_booking_value',
        'ride_distance': 'avg_ride_distance'
    })
    
    print(f"Found {len(zone_data)} unique pickup locations")
    print(f"Total rides analyzed: {zone_data['rides'].sum()}")
    
    # Prepare features for clustering
    features = ['rides', 'avg_booking_value', 'avg_ride_distance']
    
    # Check if all features exist
    missing_features = [f for f in features if f not in zone_data.columns]
    if missing_features:
        print(f"Warning: Missing features for clustering: {missing_features}")
        # Use only available features
        features = [f for f in features if f not in missing_features]
    
    if len(features) == 0:
        print("Error: No features available for clustering")
        return zone_data
    
    # Normalize the features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(zone_data[features])
    
    # Determine optimal number of clusters using elbow method
    print("\nDetermining optimal number of clusters...")
    inertia = []
    k_range = range(1, min(11, len(zone_data)))  # Up to 10 clusters or n-1
    
    for k in k_range:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        kmeans.fit(X_scaled)
        inertia.append(kmeans.inertia_)
    
    # Plot elbow curve (optional)
    plt.figure(figsize=(10, 6))
    plt.plot(k_range, inertia, 'bo-')
    plt.xlabel('Number of clusters (k)')
    plt.ylabel('Inertia')
    plt.title('Elbow Method for Optimal k')
    plt.savefig('UberAI/Dataset/elbow_curve.png')
    plt.close()
    
    # Use elbow method to determine k (simplified - choose k=3 for low/medium/high)
    # For simplicity, we'll use 3 clusters: Low, Medium, High demand
    optimal_k = 3
    
    # Perform K-means clustering
    kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
    zone_data['cluster'] = kmeans.fit_predict(X_scaled)
    
    # Get cluster centers and map to meaningful labels
    cluster_centers = scaler.inverse_transform(kmeans.cluster_centers_)
    
    # Create cluster labels based on average rides
    cluster_stats = zone_data.groupby('cluster')['rides'].agg(['mean', 'median', 'count']).round(2)
    cluster_stats.columns = ['avg_rides', 'median_rides', 'zone_count']
    
    print("\nCluster Statistics:")
    print(cluster_stats)
    
    # Sort clusters by average rides and assign meaningful labels
    cluster_order = cluster_stats['avg_rides'].sort_values().index
    label_map = {}
    
    if len(cluster_order) == 3:
        label_map = {
            cluster_order[0]: 'Low Demand',
            cluster_order[1]: 'Medium Demand',
            cluster_order[2]: 'High Demand'
        }
    elif len(cluster_order) == 2:
        label_map = {
            cluster_order[0]: 'Low Demand',
            cluster_order[1]: 'High Demand'
        }
    else:
        for i, cluster_id in enumerate(cluster_order):
            label_map[cluster_id] = f'Cluster {i+1}'
    
    zone_data['cluster_label'] = zone_data['cluster'].map(label_map)
    
    # Add cluster characteristics
    for i, center in enumerate(cluster_centers):
        print(f"\nCluster {i} Center (original scale):")
        for j, feature in enumerate(features):
            print(f"  {feature}: {center[j]:.2f}")
    
    # Save visualization of clusters
    if len(features) >= 2:
        plt.figure(figsize=(12, 8))
        scatter = plt.scatter(zone_data[features[0]], 
                            zone_data[features[1]], 
                            c=zone_data['cluster'], 
                            cmap='viridis', 
                            alpha=0.6)
        plt.xlabel(features[0])
        plt.ylabel(features[1])
        plt.title(f'Zone Clusters by {features[0]} vs {features[1]}')
        plt.colorbar(scatter, label='Cluster')
        plt.savefig('UberAI/Dataset/zone_clusters_visualization.png')
        plt.close()
    
    return zone_data

def analyze_clusters(zone_data):
    """
    Analyze and summarize the clusters
    """
    if zone_data is None or 'cluster_label' not in zone_data.columns:
        print("Error: No cluster data to analyze")
        return
    
    print("\n" + "="*60)
    print("CLUSTER ANALYSIS SUMMARY")
    print("="*60)
    
    # Summary by cluster
    cluster_summary = zone_data.groupby('cluster_label').agg({
        'pickup_location': 'count',
        'rides': ['sum', 'mean', 'median'],
        'avg_booking_value': 'mean',
        'avg_ride_distance': 'mean'
    }).round(2)
    
    # Flatten column names
    cluster_summary.columns = ['_'.join(col).strip() for col in cluster_summary.columns.values]
    cluster_summary = cluster_summary.rename(columns={
        'pickup_location_count': 'num_zones',
        'rides_sum': 'total_rides',
        'rides_mean': 'avg_rides_per_zone',
        'rides_median': 'median_rides_per_zone',
        'avg_booking_value_mean': 'avg_booking_value',
        'avg_ride_distance_mean': 'avg_ride_distance'
    })
    
    print("\nCluster Summary:")
    print(cluster_summary)
    
    # Top zones in each cluster
    print("\nTop 5 Zones in Each Cluster:")
    for cluster_label in zone_data['cluster_label'].unique():
        print(f"\n{cluster_label}:")
        top_zones = zone_data[zone_data['cluster_label'] == cluster_label].nlargest(5, 'rides')
        for idx, row in top_zones.iterrows():
            print(f"  {row['pickup_location']}: {row['rides']} rides")
    
    # Recommendations based on clusters
    print("\n" + "="*60)
    print("RECOMMENDATIONS")
    print("="*60)
    
    high_demand_clusters = [label for label in zone_data['cluster_label'].unique() 
                           if 'High' in label]
    
    if high_demand_clusters:
        print("\n1. High Demand Zones (Priority for Investment):")
        high_demand_zones = zone_data[zone_data['cluster_label'].isin(high_demand_clusters)]
        print(f"   - {len(high_demand_zones)} zones identified")
        print(f"   - Consider adding more drivers in these areas")
        print(f"   - Monitor surge pricing opportunities")
    
    low_demand_clusters = [label for label in zone_data['cluster_label'].unique() 
                          if 'Low' in label]
    
    if low_demand_clusters:
        print("\n2. Low Demand Zones (Consider Marketing/Promotions):")
        low_demand_zones = zone_data[zone_data['cluster_label'].isin(low_demand_clusters)]
        print(f"   - {len(low_demand_zones)} zones identified")
        print(f"   - Consider promotional offers to boost demand")
        print(f"   - Analyze reasons for low demand (accessibility, competition, etc.)")

if __name__ == "__main__":
    try:
        # CORRECTED FILE PATH - removed "pip install cluster" from the path
        file_path = "UberAI/Dataset/cleaned_data.csv"
        
        print(f"Loading data from: {file_path}")
        df = pd.read_csv(file_path)
        print(f"Data loaded successfully. Shape: {df.shape}")
        print(f"Columns: {df.columns.tolist()}")
        
        # Cluster the zones
        zones = cluster_zones(df)
        
        if zones is not None:
            # Save the clustered zones
            output_path = "UberAI/Dataset/zone_clusters.csv"
            zones.to_csv(output_path, index=False)
            print(f"\nClustered zones saved to: {output_path}")
            
            # Analyze the clusters
            analyze_clusters(zones)
            
            # Print sample of the clustered data
            print("\n" + "="*60)
            print("SAMPLE OF CLUSTERED DATA")
            print("="*60)
            print(zones.head(10))
        else:
            print("Failed to cluster zones. Check the error messages above.")
            
    except FileNotFoundError as e:
        print(f"Error: File not found at path: {file_path}")
        print("Please check the file path and ensure the file exists.")
        print(f"Current working directory: {os.getcwd()}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        import traceback
        traceback.print_exc()

