import csv
import os

import folium
import joblib
import numpy as np
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans

from Final.DataCleaner import DataCleaner

os.environ['LOKY_MAX_CPU_COUNT'] = '4'


def main():
    should_load_kmeans = True
    clusters_count = 1000
    bombing_dataset_name = 'Data/DataSets/operations_cleaned.csv'
    world_locations_dataset_name = 'Data/DataSets/emea_locations.csv'
    europe_cities_dataset_name = 'Data/DataSets/europe_locations_pop_greater_1000.csv'
    kmeans_model_name = f'Data/kmeans_bombing_model_clusters_{clusters_count}.pkl'
    scatter_diagram_name = f'Data/Images/bombing_scatter_clusters_{clusters_count}.png'
    map_name = f'Data/Images/map_of_locations_clusters_{clusters_count}.html'

    print('Cleaning original csv files.')
    clean_bombing_operations()
    # clean_world_locations()

    print('Loading the files into memory and filtering for relevant rows.')
    _, bombing_locations_full = load_file(bombing_dataset_name)
    _, world_locations_full = load_file(world_locations_dataset_name)
    _, europe_cities_full = load_file(europe_cities_dataset_name)

    bombing_locations = filter_for_latitude_and_longitude(bombing_locations_full, 4, 5)
    world_locations = filter_for_latitude_and_longitude(world_locations_full, 3, 4)
    europe_cities = split_and_filter_for_latitude_and_longitude(europe_cities_full, 19, ', ')

    print('Beginning KMeans.')
    bombings_per_centroid_threshold = 10

    if should_load_kmeans:
        kmeans = joblib.load(kmeans_model_name)
    else:
        kmeans = cluster_and_fit_data(world_locations, clusters_count)

    print("Fitting bombing locations to a world location.")
    nearest_locations_indices = kmeans.predict(bombing_locations)

    print(
        f'Filtering cluster locations to only include ones that have more bombings than '
        f'{bombings_per_centroid_threshold}.')
    significant_centroids = filter_significant_centroids(kmeans, nearest_locations_indices,
                                                         bombings_per_centroid_threshold)

    if not should_load_kmeans:
        print(f'Saving KMeans model to {kmeans_model_name}.')
        save_kmeans_model(kmeans, kmeans_model_name)
    print('Ending KMeans.')

    print('Beginning display data.')
    print('Rounding for significant centroids.')
    unique_significant_centroids = round_significant_centroids(significant_centroids)

    print("Finding closest world locations to centroids.")
    closest_locations = find_closest_world_locations(unique_significant_centroids, europe_cities_full)

    print("Saving closest locations to CSV.")
    closest_locations_csv_name = f'Data/Closest_Locations_to_Centroids_{clusters_count}.csv'
    save_closest_locations_to_csv(closest_locations, closest_locations_csv_name)

    print('Plotting on scatter diagram.')
    plot_and_save_on_scatter_diagram(unique_significant_centroids, scatter_diagram_name)

    print("Plotting on map.")
    plot_and_save_on_map(unique_significant_centroids, map_name)


def clean_bombing_operations(input_name='Data/DataSets/operations.csv',
                             output_name='Data/DataSets/operations_cleaned.csv'):
    """
    Cleans the original bombing dataset and removes all irrelevant data before outputting the cleaned data into a new
    csv file. Limits the data to Europe, Middle East and North Africa.
    Args:
        input_name: Name of the original file.
        output_name: Name of the new file.

    """
    emea_countries_in_dataset = ['POLAND', 'AUSTRIA', 'YUGOSLAVIA', 'ITALY', 'SICILY', 'BULGARIA', 'FRANCE',
                                 'GREAT BRITAIN', 'PANTELLARIA', 'SARDINIA', 'ALGERIA', 'ROMANIA',
                                 'HOLLAND OR NETHERLANDS', 'GERMANY', 'ALBANIA', 'LUXEMBOURG', 'CYPRUS', 'CRETE',
                                 'DENMARK', 'HUNGARY', 'CORSICA', 'SWITZERLAND', 'NORWAY', 'BELGIUM', 'GREECE',
                                 'CZECHOSLOVAKIA']
    rows_and_headers_to_keep = [1, 3, 14, 15, 19, 20]

    data_cleaner = DataCleaner(input_name, output_name)
    data_cleaner.remove_if_row_empty(3)
    data_cleaner.remove_if_row_empty(19)
    data_cleaner.remove_if_row_empty(20)
    data_cleaner.filter_for_locations(14, emea_countries_in_dataset)
    data_cleaner.remove_irrelevant_data(rows_and_headers_to_keep)
    data_cleaner.remove_all_over_threshold(5, 80)
    data_cleaner.save()


def clean_world_locations(input_name='Data/DataSets/world_locations.csv',
                          output_name='Data/DataSets/emea_locations.csv'):
    """
    Cleans the original locations dataset and removes all irrelevant data before outputting the cleaned data into a new
    csv file. Limits the data to Europe, Middle East and North Africa.
    Args:
        input_name: Name of the original file.
        output_name: Name of the new file.

    """
    emea_county_codes_in_dataset = ['lt', 'al', 'mt', 'ly', 'cz', 'dz', 'ch', 'hr', 'ad', 'pl', 'ro', 'by', 'is', 'cy',
                                    'lu', 'at', 'sk', 'gb', 'me', 'be', 'ru', 'eh', 'fr', 'gr', 'ee', 'pt', 'ua', 'mk',
                                    'se', 'bg', 'sm', 'de', 'es', 'ba', 'rs', 'eg', 'ie', 'hu', 'tn', 'li', 'ma', 'mc',
                                    'md', 'si', 'fi', 'it', 'no', 'nl', 'lv', 'dk']
    rows_and_headers_to_keep = [0, 1, 2, 5, 6]

    data_cleaner = DataCleaner(input_name, output_name)
    data_cleaner.filter_for_locations(0, emea_county_codes_in_dataset)
    data_cleaner.remove_irrelevant_data(rows_and_headers_to_keep)
    data_cleaner.save()


def load_file(file_name):
    """
    Opens a csv file.
    Args:
        file_name: Name of the file.

    Returns: The header and the rows.

    """
    with open(file_name, mode='r', newline='', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        header = next(reader)
        rows = [row for row in reader]

    return header, rows


def filter_for_latitude_and_longitude(data, latitude_index, longitude_index):
    """
    Filters the data and only gets the latitude and longitude data.
    Args:
        data: Raw data from the csv.
        latitude_index: Index of the row for latitude.
        longitude_index: Index of the row for longitude.

    Returns: Numpy array of latitude and longitudes.

    """
    return np.array([[row[latitude_index], row[longitude_index]] for row in data])


def split_and_filter_for_latitude_and_longitude(data, index, split_value):
    """
    Filters the data and only gets the latitude and longitude data.
    Args:
        data: Raw data from the csv.
        index: Index of the row.
        split_value: Value to split the index by.

    Returns: Numpy array of latitude and longitudes.

    """
    return np.array([[row[index].split(split_value)[0], row[index].split(split_value)[1]] for row in data])


def cluster_and_fit_data(data, number_clusters):
    """
    Clusters the data and fits the world locations dataset to it.
    Args:
        data: World location dataset.
        number_clusters: Number of clusters.

    Returns: KMeans object.

    """
    return KMeans(n_clusters=number_clusters, n_init=10).fit(data)


def filter_significant_centroids(kmeans, nearest_locations_indices,
                                 bombings_per_centroid_threshold=10):
    """
    Filters the centroids from the kmeans and excludes any that have less bombings fitted to than the threshold.
    Args:
        kmeans: KMeans object.
        nearest_locations_indices: Indices of the nearest locations of the bombings
        bombings_per_centroid_threshold: Threshold of how many bombings have to have been fit to the centroid to not
        be excluded.

    Returns: The significant clusters that have the necessary bombings in it.

    """

    bombings_per_centroid = np.bincount(nearest_locations_indices)
    significant_centroids_indices = np.where(bombings_per_centroid > bombings_per_centroid_threshold)[0]
    significant_centroids = kmeans.cluster_centers_[significant_centroids_indices]

    return significant_centroids


def round_significant_centroids(centroids):
    """
    Used for processing on the graphs. Gets only one value for each centroid to avoid duplication for the graphs.
    Prevents delays on the map. Credit: ChatGPT, I couldn't figure out how to do it the best.
    Args:
        centroids: Centroids from KMeans.

    Returns: List of unique centroids.

    """
    rounded_significant_centroids = np.round(centroids, decimals=5)
    dtype = np.dtype(','.join(['f8'] * rounded_significant_centroids.shape[1]))
    _, unique_indices = np.unique(rounded_significant_centroids.view(dtype), return_index=True, axis=0)
    unique_significant_centroids = centroids[unique_indices]

    return unique_significant_centroids


def save_kmeans_model(kmeans, name):
    """
    Saves the model to a file.
    Args:
        kmeans: KMeans object.
        name: File path to save location.

    """
    joblib.dump(kmeans, name)


def plot_and_save_on_scatter_diagram(centroids, file_name):
    """
    Plots the KMeans data on a scatter diagram.
    Args:
        centroids: Data to plot.
        file_name: File path to save location.


    """
    latitude = centroids[:, 0]
    longitude = centroids[:, 1]

    plt.scatter(longitude, latitude)
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Geographical Scatter Plot')

    print(f"Saving diagram to {file_name}")
    plt.savefig(file_name)
    plt.close()


def plot_and_save_on_map(centroids, file_name):
    """
    Plots the KMeans data on a map of Europe.
    Args:
        centroids: Data to plot.
        file_name: File path to save location.

    """
    map_center = np.mean(centroids, axis=0)

    map = folium.Map(location=map_center, zoom_start=4)

    for location in centroids:
        folium.Marker([location[0], location[1]]).add_to(map)

    print(f"Saving map to {file_name}")
    map.save(file_name)


def find_closest_world_locations(centroids, world_locations):
    """
    Finds the closest world location to each centroid.

    Args:
        centroids: The centroids from KMeans.
        world_locations: The world locations to compare against.

    Returns:
        A list of tuples containing the centroid and its closest world location.
    """
    closest_locations = []
    for centroid in centroids:
        closest_location = min(world_locations,
                               key=lambda loc: np.linalg.norm(
                                   centroid - np.array([float(loc[19].split(', ')[0]), float(loc[19].split(', ')[1])])))
        closest_locations.append((centroid, closest_location))
    return closest_locations


def save_closest_locations_to_csv(closest_locations, file_name):
    """
    Saves the closest world locations to each centroid to a CSV file.

    Args:
        closest_locations: A list of tuples containing the centroid and its closest world location.
        file_name: The name of the file to save the data.
    """
    with open(file_name, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Centroid Latitude', 'Centroid Longitude', 'Name', 'Country Name', 'Closest Location Latitude',
                         'Closest Location Longitude'])
        for centroid, location in closest_locations:
            writer.writerow([centroid[0], centroid[1], location[2], location[7], location[19].split(', ')])


if __name__ == '__main__':
    main()
