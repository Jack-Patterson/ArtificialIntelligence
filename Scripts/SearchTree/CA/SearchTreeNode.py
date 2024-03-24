class SearchTreeNode:

    def __init__(self, board_instance, playing_as, ply_depth=0, max_ply_depth=6):
        self.children = []
        self.value_is_assigned = False
        self.ply_depth = ply_depth
        self.max_ply_depth = max_ply_depth
        self.current_board = board_instance
        self.move_for = playing_as
        if self.current_board.state_of_board() == "U" and ply_depth != max_ply_depth:
            self.generate_children()
        else:
            if self.current_board.state_of_board() == "D":
                self.value = 0
            elif self.current_board.state_of_board() == "U":
                self.value = self.evaluate_board()
            else:
                if (self.ply_depth % 2) == 0:
                    self.value = -1
                else:
                    self.value = 1
            self.value_is_assigned = True

    def min_max_value(self):
        if self.value_is_assigned:
            return self.value

        if len(self.children) == 0:
            return self.evaluate_board()

        self.children = sorted(self.children, key=lambda x: x.min_max_value())

        if (self.ply_depth % 2) == 0:
            self.value = max(child.min_max_value() for child in self.children)
        else:
            self.value = min(child.min_max_value() for child in self.children)
        self.value_is_assigned = True

        return self.value

    def generate_children(self):
        for board_for_next_move in self.current_board.get_all_possible_moves(self.move_for):
            self.children.append(
                SearchTreeNode(board_for_next_move, self.current_board.get_other_piece_colour(self.move_for),
                               self.ply_depth + 1))

    def evaluate_board(self):
        pawn_value = 0.75
        king_value = 1.0
        total_score = (12 * pawn_value + 12 * king_value)
        modifier = -1 if self.ply_depth % 2 == 0 else 1

        white_pawns, black_pawns, white_kings, black_kings = self.current_board.count_pawns_and_kings()
        white_score = (white_pawns * pawn_value) + (white_kings * king_value)
        black_score = (black_pawns * pawn_value) + (black_kings * king_value)

        piece_difference = white_score - black_score
        score = (piece_difference / total_score) * modifier

        return score
