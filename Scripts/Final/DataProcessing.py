from Final.DataCleaner import DataCleaner


def main():
    clean_bombing_operations(output_name='data/test_cleaned_output.csv')


def clean_bombing_operations(input_name='Data/operations.csv', output_name='Data/operations_cleaned.csv'):
    emea_countries_in_dataset = ['POLAND', 'AUSTRIA', 'YUGOSLAVIA', 'ITALY', 'SICILY', 'TUNISIA', 'BULGARIA', 'FRANCE',
                                 'GREAT BRITAIN', 'PANTELLARIA', 'SARDINIA', 'ALGERIA', 'ROMANIA',
                                 'HOLLAND OR NETHERLANDS', 'GERMANY', 'ALBANIA', 'LUXEMBOURG', 'LIBYA', 'CYPRUS',
                                 'CRETE', 'DENMARK', 'HUNGARY', 'CORSICA', 'SWITZERLAND', 'NORWAY', 'BELGIUM', 'GREECE',
                                 'CZECHOSLOVAKIA']
    rows_and_headers_to_keep = [1, 3, 14, 15, 19, 20]

    data_cleaner = DataCleaner(input_name, output_name)
    data_cleaner.remove_if_row_empty(3)
    data_cleaner.remove_if_row_empty(19)
    data_cleaner.remove_if_row_empty(20)
    data_cleaner.filter_for_locations(emea_countries_in_dataset, 14)
    data_cleaner.remove_irrelevant_data(rows_and_headers_to_keep)
    data_cleaner.remove_all_over_threshold(5, 80)
    data_cleaner.save()


if __name__ == '__main__':
    main()
