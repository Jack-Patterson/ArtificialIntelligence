def cost(chromosome):
    square = len(chromosome)
    square_side = int(square ** 0.5)
    sum_all_numbers = (square * (square + 1)) / 2
    expected_row_column_total = sum_all_numbers / square_side

    rows = [sum(chromosome[i * square_side: (i + 1) * square_side]) for i in range(square_side)]
    columns = [sum([chromosome[i + j * square_side] for j in range(square_side)]) for i in range(square_side)]

    row_offset_from_expected = sum(abs(row_total - expected_row_column_total) for row_total in rows)
    column_offset_from_expected = sum(abs(column_total - expected_row_column_total) for column_total in columns)

    return int(row_offset_from_expected + column_offset_from_expected)
