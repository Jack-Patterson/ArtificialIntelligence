class SearchTreeNode:

    def __init__(self, board_instance, playing_as, ply=0):
        self.children = []
        self.value_is_assigned = False
        self.ply_depth = ply
        self.current_board = board_instance
        self.move_for = playing_as
        if self.current_board.state == "U":
            self.generate_children()
        else:
            if self.current_board.state == "D":
                self.value = 0
            else:
                if (self.ply_depth % 2) == 0:
                    self.value = -1
                else:
                    self.value = 1
            self.value_is_assigned = True

    def min_max_value(self):
        if self.value_is_assigned:
            return self.value

        self.children = sorted(self.children, key=lambda x: x.min_max_value())

        if (self.ply_depth % 2) == 0:
            # computers move
            self.value = self.children[-1].value
        else:
            self.value = self.children[0].value
        self.value_is_assigned = True

        return self.value

    def generate_children(self):
        for board_for_next_move in self.current_board.all_possible_moves(self.move_for):
            self.children.append(
                SearchTreeNode(board_for_next_move, self.current_board.other(self.move_for), ply=self.ply_depth + 1))
