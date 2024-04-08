import csv

import folium
import joblib
import numpy as np
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans

# bombing_locations = np.array([
#     [38.22, 15.37],  # SPADAFORA
#     [39.27, 16.25],  # COSENZA
#     [38.43, 15.9],  # GIOJA TAURO
#     [38.23, 15.72],  # SCILLA
#     [52.53, 13.42],  # BERLIN
#     [51.22, 6.78],  # DUSSELDORF
#     [38.08, 14.63],  # AGATA
#     [38.18, 15.57],  # MESSINA
#     [40.07, 15.63]  # SAPRI
# ])
#
# # world_locations = np.array([
# #     [53.6166667, -9.6666667],  # Aasleagh
# #     [51.9666667, -8.5833333],  # Abbevill
# #     [52.35, -9.6833333],  # Abbeydorney
# #     [52.3813889, -9.3025],  # Abbeyfeale
# #     [52.8991667, -7.3575],  # Abbeyleix
# #     [52.0938889, -7.6113889],  # Abbeyside
# #     [54.0608333, -8.5036111],  # Abbeyville
# #     [53.3930556, -6.355],# Abbotstown
# #     [52.53, 13.42],
# # ])
#
# world_locations = np.array(
#     [[34.5289, 69.1725], [41.3275, 19.8189], [36.7525, 3.042], [-14.2781, -170.7025], [42.5078, 1.5211],
#      [-8.8368, 13.2343], [18.217, -63.0578], [17.1172, -61.8457], [-34.6051, -58.4004], [40.182, 44.5146],
#      [12.524, -70.027], [-35.2835, 149.1281], [48.2064, 16.3707], [40.3777, 49.892], [25.0582, -77.3431],
#      [26.2154, 50.5832], [23.7104, 90.4074], [13.1, -59.6167], [53.9, 27.5667], [50.8467, 4.3499], [17.25, -88.7667],
#      [6.3654, 2.4183], [32.2915, -64.778], [27.4661, 89.6419], [-16.5, -68.15], [43.8486, 18.3564], [-24.6545, 25.9086],
#      [-15.7797, -47.9297], [18.4167, -64.6167], [4.9403, 114.9481], [42.6975, 23.3242], [12.3642, -1.5383],
#      [-3.3822, 29.3644], [14.9215, -23.5087], [11.5625, 104.916], [3.8667, 11.5167], [45.4166, -75.698],
#      [12.15, -68.2667], [19.2866, -81.3744], [4.3612, 18.555], [12.1067, 15.0444], [49.188, -2.1049],
#      [49.4598, -2.5353], [-33.4569, -70.6483], [39.9075, 116.3972], [22.2796, 114.1887], [22.2006, 113.5461],
#      [25.047, 121.5457], [4.6097, -74.0818], [-11.7022, 43.2551], [-4.2658, 15.2832], [-21.23, -159.76],
#      [9.9278, -84.0807], [5.3453, -4.0268], [45.8144, 15.978], [23.1195, -82.3785], [12.1084, -68.9335],
#      [35.1595, 33.3669], [50.088, 14.4208], [39.0339, 125.7543], [-4.3276, 15.3136], [55.6759, 12.5655],
#      [11.5877, 43.1447], [15.3017, -61.3881], [18.4896, -69.9018], [-0.2299, -78.525], [30.0392, 31.2394],
#      [13.6894, -89.1872], [3.75, 8.7833], [15.3333, 38.9333], [59.437, 24.7535], [9.025, 38.7469], [62.0097, -6.7716],
#      [-51.7012, -57.8494], [-18.1416, 178.4415], [60.1692, 24.9402], [48.8534, 2.3488], [4.9333, -52.3333],
#      [-17.5333, -149.5667], [0.3925, 9.4537], [13.4531, -16.6794], [41.6941, 44.8337], [52.5244, 13.4105],
#      [5.556, -0.1969], [36.1447, -5.3526], [37.9534, 23.749], [64.1835, -51.7216], [12.0564, -61.7485],
#      [15.9985, -61.7255], [13.4757, 144.7489], [14.6127, -90.5307], [9.5716, -13.6476], [11.8636, -15.5977],
#      [6.8045, -58.1553], [18.5392, -72.335], [41.9024, 12.4533], [14.0818, -87.2068], [47.498, 19.0399],
#      [64.1355, -21.8954], [28.6667, 77.2167], [-6.2118, 106.8416], [35.6944, 51.4215], [33.3406, 44.4009],
#      [53.3331, -6.2489], [54.15, -4.4833], [31.769, 35.2163], [41.8947, 12.4811], [17.997, -76.7936],
#      [35.6895, 139.6917], [31.9552, 35.945], [51.1801, 71.446], [-1.2833, 36.8167], [1.3272, 172.9813],
#      [29.3697, 47.9783], [42.87, 74.59], [17.9667, 102.6], [56.946, 24.1059], [33.9, 35.4833], [-29.3167, 27.4833],
#      [6.3005, -10.7969], [32.8752, 13.1875], [47.1415, 9.5215], [54.6892, 25.2798], [49.6117, 6.13],
#      [-18.9137, 47.5361], [-13.9669, 33.7873], [3.1412, 101.6865], [4.1748, 73.5089], [12.65, -8.0], [35.8997, 14.5147],
#      [7.0897, 171.3803], [14.6089, -61.0733], [18.0858, -15.9785], [-20.1619, 57.4989], [-12.7794, 45.2272],
#      [19.4273, -99.1419], [6.9174, 158.1588], [43.7333, 7.4167], [47.9077, 106.8832], [42.4411, 19.2636],
#      [16.7918, -62.2106], [34.0133, -6.8326], [-25.9653, 32.5892], [19.745, 96.1297], [-22.5594, 17.0832],
#      [-0.5308, 166.9112], [27.7017, 85.3206], [52.374, 4.8897], [-22.2763, 166.4572], [-41.2866, 174.7756],
#      [12.1328, -86.2504], [13.5137, 2.1098], [9.0574, 7.4898], [-19.0585, -169.9213], [15.2123, 145.7545],
#      [59.9127, 10.7461], [23.6139, 58.5922], [33.7035, 73.0594], [7.3426, 134.4789], [8.9958, -79.5196],
#      [-9.4431, 147.1797], [-25.3007, -57.6359], [-12.0432, -77.0282], [14.6042, 120.9822], [52.2298, 21.0118],
#      [38.7169, -9.1399], [18.4663, -66.1057], [25.2747, 51.5245], [37.5683, 126.9778], [47.0056, 28.8575],
#      [-20.8823, 55.4504], [44.4328, 26.1043], [55.755, 37.6218], [-1.9474, 30.0579], [-15.9387, -5.7168],
#      [17.2948, -62.7261], [14.006, -60.991], [46.7738, -56.1815], [13.1587, -61.2248], [-13.8333, -171.7667],
#      [43.9333, 12.45], [0.3365, 6.7273], [24.6905, 46.7096], [14.6937, -17.4441], [44.8176, 20.4633], [-4.6167, 55.45],
#      [8.484, -13.2299], [1.2897, 103.8501], [18.026, -63.0458], [48.1482, 17.1067], [46.0511, 14.5051],
#      [-9.4333, 159.95], [2.0416, 45.3435], [-33.9258, 18.4232], [4.8517, 31.5825], [40.4165, -3.7026],
#      [6.9319, 79.8478], [31.7834, 35.2339], [15.5518, 32.5324], [5.8664, -55.1668], [-26.3167, 31.1333],
#      [59.3326, 18.0649], [46.9481, 7.4474], [33.5086, 36.3084], [38.5358, 68.7791], [42.0, 21.4333], [13.722, 100.5252],
#      [-8.5601, 125.5668], [6.1375, 1.2123], [-9.38, -171.25], [-21.1394, -175.2032], [10.6662, -61.5166],
#      [36.819, 10.1658], [39.9199, 32.8543], [37.95, 58.3833], [21.4612, -71.1419], [-8.5189, 179.1991],
#      [0.3163, 32.5822], [50.4454, 30.5186], [24.4648, 54.3618], [51.5085, -0.1257], [-6.1722, 35.7395],
#      [38.8951, -77.0364], [18.3419, -64.9307], [-34.8335, -56.1674], [41.2647, 69.2163], [-17.7338, 168.3219],
#      [10.488, -66.8792], [21.0245, 105.8412], [-13.2816, -176.1745], [27.1532, -13.2014], [15.3531, 44.2078],
#      [-15.4134, 28.2771], [-17.8294, 31.0539]])

with open('data/operations_cleaned.csv', mode='r', newline='', encoding='utf-8') as infile:
    reader = csv.reader(infile)
    header = next(reader)
    rows = [[row[5], row[6]] for row in reader]

bombing_locations = []
for row in rows:
    if row[0] != '' and row[1] != '':
        if row[0] != 100.65 and float(row[1]) < 80.00:
            bombing_locations.append([float(row[0]), float(row[1])])

with open('data/europenorthafricacitiespop.csv', mode='r', newline='', encoding='utf-8') as infile:
    reader = csv.reader(infile)
    header = next(reader)
    rowdata = [row for row in reader]
    rows = [[row[5], row[6]] for row in rowdata]

eu_naf_country_codes = ['lt', 'al', 'mt', 'ly', 'cz', 'dz', 'ch', 'hr', 'ad', 'pl', 'ro', 'by', 'is', 'cy', 'lu', 'at',
                        'sk',
                        'gb', 'me', 'be', 'ru', 'eh', 'fr', 'gr', 'ee', 'pt', 'ua', 'mk', 'se', 'bg', 'sm', 'de', 'es',
                        'ba',
                        'rs', 'eg', 'ie', 'hu', 'tn', 'li', 'ma', 'mc', 'md', 'si', 'fi', 'it', 'no', 'nl', 'lv', 'dk']

world_locations = []
for row in rowdata:
    if row[0].lower() in eu_naf_country_codes:
        # world_locations.append(row)
        world_locations.append([float(row[5]), float(row[6])])
#
# with open('data/europenorthafricacitiespop.csv', mode='w', newline='', encoding='utf-8') as outfile:
#     writer = csv.writer(outfile)
#     writer.writerow(header)
#     writer.writerows(world_locations)

bombing_locations = np.array(bombing_locations)
world_locations = np.array(world_locations)

print("Beginning KMeans")
# kmeans = KMeans(n_clusters=1000)
#
# print('fitting locations')
# kmeans = kmeans.fit(world_locations)

kmeans = joblib.load('Data/kmeans_bombing_model_1000_clusters.pkl')

print("Fitting bombing locations to a world location")
nearest_locations_indices = kmeans.predict(bombing_locations)

# bombings_per_centroid = np.bincount(nearest_locations_indices)
# significant_centroids_indices = np.where(bombings_per_centroid > 10)[0]
# significant_centroids = kmeans.cluster_centers_[significant_centroids_indices]
# significant_bombing_locations_indices = np.isin(nearest_locations_indices, significant_centroids_indices)
# significant_bombing_locations = bombing_locations[significant_bombing_locations_indices]

nearest_locations = kmeans.cluster_centers_[nearest_locations_indices]

rounded_significant_centroids = np.round(nearest_locations, decimals=5)
dtype = np.dtype(','.join(['f8'] * rounded_significant_centroids.shape[1]))
_, unique_indices = np.unique(rounded_significant_centroids.view(dtype), return_index=True, axis=0)
unique_significant_centroids = nearest_locations[unique_indices]

print("Getting coordinates of location")
# print(len(nearest_locations))
#
# rounded_locations = np.round(nearest_locations, decimals=5)
# dtype = np.dtype(','.join(['f8'] * rounded_locations.shape[1]))
# _, unique_indices = np.unique(rounded_locations.view(dtype), return_index=True, axis=0)
# unique_nearest_locations = nearest_locations[unique_indices]

# print("Saving KMeans model")
# joblib.dump(kmeans, 'data/kmeans_bombing_model_1000_clusters.pkl')
print("Completed KMeans")

# bombings_per_centroid = np.bincount(nearest_locations_indices)
# significant_centroids_indices = np.where(bombings_per_centroid > 10)[0]
# significant_centroids = kmeans.cluster_centers_[significant_centroids_indices]
# significant_bombing_locations = bombing_locations[np.isin(nearest_locations_indices, significant_centroids_indices)]

print('plotting on scatter')
latitude = unique_significant_centroids[:, 0]
longitude = unique_significant_centroids[:, 1]

plt.scatter(longitude, latitude)
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Geographical Scatter Plot')

plt.savefig('data/bombing_scatter_1000_clusters.png')
plt.close()

print("Plotting on map")
map_center = np.mean(unique_significant_centroids, axis=0)

map = folium.Map(location=map_center, zoom_start=4)

for location in unique_significant_centroids:
    folium.Marker([location[0], location[1]]).add_to(map)

print("Saving map")
map_path = 'Data/map_of_locations_1000_clusters.html'
map.save(map_path)

print(f"Map has been saved to {map_path}")