import csv
import os

import folium
import joblib
import numpy as np
from geopy.distance import geodesic
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans

from DataCleaner import DataCleaner

os.environ['LOKY_MAX_CPU_COUNT'] = '4'


def main():
    """

    First, it cleans the data. Next, it loads all the required files into memory. There are 4 csv files, with them being
    the dataset of Allied bombings that happened in europe during WW2, the next is a dataset of every village, town and
    city in Europe. The next is the same, but it only includes locations with a population greater than 1000, and
    finally a dataset of all European capitals.

    Next it creates kmeans for each location in europe and fits the bombings to each of those locations. It then removes
    any that have 10 or fewer bombings that occurred there. It then links them to either the closest significant
    location (pop > 1000) or the closest capital. The issue is, capitals in the other datasets are split into suburbs,
    so I used another dataset to get the capital locations and if it is within the reasonable distance (I found 35km to
    be the best) it will select that, or else the closest significant location.

    It then saves the results into a csv file, two scatter diagrams and plots them on a map. Each map contains two
    labels for each cluster, with one in blue being the cluster location, and the other in red being the closest
    significant location. Each one contains a label which has an ID to link it to the other, as well as location
    information and how many bombings took place in that location.

    """
    should_load_kmeans = False
    clusters_count = 4000
    bombing_dataset_name = 'Data/DataSets/operations_cleaned.csv'
    world_locations_dataset_name = 'Data/DataSets/emea_locations.csv'
    europe_cities_dataset_name = 'Data/DataSets/europe_locations_pop_greater_1000.csv'
    europe_capitals_dataset_name = 'Data/DataSets/europe_capitals.csv'
    kmeans_model_name = f'Data/kmeans_bombing_model_clusters_{clusters_count}.pkl'
    scatter_centroids_diagram_name = f'Data/Images/bombing_scatter_centroids_clusters_{clusters_count}.png'
    scatter_closest_location_diagram_name = \
        f'Data/Images/bombing_scatter_closest_location_clusters_{clusters_count}.png'
    map_name = f'Data/Images/map_of_locations_clusters_{clusters_count}.html'

    print('Cleaning original csv files.')
    # clean_bombing_operations()
    # clean_world_locations()
    # clean_country_capitals()

    print('Loading the files into memory and filtering for relevant rows.')
    _, bombing_locations_full = load_file(bombing_dataset_name)
    _, world_locations_full = load_file(world_locations_dataset_name)
    _, europe_cities_full = load_file(europe_cities_dataset_name)
    _, europe_capitals_full = load_file(europe_capitals_dataset_name)

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
    unique_significant_centroids = combine_significant_centroids(significant_centroids)

    print("Finding closest world locations to centroids.")
    closest_locations = find_closest_world_locations(unique_significant_centroids, europe_cities_full,
                                                     europe_capitals_full)

    print("Saving closest locations to CSV.")
    closest_locations_csv_name = f'Data/Closest_Locations_to_Centroids_{clusters_count}.csv'
    save_closest_locations_to_csv(closest_locations, closest_locations_csv_name)

    print('Plotting centroids on scatter diagram.')
    centroids_without_count = np.array([centroid[0] for centroid in unique_significant_centroids])
    plot_and_save_on_scatter_diagram(centroids_without_count, scatter_centroids_diagram_name)

    print('Plotting closest locations on scatter diagram.')
    closest_locations_lat_long = filter_for_latitude_and_longitude_with_additional_index(closest_locations, 1, 2, 3)
    plot_and_save_on_scatter_diagram(closest_locations_lat_long, scatter_closest_location_diagram_name)

    plot_and_save_on_map(closest_locations, map_name)


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
                                 'GREAT BRITAIN', 'PANTELLARIA', 'SARDINIA', 'ROMANIA', 'HOLLAND OR NETHERLANDS',
                                 'GERMANY', 'ALBANIA', 'LUXEMBOURG', 'CYPRUS', 'CRETE', 'DENMARK', 'HUNGARY', 'CORSICA',
                                 'SWITZERLAND', 'NORWAY', 'BELGIUM', 'GREECE', 'CZECHOSLOVAKIA']
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
    emea_county_codes_in_dataset = ['lt', 'al', 'mt', 'cz', 'ch', 'hr', 'ad', 'pl', 'ro', 'by', 'is', 'cy', 'lu', 'at',
                                    'sk', 'gb', 'me', 'be', 'ru', 'fr', 'gr', 'ee', 'pt', 'ua', 'mk', 'se', 'bg', 'sm',
                                    'de', 'es', 'ba', 'rs', 'ie', 'hu', 'li', 'mc', 'md', 'si', 'fi', 'it', 'no', 'nl',
                                    'lv', 'dk']

    rows_and_headers_to_keep = [0, 1, 2, 5, 6]

    data_cleaner = DataCleaner(input_name, output_name)
    data_cleaner.filter_for_locations(0, emea_county_codes_in_dataset)
    data_cleaner.remove_irrelevant_data(rows_and_headers_to_keep)
    data_cleaner.save()


def clean_country_capitals(input_name='Data/DataSets/country_capitals.csv',
                           output_name='Data/DataSets/europe_capitals.csv'):
    """
    Cleans the country capitals dataset to only include europe capitals
    Args:
        input_name: Name of the original file.
        output_name:  Name of the new file.

    """
    european_countries = [
        "Albania", "Andorra", "Armenia", "Austria", "Azerbaijan", "Belarus", "Belgium", "Bosnia and Herzegovina",
        "Bulgaria", "Croatia", "Cyprus", "Czechia", "Denmark", "Estonia", "Finland", "France", "Georgia", "Germany",
        "Greece", "Holy See", "Hungary", "Iceland", "Ireland", "Italy", "Kazakhstan", "Latvia", "Liechtenstein",
        "Lithuania", "Luxembourg", "Malta", "Moldova", "Monaco", "Montenegro", "Netherlands", "North Macedonia",
        "Norway", "Poland", "Portugal", "Romania", "Russia", "San Marino", "Serbia", "Slovakia", "Slovenia", "Spain",
        "Sweden", "Switzerland", "Turkey", "Ukraine", "United Kingdom"]

    data_cleaner = DataCleaner(input_name, output_name)
    data_cleaner.filter_for_locations(0, european_countries)
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


def filter_for_latitude_and_longitude_with_additional_index(data, contained_data, latitude_index, longitude_index):
    """
    Filters the data and only gets the latitude and longitude data.
    Args:
        data: Raw data from the csv.
        contained_data: Index of the object within.
        latitude_index: Index of the row for latitude.
        longitude_index: Index of the row for longitude.

    Returns: Numpy array of latitude and longitudes.

    """
    return np.array(
        [[float(row[contained_data][latitude_index]), float(row[contained_data][longitude_index])] for row in data])


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
    significant_centroids = [(kmeans.cluster_centers_[index], bombings_per_centroid[index])
                             for index in significant_centroids_indices]

    return significant_centroids


def combine_significant_centroids(centroids_with_counts):
    """
    Combine the centroid coordinates.
    Args:
        centroids_with_counts: List of tuples with each centroid and the count of bombings.

    Returns: List of unique rounded centroids with associated bombing counts.

    """
    rounded_centroids_with_counts = []
    seen = set()

    for centroid, count in centroids_with_counts:
        rounded_centroid = tuple(np.round(centroid, decimals=5))
        if rounded_centroid not in seen:
            seen.add(rounded_centroid)
            rounded_centroids_with_counts.append((rounded_centroid, count))

    return rounded_centroids_with_counts


def save_kmeans_model(kmeans, name):
    """
    Saves the model to a file.
    Args:
        kmeans: KMeans object.
        name: File path to save location.

    """
    joblib.dump(kmeans, name)


def plot_and_save_on_scatter_diagram(points, file_name):
    """
    Plots the KMeans data on a scatter diagram.
    Args:
        points: Data to plot.
        file_name: File path to save location.


    """
    latitude = points[:, 0]
    longitude = points[:, 1]

    plt.scatter(longitude, latitude)
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Geographical Scatter Plot')

    print(f"Saving diagram to {file_name}")
    plt.savefig(file_name)
    plt.close()


def plot_and_save_on_map(closest_locations, file_name):
    map_center = np.mean([loc[0][:2] for loc in closest_locations], axis=0)
    map = folium.Map(location=map_center, zoom_start=4)

    for i, (centroid, location, count) in enumerate(closest_locations):
        folium.Marker(
            centroid[:2],
            popup=f"Centroid ID: {i}, Bombings Count: {count}<br>Details:<br>Name: {location[0]}, Country: "
                  f"{location[1]}, Lat: {centroid[0]}, Long: {centroid[1]}",
            icon=folium.Icon(color='blue')
        ).add_to(map)
        folium.Marker(
            [float(location[2]), float(location[3])],
            popup=f"Centroid ID: {i}, Closest Location<br>Name: {location[0]}, Country: {location[1]}, Lat: "
                  f"{location[2]}, Long: {location[3]}",
            icon=folium.Icon(color='red')
        ).add_to(map)

    map.save(file_name)


def find_closest_world_locations(centroids, world_locations, capitals, reasonable_distance_km=35):
    """
    Finds the closest world location to each centroid.
    Returns:
        A list of tuples containing the centroid, its closest world location, and bombings count.
    """
    closest_locations = []
    for centroid, count in centroids:
        nearest_capital = min(capitals, key=lambda loc: geodesic(centroid[:2], loc[2:4]).kilometers)
        distance_to_capital = geodesic(centroid[:2], nearest_capital[2:4]).kilometers

        if distance_to_capital <= reasonable_distance_km:
            closest_location = nearest_capital
            location_details = [closest_location[1], closest_location[0], closest_location[2], closest_location[3]]
        else:
            closest_location = min(world_locations,
                                   key=lambda loc: np.linalg.norm(centroid[:2] - np.array(
                                       [float(loc[19].split(', ')[0]), float(loc[19].split(', ')[1])])))
            split_location = closest_location[19].split(', ')
            location_details = [closest_location[2], closest_location[7], split_location[0], split_location[1]]

        closest_locations.append((centroid, location_details, count))
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
                         'Closest Location Longitude', 'Number of Bombing At Location'])
        for centroid, location, bombings_count in closest_locations:
            writer.writerow([centroid[0], centroid[1], location[0], location[1], location[2], location[3],
                             bombings_count])


if __name__ == '__main__':
    main()
