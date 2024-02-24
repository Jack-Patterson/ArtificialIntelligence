from SearchTree.CA.CurrentBoard import CurrentBoard


def play():
    response = input("Do you wish to play first (y/n) ?")
    players_turn = (response == "y")

    cb = CurrentBoard()
    player_is_playing = 'W' if players_turn is True else 'B'

    print(player_is_playing)
    cb.display()

    print("\n" + cb.get_value_position_at_index('c4'))

    # initial_position = input("Enter the initial position (e.g., C8): ")
    # move_position = input("Enter the move position (e.g., D7): ")
    # cb.switch_positions(initial_position, move_position)

    cb.display()

    cb.all_possible_moves(player_is_playing)


if __name__ == '__main__':
    play()
