import csv


class DataCleaner:

    def __init__(self, input_filename, output_filename):
        self.input_filename = input_filename
        self.output_filename = output_filename

    def open_file(self):
        with open(self.input_filename, mode='r', newline='', encoding='utf-8') as infile:
            reader = csv.reader(infile)
            header = next(reader)
            data = [row for row in reader]

        return data, header

    def remove_row_if_attacking_country_empty(self, data):
        new_data = [row for row in data if row[3] != '']
        return new_data

    def save_cleaned_data(self, data, header):
        with open(self.output_filename, mode='w', newline='', encoding='utf-8') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(header)
            writer.writerows(data)

    def get_data_with_european_locations(self, data):
        european_locations = ['POLAND', 'AUSTRIA', 'YUGOSLAVIA', 'ITALY', 'SICILY', 'TUNISIA', 'BULGARIA', 'FRANCE',
                              'GREAT BRITAIN', 'PANTELLARIA', 'SARDINIA', 'ALGERIA', 'ROMANIA',
                              'HOLLAND OR NETHERLANDS', 'GERMANY', 'ALBANIA', 'LUXEMBOURG', 'LIBYA', 'CYPRUS', 'CRETE',
                              'DENMARK', 'HUNGARY', 'CORSICA', 'SWITZERLAND', 'NORWAY', 'BELGIUM', 'GREECE',
                              'CZECHOSLOVAKIA']
        new_data = [row for row in data if row[14] in european_locations]
        return new_data

    def remove_irrelevant_data(self, data, header):
        new_data = []
        for row in data:
            new_row_data = [row[0], row[1], row[3], row[14], row[15], row[19], row[20]]
            new_data.append(new_row_data)

        new_header = [header[0], header[1], header[3], header[14], header[15], header[19], header[20]]

        return new_data, new_header
