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
            initial_row, initial_column = 0, 0
            move_row, move_column = 0, 0

            possible_moves = cb.get_positions_of_all_possible_moves(player_is_playing)
            print("Current Board State: \nAll possible places to move are signified by an 'o'.")
            cb.display(possible_moves)
            while cb.board[initial_row][initial_column].upper() != player_is_playing.upper():
                initial_position = input("Enter the initial position (e.g., C8): ")
                initial_row, initial_column = cb.get_value_position_at_index(initial_position)

            possible_moves = cb.get_positions_of_all_possible_moves(player_is_playing, initial_row, initial_column)
            print("All potential moves for the selected piece: \nAll possible places to move are signified by an 'o'.")
            cb.display(possible_moves)
            while (move_row, move_column) not in possible_moves:
                move_position = input("Enter the move position (e.g., D7): ")
                move_row, move_column = cb.get_value_position_at_index(move_position)

            cb.switch_positions(initial_row, initial_column, move_row, move_column)
        else:
            # search_tree = SearchTreeNode(cb, cb.other(player_is_playing))
            # search_tree.min_max_value()
            # cb = search_tree.children[-1].current_board
            pass

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
