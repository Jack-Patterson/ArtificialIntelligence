from copy import deepcopy
from typing import Tuple, Optional


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
        self.state = self.state_of_board

    def state_of_board(self):
        white_pieces, black_pieces = self.count_pieces()
        white_moves = len(self.get_positions_of_all_possible_moves('W'))
        black_moves = len(self.get_positions_of_all_possible_moves('B'))

        if white_pieces == 0 and black_pieces == 0:
            return 'D'
        elif white_pieces == 0 or black_pieces == 0:
            return 'W'

        if white_moves == 0 or black_moves == 0:
            return 'W'

        return "U"

    def display(self, highlight_positions: Optional[Tuple[int, int]] = None) -> None:
        print("  A B C D E F G H")
        row_number = 8
        for row_index, row in enumerate(self.board):
            display_row = ""
            for col_index, piece in enumerate(row):
                if highlight_positions is not None and (row_index, col_index) in highlight_positions:
                    display_row += 'o '
                else:
                    display_row += f"{piece} "
            print(f"{row_number} {display_row}")
            row_number -= 1
        print("\n")

    def get_other_piece_colour(self, piece: str) -> str:
        return 'B' if piece.upper() == 'W' else 'W'

    def is_player_piece_at_position(self, player_piece: str, piece_row_index: int, piece_column_index: int) -> bool:
        return self.board[piece_row_index][piece_column_index].upper() == player_piece.upper()

    def find_moves_for_king_piece(self, row, col, possible_moves):
        moves = []
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        for d_row, d_col in directions:
            next_row, next_col = row + d_row, col + d_col
            if (0 <= next_row < len(self.board) and 0 <= next_col < len(self.board[0]) and
                    self.board[next_row][next_col] == '.'):
                moves.append((next_row, next_col))
        return moves

    def get_positions_of_all_possible_moves(self, player_piece: str, piece_row_index: int = None,
                                            piece_column_index: int = None, as_board=False):
        if type(piece_row_index) is int and type(piece_column_index) is int:
            possible_regular_moves, possible_jumps_moves = self.get_positions_of_all_possible_moves_for_piece(
                player_piece,
                piece_row_index,
                piece_column_index)
        else:
            possible_regular_moves = []
            possible_jumps_moves = []
            for row in range(len(self.board)):
                for column in range(len(self.board[row])):
                    if self.is_player_piece_at_position(player_piece, row, column):
                        piece_moves, piece_jumps = self.get_positions_of_all_possible_moves_for_piece(player_piece, row,
                                                                                                      column, as_board)
                        possible_regular_moves.extend(piece_moves)
                        possible_jumps_moves.extend(piece_jumps)

        return possible_jumps_moves if possible_jumps_moves else possible_regular_moves

    def get_positions_of_all_possible_moves_for_piece(self, player_piece: str, piece_row_index: int,
                                                      piece_column_index: int, as_board: bool = False):
        possible_regular_moves = []
        possible_jumps_moves = []
        no_piece_in_position = '.'
        direction = -1 if player_piece.upper() == 'W' else 1

        move_positions = [(piece_row_index + direction, piece_column_index - 1),
                          (piece_row_index + direction, piece_column_index + 1)]
        jump_positions = [(piece_row_index + 2 * direction, piece_column_index - 2),
                          (piece_row_index + 2 * direction, piece_column_index + 2)]

        if self.board[piece_row_index][piece_column_index].isupper():
            move_positions.extend([(piece_row_index - direction, piece_column_index - 1),
                                   (piece_row_index - direction, piece_column_index + 1)])
            jump_positions.extend([(piece_row_index - 2 * direction, piece_column_index - 2),
                                   (piece_row_index - 2 * direction, piece_column_index + 2)])

        for jump_row, jump_col in jump_positions:
            mid_row = (piece_row_index + jump_row) // 2
            mid_col = (piece_column_index + jump_col) // 2

            if 0 <= jump_row < len(self.board) and 0 <= jump_col < len(self.board[0]):
                if (self.board[jump_row][jump_col] == no_piece_in_position and
                        self.board[mid_row][mid_col].upper() == self.get_other_piece_colour(player_piece).upper()):
                    if as_board:
                        new_board = self.add_jump_move(piece_row_index, piece_column_index, mid_row, mid_col, jump_row,
                                                       jump_col)
                        possible_jumps_moves.append(new_board)
                    else:
                        possible_jumps_moves.append((jump_row, jump_col))

        if not possible_jumps_moves:
            for new_row, new_col in move_positions:
                if 0 <= new_row < len(self.board) and 0 <= new_col < len(self.board[0]):
                    if self.board[new_row][new_col] == no_piece_in_position:
                        if as_board:
                            new_board = self.add_regular_move(piece_row_index, piece_column_index, new_row, new_col)
                            possible_regular_moves.append(new_board)
                        else:
                            possible_regular_moves.append((new_row, new_col))

        return possible_regular_moves, possible_jumps_moves

    def add_regular_move(self, piece_row_index, piece_column_index, new_row_index, new_column_index):
        new_board = self.get_new_board(piece_row_index, piece_column_index, new_row_index, new_column_index)
        return new_board

    def add_jump_move(self, piece_row_index, piece_column_index, over_row, over_col, jump_row, jump_col):
        new_board = self.get_new_board(piece_row_index, piece_column_index, jump_row, jump_col)
        new_board.remove_at_board_position(over_row, over_col)
        return new_board

    def get_value_position_at_index(self, position: str) -> Tuple[int, int]:
        column_index = ord(position[0].upper()) - ord('A')
        row_index = 8 - int(position[1])

        return row_index, column_index

    def indices_to_board_position(self, row_index: int, column_index: int) -> str:
        column_letter = chr(column_index + ord('A'))
        row_number = 8 - row_index

        return f"{column_letter}{row_number}"

    def switch_positions(self, initial_row_index: int, initial_column_index: int, move_row_index: int,
                         move_column_index: int) -> None:
        piece = self.board[initial_row_index][initial_column_index]
        self.board[initial_row_index][initial_column_index] = '.'
        self.board[move_row_index][move_column_index] = piece

        if piece.lower() == 'w' and move_row_index == 0:
            self.board[move_row_index][move_column_index] = 'W'  # White piece becomes a king
        elif piece.lower() == 'b' and move_row_index == len(self.board) - 1:
            self.board[move_row_index][move_column_index] = 'B'

    def remove_at_board_position_if_jump(self, player_piece: str, initial_piece_row_index: int,
                                         initial_piece_column_index: int, new_piece_row_index: int,
                                         new_piece_column_index: int) -> None:
        if self.board[new_piece_row_index][new_piece_column_index].isupper():
            directions = [-1, 1]
        else:
            directions = [-1] if player_piece == 'W' else [1]

        for direction in directions:
            if (new_piece_row_index - initial_piece_row_index == 2 * direction and abs(
                    new_piece_column_index - initial_piece_column_index) == 2) or (
                    initial_piece_row_index - new_piece_row_index == 2 * direction and abs(
                initial_piece_column_index - new_piece_column_index) == 2):
                jumped_row_index = initial_piece_row_index + direction
                jumped_column_index = initial_piece_column_index + (
                        new_piece_column_index - initial_piece_column_index) // 2

                self.remove_at_board_position(jumped_row_index, jumped_column_index)

    def remove_at_board_position(self, piece_row_index: int, piece_column_index: int,
                                 remove_character: chr = '.') -> None:
        self.board[piece_row_index][piece_column_index] = remove_character

    def get_new_board(self, piece_row_index: int, piece_column_index: int, move_row_index: int, move_column_index: int):
        new_board = Board(deepcopy(self.board))
        new_board.switch_positions(piece_row_index, piece_column_index, move_row_index, move_column_index)

        return new_board

    def count_pieces(self) -> Tuple[int, int]:
        """

        Returns: Tuple containing the counts of black and white pieces on the board.

        """
        black_pieces = 0
        white_pieces = 0

        for row in self.board:
            for cell in row:
                if cell.upper() == 'W':
                    white_pieces += 1
                elif cell.upper() == 'B':
                    black_pieces += 1

        return white_pieces, black_pieces

    def count_pawns_and_kings(self):
        white_pawns, black_pawns, white_kings, black_kings = 0, 0, 0, 0

        for row in self.board:
            for cell in row:
                if cell == 'w':
                    white_pawns += 1
                elif cell == 'W':
                    white_kings += 1
                elif cell == 'b':
                    black_pawns += 1
                elif cell == 'B':
                    black_kings += 1

        return white_pawns, black_pawns, white_kings, black_kings
