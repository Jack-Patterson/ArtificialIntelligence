import csv

with open('Data/DataSets/country-capital-lat-long-population.csv', mode='r', newline='', encoding='utf-8') as infile:
    reader = csv.reader(infile)
    header = next(reader)
    rows = [[row[2], row[3]] for row in reader]

rows_fixed = []
for row in rows:
    rows_fixed.append([float(row[0]), float(row[1])])

print(f'np.array({rows_fixed})')
