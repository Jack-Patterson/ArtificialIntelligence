import os

import joblib
import numpy as np
import pandas as pd

os.environ['LOKY_MAX_CPU_COUNT'] = '4'
from sklearn.cluster import KMeans
import folium

from Final.DataCleaner import DataCleaner

if __name__ == '__main__':
    # input_csv = 'Data/operations.csv'
    # output_csv = 'Data/operations_cleaned.csv'
    #
    # dc = DataCleaner(input_csv, output_csv)
    #
    # data, header = dc.open_file()
    # data = dc.remove_row_if_attacking_country_empty(data)
    # data = dc.get_data_with_european_locations(data)
    # data, header = dc.remove_irrelevant_data(data, header)
    # dc.save_cleaned_data(data, header)
    #
    # for i in range(14):
    #     print(data[i])

    # Load datasets
    dataset1_path = 'Data/operations_cleaned.csv'
    dataset2_path = 'Data/worldcitiespop.csv'

    dataset1 = pd.read_csv(dataset1_path)
    dataset2 = pd.read_csv(dataset2_path)

    # Preprocess (if necessary, e.g., removing NaN values)
    dataset1.dropna(subset=['Target Latitude', 'Target Longitude'], inplace=True)
    dataset2.dropna(subset=['Latitude', 'Longitude'], inplace=True)

    # For the purpose of clustering, we'll use only the latitude and longitude
    locations1 = dataset1[['Target Latitude', 'Target Longitude']]
    locations2 = dataset2[['Latitude', 'Longitude']]

    n_clusters = locations1.drop_duplicates().shape[0]

    # Perform KMeans clustering on the second dataset
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, verbose=2)
    kmeans.fit(locations2)

    joblib.dump(kmeans, 'kmeans_model.pkl')
    print("Model saved to 'kmeans_model.pkl'.")

    # The centroids can be considered as the linked locations in the second dataset
    # centroids = kmeans.cluster_centers_
    closest_centroids = kmeans.predict(locations1)

    lat_min, lat_max = 12.0, 72.0
    lon_min, lon_max = -25.0, 60.0

    # Filter centroids to those within EMEA
    centroids = kmeans.cluster_centers_[closest_centroids]
    centroids_filtered = np.array([c for c in centroids if lat_min <= c[0] <= lat_max and lon_min <= c[1] <= lon_max])

    map_emea = folium.Map(location=[34.0, 9.0], zoom_start=3)

    # Add markers for the filtered centroids
    for lat, lon in centroids_filtered:
        folium.Marker([lat, lon]).add_to(map_emea)

    # Save or display the map
    map_emea.save('Data/emea_matched_locations_map.html')

    # # Initialize a map centered around Europe/MENA
    # m = folium.Map(location=[34.0, 9.0], zoom_start=3)
    #
    # # Add markers for centroids
    # for lat, lon in centroids:
    #     folium.Marker([lat, lon]).add_to(m)
    #
    # # Save to an HTML file
    # m.save('Data/linked_locations_map.html')

    #load trained file
    # kmeans_loaded = joblib.load('Data/kmeans_model.pkl')
    # print("Model loaded.")

# 75341
# 3173958
