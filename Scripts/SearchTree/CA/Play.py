from SearchTree.CA.CurrentBoard import Board
from SearchTree.CA.SearchTreeNode import SearchTreeNode


def play():
    game_is_finished = False

    response = input("Do you wish to play first? White will go first. (y/n) ")
    players_turn = (response.lower() == "y")

    cb = Board()

    while game_is_finished is False:
        player_is_playing = 'W' if players_turn is True else 'B'

        if players_turn:
            possible_moves = cb.get_possible_moves(player_is_playing)
            print("Current Board State: \nAll possible places to move are signified by an 'o'.")
            cb.display(possible_moves)

            row, column = 0, 0
            while cb.board[row][column].upper() != player_is_playing.upper():
                initial_position = input("Enter the initial position (e.g., C8): ")
                row, column = cb.get_value_position_at_index(initial_position)

            possible_moves = cb.get_possible_moves(player_is_playing, initial_position)
            cb.display(possible_moves)

            move_position = input("Enter the move position (e.g., D7): ")
            initial_row, initial_column = cb.get_value_position_at_index(initial_position)
            move_row, move_column = cb.get_value_position_at_index(move_position)

            if cb.is_valid_move_for_position(initial_row, initial_column, move_row, move_column, player_is_playing):
                cb.switch_positions(initial_position, move_position)
        else:
            search_tree = SearchTreeNode(cb, cb.other(player_is_playing))
            search_tree.min_max_value()
            cb = search_tree.children[-1].current_board
            # pass

        if cb.state != 'U':
            if cb.state == "D":
                print(" I cant believe it you drew!!")
            else:
                if players_turn:
                    print("This is impossible!!!!")
                else:
                    print("Too easy loser!!!")

            print("Final Board State:")
            cb.display()
            game_is_finished = True

        players_turn = not players_turn


if __name__ == '__main__':
    play()
