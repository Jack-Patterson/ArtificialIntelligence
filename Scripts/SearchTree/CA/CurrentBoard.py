class CurrentBoard:
    board = ""
    default_board = [
        ['.', 'b', '.', 'b', '.', 'b', '.', 'b'],
        ['b', '.', 'b', '.', 'b', '.', 'b', '.'],
        ['.', 'b', '.', 'b', '.', 'b', '.', 'b'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['w', '.', 'w', '.', 'w', '.', 'w', '.'],
        ['.', 'w', '.', 'w', '.', 'w', '.', 'w'],
        ['w', '.', 'w', '.', 'w', '.', 'w', '.']
    ]

    def __init__(self, string_def=None):
        if string_def is None:
            self.board = self.default_board
        else:
            self.board = string_def
        self.state = self.state_of_board()

    def display(self, game_display=False):

        if game_display:
            ind = 0
            new_board = ""
            for char in self.board:
                if char == " ":
                    new_board += str(ind)
                else:
                    new_board += char
                ind += 1
        else:
            new_board = self.board

        print("  A B C D E F G H")
        row_number = 8
        for row in new_board:
            print(f"{row_number} {' '.join(row)}")
            row_number -= 1

    def other(self, piece):
        return 'B' if piece == 'W' else 'W'

    def Eq3(self, i1, i2, i3):
        if self.board[i1] == " ":
            return False
        return (self.board[i1] == self.board[i2]) and (self.board[i2] == self.board[i3])

    def state_of_board(self):
        # if self.Eq3(0, 1, 2) or self.Eq3(0, 3, 6) or self.Eq3(0, 4, 8):
        #     return self.board[0]
        # if self.Eq3(3, 4, 5) or self.Eq3(1, 4, 7) or self.Eq3(2, 4, 6):
        #     return self.board[4]
        # if self.Eq3(6, 7, 8) or self.Eq3(2, 5, 8):
        #     return self.board[8]
        #
        # if " " in self.board:
        #     return "U"
        # return "D"
        return "U"

    def all_possible_moves(self, player_piece: str):
        no_piece_in_position = '.'
        possible_moves = []

        for index in range(len(self.board)):
            for index2 in range(len(self.board[index])):
                piece_at_position: str = self.board[index][index2]

                if player_piece.upper() == 'W':
                    if piece_at_position == 'w':
                        if index != 0:
                            if index2 == 0:
                                if self.board[index - 1][index2 + 1] == no_piece_in_position:
                                    print(self.indices_to_board_position(index - 1, index2 + 1))
                            elif index2 == 7:
                                if self.board[index - 1][index2 - 1] == no_piece_in_position:
                                    print(self.indices_to_board_position(index - 1, index2 - 1))
                            else:
                                if self.board[index - 1][index2 + 1] == no_piece_in_position:
                                    print(self.indices_to_board_position(index - 1, index2 + 1))
                                if self.board[index - 1][index2 - 1] == no_piece_in_position:
                                    print(self.indices_to_board_position(index - 1, index2 - 1))

                else:
                    if piece_at_position == 'b':
                        if index != 8:
                            if index2 == 0:
                                if self.board[index + 1][index2 + 1] == no_piece_in_position:
                                    print(self.indices_to_board_position(index + 1, index2 + 1))
                            elif index2 == 7:
                                if self.board[index + 1][index2 - 1] == no_piece_in_position:
                                    print(self.indices_to_board_position(index + 1, index2 - 1))
                            else:
                                if self.board[index + 1][index2 + 1] == no_piece_in_position:
                                    print(self.indices_to_board_position(index + 1, index2 + 1))
                                if self.board[index + 1][index2 - 1] == no_piece_in_position:
                                    print(self.indices_to_board_position(index + 1, index2 - 1))

        return possible_moves

    def get_value_position_at_index(self, position):
        column_index = ord(position[0].upper()) - ord('A')

        row_index = 8 - int(position[1])
        return self.board[row_index][column_index]

    def indices_to_board_position(self, row_index, column_index):
        column_letter = chr(column_index + ord('A'))
        row_number = 8 - row_index

        return f"{column_letter}{row_number}"

    def switch_positions(self, initial_position, move_position):
        initial_column_index = ord(initial_position[0].upper()) - ord('A')
        initial_row_index = 8 - int(initial_position[1])

        move_column_index = ord(move_position[0].upper()) - ord('A')
        move_row_index = 8 - int(move_position[1])

        (self.board[initial_row_index][initial_column_index], self.board[move_row_index][move_column_index]) = (
            self.board[move_row_index][move_column_index], self.board[initial_row_index][initial_column_index])
