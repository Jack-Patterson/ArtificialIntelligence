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

    def state_of_board(self):
        white_pieces, black_pieces = self.count_pieces()
        white_moves = len(self.get_possible_moves('W'))
        black_moves = len(self.get_possible_moves('B'))

        if white_pieces == 0 and black_pieces == 0:
            return 'D'
        elif white_pieces == 0 or black_pieces == 0:
            return 'W'

        if white_moves == 0 or black_moves == 0:
            return 'W'

        return "U"

    def display(self, highlight_positions=None):

        print("  A B C D E F G H")
        row_number = 8
        for row_idx, row in enumerate(self.board):
            display_row = ""
            for col_idx, piece in enumerate(row):
                if highlight_positions is not None and (row_idx, col_idx) in highlight_positions:
                    display_row += 'o '
                else:
                    display_row += f"{piece} "
            print(f"{row_number} {display_row}")
            row_number -= 1
        print("\n")

    def other(self, piece):
        return 'B' if piece.upper() == 'W' else 'W'

    def all_possible_moves(self, player_piece: str):
        possible_moves = []
        no_piece_in_position = '.'
        direction = -1 if player_piece.upper() == 'W' else 1

        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                if self.is_player_piece_at_position(row, col, player_piece):
                    self.find_moves_for_piece(player_piece, row, col, direction, possible_moves, no_piece_in_position)

        return possible_moves

    def position_possible_moves(self, row, col, player_piece):
        possible_moves = set()
        no_piece_in_position = '.'
        direction = -1 if player_piece.upper() == 'W' else 1

        move_positions = [(row + direction, col - 1), (row + direction, col + 1)]

        for new_row, new_col in move_positions:
            if 0 <= new_row < len(self.board) and 0 <= new_col < len(self.board[0]):
                if self.board[new_row][new_col] == no_piece_in_position:
                    possible_moves.add((new_row, new_col))

        return possible_moves

    def is_valid_move_for_position(self, piece_row_index, piece_column_index, suggested_row_index,
                                   suggested_column_index, player_piece):
        return True if ((suggested_row_index, suggested_column_index) in
                        self.position_possible_moves(piece_row_index, piece_column_index, player_piece)) else False

    def get_possible_moves(self, player_piece, specific_position=None):
        if specific_position:
            row_index, col_index = self.get_value_position_at_index(specific_position)
            possible_moves = self.position_possible_moves(row_index, col_index, player_piece)
        else:
            possible_moves = set()
            for row in range(len(self.board)):
                for col in range(len(self.board[row])):
                    if self.board[row][col].lower() == player_piece.lower():
                        piece_moves = self.position_possible_moves(row, col, player_piece)
                        possible_moves.update(piece_moves)

        return possible_moves

    def is_player_piece_at_position(self, row, col, player_piece):
        return self.board[row][col].lower() == player_piece.lower()

    def find_moves_for_piece(self, player_piece, row, col, direction, possible_moves, no_piece):
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
        possible_moves.append(new_board)

    def add_jump_move(self, row, col, over_row, over_col, jump_row, jump_col, possible_moves):
        new_board = self.get_new_board(row, col, jump_row, jump_col)
        new_board.remove_at_board_position(over_row, over_col)
        possible_moves.append(new_board)

    def get_value_position_at_index(self, position: str):
        column_index = ord(position[0].upper()) - ord('A')

        row_index = 8 - int(position[1])
        return row_index, column_index

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

    def count_pieces(self):
        black_pieces = 0
        white_pieces = 0

        for row in self.board:
            for cell in row:
                if cell.upper() == 'W':
                    white_pieces += 1
                elif cell.upper() == 'B':
                    black_pieces += 1

        return white_pieces, black_pieces
