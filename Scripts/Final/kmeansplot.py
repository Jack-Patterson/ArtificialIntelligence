import csv

import folium
import joblib
import numpy as np
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans

with open('Data/DataSets/operations_cleaned.csv', mode='r', newline='', encoding='utf-8') as infile:
    reader = csv.reader(infile)
    header = next(reader)
    rows = [[row[5], row[6]] for row in reader]

bombing_locations = []
for row in rows:
    if row[0] != '' and row[1] != '':
        if row[0] != 100.65 and float(row[1]) < 60.00:
            bombing_locations.append([float(row[0]), float(row[1])])

with open('Data/DataSets/emea_locations.csv', mode='r', newline='', encoding='utf-8') as infile:
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

# bombing_locations = bombing_locations[:int(len(bombing_locations)/10)]

bombing_locations = np.array(bombing_locations)
world_locations = np.array(world_locations)

print(world_locations.shape)
print(bombing_locations.shape)

latitude = bombing_locations[:, 0]
longitude = bombing_locations[:, 1]

plt.scatter(longitude, latitude)
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Geographical Scatter Plot')

plt.savefig('data/bombing_scatter2.png')
plt.close()

# map_center = np.mean(bombing_locations, axis=0)
# map = folium.Map(location=map_center, zoom_start=4)
#
# for location in bombing_locations:
#     folium.Marker([location[0], location[1]]).add_to(map)
#
# print("Saving map")
# map_path = 'Data/map_of_locations2.html'
# map.save(map_path)

# kmeans = KMeans(n_clusters=100).fit(world_locations)
# nearest_locations_indices = kmeans.predict(bombing_locations)
# nearest_locations = kmeans.cluster_centers_[nearest_locations_indices]
# joblib.dump(kmeans, 'data/kmeans_bombing_model.pkl')