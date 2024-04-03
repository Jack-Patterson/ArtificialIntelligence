import csv


# Function to filter and save rows
def filter_and_save_csv(input_filename, output_filename, target_value):
    with open(input_filename, mode='r', newline='', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        header = next(reader)  # Skip the header row if your CSV has one
        rows = len([row for row in reader])
        print(rows)
        # Filter rows where the first element is exactly 'ie'
        filtered_rows = [row for row in reader if row[0] == target_value]

    with open(output_filename, mode='w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(header)  # Write the header row to the new file
        writer.writerows(filtered_rows)  # Write the filtered rows


# Replace 'your_input_file.csv' with the path to your actual input CSV file
input_csv = 'Data/worldcitiespop.csv'
output_csv = 'Data/new_data.csv'
filter_value = 'ie'

# Call the function with your file paths and filter value
filter_and_save_csv(input_csv, output_csv, filter_value)
