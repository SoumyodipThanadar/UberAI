import pandas as pd
from sklearn.cluster import KMeans

def cluster_zones(df):
    zone_data = df.groupby('pickup_zone').size().reset_index(name='rides')

    kmeans = KMeans(n_clusters=3, random_state=42)
    zone_data['cluster'] = kmeans.fit_predict(zone_data[['rides']])

    return zone_data

if __name__ == "__main__":
    df = pd.read_csv("Dataset/cleaned_data.csv")
    zones = cluster_zones(df)
    zones.to_csv("Dataset/zone_clusters.csv", index=False)

