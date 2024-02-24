from copy import deepcopy


class Board:
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
        return 'B' if piece.upper() == 'W' else 'W'

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
        possible_moves = []
        no_piece_in_position = '.'
        direction = -1 if player_piece.upper() == 'W' else 1
        start_row, end_row = (0, 7) if direction == -1 else (7, 0)

        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                if self.is_player_piece(row, col, player_piece):
                    self.find_moves_for_piece(player_piece, row, col, direction, possible_moves, no_piece_in_position, start_row,
                                              end_row)

        return possible_moves

    def is_player_piece(self, row, col, player_piece):
        return self.board[row][col].lower() == player_piece.lower()

    def find_moves_for_piece(self, player_piece, row, col, direction, possible_moves, no_piece, start_row, end_row):
        opponent_piece = self.other(player_piece)
        move_positions = [(row + direction, col - 1), (row + direction, col + 1)]

        for new_row, new_col in move_positions:
            if 0 <= new_row <= 7 and 0 <= new_col <= 7:
                if self.board[new_row][new_col] == no_piece:
                    self.add_move(row, col, new_row, new_col, possible_moves)
                elif self.board[new_row][
                    new_col].upper() == opponent_piece and 0 <= new_row + direction <= 7 and 0 <= new_col + (
                        new_col - col) <= 7:
                    jump_row, jump_col = new_row + direction, new_col + (new_col - col)
                    if self.board[jump_row][jump_col] == no_piece:
                        self.add_jump_move(row, col, new_row, new_col, jump_row, jump_col, possible_moves)

    def add_move(self, row, col, new_row, new_col, possible_moves):
        new_board = self.get_new_board(row, col, new_row, new_col)
        new_board.display()
        print("\n")
        possible_moves.append(new_board)

    def add_jump_move(self, row, col, over_row, over_col, jump_row, jump_col, possible_moves):
        new_board = self.get_new_board(row, col, jump_row, jump_col)
        new_board.remove_at_board_position(over_row, over_col)
        new_board.display()
        print("\n")
        possible_moves.append(new_board)

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

    def remove_at_board_position(self, row_index, column_index, remove_character='.'):
        self.board[row_index][column_index] = remove_character

    def get_new_board(self, initial_pos_row, initial_pos_column, new_pos_row, new_pos_column):
        current_position = self.indices_to_board_position(initial_pos_row, initial_pos_column)
        potential_move_position = self.indices_to_board_position(new_pos_row, new_pos_column)

        new_board = Board(deepcopy(self.board))
        new_board.switch_positions(current_position, potential_move_position)

        return new_board
