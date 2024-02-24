def test():
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

    # Function to print the board with chess notation
    def print_board_with_notation(board):
        print("  A B C D E F G H")
        row_number = 8
        for row in board:
            print(f"{row_number} {' '.join(row)}")
            row_number -= 1

    print_board_with_notation(board)


test()
