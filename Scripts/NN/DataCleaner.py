import csv


class DataCleaner:

    def __init__(self, input_filename, output_filename):
        self.input_filename = input_filename
        self.output_filename = output_filename

        with open(self.input_filename, mode='r', newline='', encoding='utf-8') as infile:
            reader = csv.reader(infile)
            self.header = next(reader)
            self.data = [row for row in reader]

    def save(self):
        with open(self.output_filename, mode='w', newline='', encoding='utf-8') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(self.header)
            writer.writerows(self.data)

    def remove_irrelevant_data(self, rows_and_headers_to_keep):
        new_rows = []
        for row in self.data:
            new_row_data = []
            for index in rows_and_headers_to_keep:
                new_row_data.append(row[index])
            new_rows.append(new_row_data)

        new_header = []
        for index in rows_and_headers_to_keep:
            new_header.append(self.header[index])

        self.data = new_rows
        self.header = new_header

    def remove_if_row_empty(self, row_index):
        self.data = [row for row in self.data if row[row_index] != '']

    def filter_for_locations(self, row_index, filter_data):
        self.data = [row for row in self.data if row[row_index] in filter_data]

    def remove_all_over_threshold(self, row_index, threshold):
        self.data = [row for row in self.data if float(row[row_index]) < threshold]

    
