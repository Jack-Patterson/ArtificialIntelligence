from Final.DataCleaner import DataCleaner


def main():
    # clean_bombing_operations()
    # clean_world_locations()
    pass


def clean_bombing_operations(input_name='Data/DataSets/operations.csv',
                             output_name='Data/DataSets/operations_cleaned.csv'):
    """
    Cleans the original bombing dataset and removes all irrelevant data before outputting the cleaned data into a new csv file.
    Args:
        input_name: Name of the original file.
        output_name: Name of the new file.

    """
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
    data_cleaner.filter_for_locations(14, emea_countries_in_dataset)
    data_cleaner.remove_irrelevant_data(rows_and_headers_to_keep)
    data_cleaner.remove_all_over_threshold(5, 80)
    data_cleaner.save()


def clean_world_locations(input_name='Data/DataSets/world_locations.csv',
                          output_name='Data/DataSets/emea_locations.csv'):
    """
    Cleans the original locations dataset and removes all irrelevant data before outputting the cleaned data into a new csv file.
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


if __name__ == '__main__':
    main()
