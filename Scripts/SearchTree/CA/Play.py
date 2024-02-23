def play():
    # board = [
    #             ['.', 'b', '.', 'b', '.', 'b', '.', 'b'],
    #             ['b', '.', 'b', '.', 'b', '.', 'b', '.'],
    #             ['.', 'b', '.', 'b', '.', 'b', '.', 'b'],
    #             ['.', '.', '.', '.', '.', '.', '.', '.'],
    #             ['.', '.', '.', '.', '.', '.', '.', '.'],
    #             ['w', '.', 'w', '.', 'w', '.', 'w', '.'],
    #             ['.', 'w', '.', 'w', '.', 'w', '.', 'w'],
    #             ['w', '.', 'w', '.', 'w', '.', 'w', '.']
    #         ]
    #
    # for row in board:
    #     print(row)

    board = [
        ['.', 'b', '.', 'b', '.', 'b', '.', 'b'],
        ['b', '.', 'b', '.', 'b', '.', 'b', '.'],
        ['.', 'b', '.', 'b', '.', 'b', '.', 'b'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['w', '.', 'w', '.', 'w', '.', 'w', '.'],
        ['.', 'w', '.', 'w', '.', 'w', '.', 'w'],
        ['w', '.', 'w', '.', 'w', '.', 'w', '.']
    ]

    # Function to convert column number to letter (A-H)
    def column_to_letter(column):
        return chr(column + 65)

    def get_board_value_at_position(position):
        # Mapping the column letters to array indices (0-based)
        col_mapping = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7}

        # Extracting the column letter and row number from the position
        col_letter = position[0]
        row_number = int(position[1])

        # Convert the column letter to an index
        col_index = col_mapping[col_letter]

        # Convert the row number to a 0-based index
        # Since the board is indexed from 8 at the top to 1 at the bottom,
        # we subtract the row number from 8 to get the 0-based index.
        row_index = 8 - row_number

        # Return the value at the specified position
        return board[row_index][col_index]

    # Printing the board with rows and columns like chess
    # Print column letters at the top
    print('  ', end='')
    for col in range(8):
        print(f' {column_to_letter(col)}  ', end='')
    print()

    # Print the board with row numbers
    for row in range(8, 0, -1):  # Start from 8 to 1 for proper chess rows
        print(f'{row} ', end='')  # Print the row number
        for col in range(8):
            print(f'[{board[8 - row][col]}]', end=' ')  # Adjust board indexing for correct orientation
        print()  # Newline after each row

    print(f"\n{get_board_value_at_position('B8')}")


if __name__ == '__main__':
    play()
