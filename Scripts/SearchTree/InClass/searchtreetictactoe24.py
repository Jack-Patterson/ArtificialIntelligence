# class CurrentBoard:
#     # Tic Tac Toe
#     board = ""
#
#     def __init__(self, string_def=" " * 9):
#         self.board = string_def
#         self.state = self.state_of_board()
#
#     def display(self, game_display=False):
#
#         if game_display:
#             ind = 0
#             c = ""
#             for char in self.board:
#                 if char == " ":
#                     c += str(ind)
#                 else:
#                     c += char
#                 ind += 1
#         else:
#             c = self.board
#
#         print(c[0] + "|" + c[1] + "|" + c[2])
#         print("-----")
#         print(c[3] + "|" + c[4] + "|" + c[5])
#         print("-----")
#         print(c[6] + "|" + c[7] + "|" + c[8])
#
#     def other(self, piece):
#         if piece == "X":
#             return "O"
#         return "X"
#
#     def Eq3(self, i1, i2, i3):
#         if self.board[i1] == " ":
#             return False
#         return (self.board[i1] == self.board[i2]) and (self.board[i2] == self.board[i3])
#
#     def state_of_board(self):
#         if self.Eq3(0, 1, 2) or self.Eq3(0, 3, 6) or self.Eq3(0, 4, 8):
#             return self.board[0]
#         if self.Eq3(3, 4, 5) or self.Eq3(1, 4, 7) or self.Eq3(2, 4, 6):
#             return self.board[4]
#         if self.Eq3(6, 7, 8) or self.Eq3(2, 5, 8):
#             return self.board[8]
#
#         if " " in self.board:
#             return "U"
#         return "D"
#
#     def all_possible_moves(self, player_piece):
#         possible_moves = []
#         for index in range(len(self.board)):
#             if self.board[index] == " ":
#                 possible_moves.append(CurrentBoard(self.board[:index] + player_piece + self.board[index + 1:]))
#
#         return possible_moves
#
#
# class SearchTreeNode:
#
#     def __init__(self, board_instance, playing_as, ply=0):
#         self.children = []
#         self.value_is_assigned = False
#         self.ply_depth = ply
#         self.current_board = board_instance
#         self.move_for = playing_as
#         if self.current_board.state == "U":
#             self.generate_children()
#         else:  # Game over
#             if self.current_board.state == "D":
#                 self.value = 0
#             else:
#                 if ((self.ply_depth % 2) == 0):
#                     self.value = -1
#                 else:
#                     self.value = 1
#             self.value_is_assigned = True
#
#     def min_max_value(self):
#         if self.value_is_assigned:
#             return self.value
#
#         self.children = sorted(self.children, key=lambda x: x.min_max_value())
#
#         if ((self.ply_depth % 2) == 0):
#             # computers move
#             self.value = self.children[-1].value
#         else:
#             # players move
#             self.value = self.children[0].value
#         self.value_is_assigned = True
#
#         return self.value
#
#     def generate_children(self):
#         for board_for_next_move in self.current_board.all_possible_moves(self.move_for):
#             self.children.append(
#                 SearchTreeNode(board_for_next_move, self.current_board.other(self.move_for), ply=self.ply_depth + 1))
#
#
# def play_Tic_Tac_Toe():
#     response = input("Do you wish to play first (y/n) ?")
#     players_turn = (response == "y")
#
#     response = input("Do you wish to play X or O  (X/O) ?")
#     cb = CurrentBoard()
#     player_is_playing = cb.other(cb.other(response))
#
#     for _ in range(10):
#
#         if players_turn:
#             cb.display(game_display=True)
#             choice = input("Make your move ")
#             ind = int(choice)
#             cb = CurrentBoard(cb.board[:ind] + player_is_playing + cb.board[ind + 1:])
#             cb.display()
#
#         else:
#             search_tree = SearchTreeNode(cb, cb.other(player_is_playing))
#             search_tree.min_max_value()
#             cb = search_tree.children[-1].current_board
#         if cb.state != "U":
#             if cb.state == "D":
#                 print(" I cant believe it you drew !!")
#             else:
#                 if players_turn:
#                     print("This is impossible!!!!")
#                 else:
#                     print("Too easy loser !!!")
#                     cb.display()
#
#             break
#
#         players_turn = not players_turn
#
#
# play_Tic_Tac_Toe()
