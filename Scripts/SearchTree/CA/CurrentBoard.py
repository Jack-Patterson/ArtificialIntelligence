class CurrentBoard:
    board = ""

    def __init__(self, string_def=" " * 9):
        self.board = string_def
        self.state = self.state_of_board()

    def display(self, game_display=False):

        if game_display:
            ind = 0
            c = ""
            for char in self.board:
                if char == " ":
                    c += str(ind)
                else:
                    c += char
                ind += 1
        else:
            c = self.board

        print(c[0] + "|" + c[1] + "|" + c[2])
        print("-----")
        print(c[3] + "|" + c[4] + "|" + c[5])
        print("-----")
        print(c[6] + "|" + c[7] + "|" + c[8])

    def other(self, piece):
        if piece == "X":
            return "O"
        return "X"

    def Eq3(self, i1, i2, i3):
        if self.board[i1] == " ":
            return False
        return (self.board[i1] == self.board[i2]) and (self.board[i2] == self.board[i3])

    def state_of_board(self):
        if self.Eq3(0, 1, 2) or self.Eq3(0, 3, 6) or self.Eq3(0, 4, 8):
            return self.board[0]
        if self.Eq3(3, 4, 5) or self.Eq3(1, 4, 7) or self.Eq3(2, 4, 6):
            return self.board[4]
        if self.Eq3(6, 7, 8) or self.Eq3(2, 5, 8):
            return self.board[8]

        if " " in self.board:
            return "U"
        return "D"

    def all_possible_moves(self, player_piece):
        possible_moves = []
        for index in range(len(self.board)):
            if self.board[index] == " ":
                possible_moves.append(CurrentBoard(self.board[:index] + player_piece + self.board[index + 1:]))

        return possible_moves