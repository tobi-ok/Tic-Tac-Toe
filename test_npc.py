import main

game_width = 3
game_height = 3

def test_attack():
    side = 'O'
    gamemode = 'pve'
    difficulty = 'medium'
    test_board = [
        ['O', None, 'X'],
        [None, None, None],
        ['O', None, None],
    ]
    expected_board = [
        ['O', None, 'X'],
        ['O', None, None],
        ['O', None, None],
    ]

    game = main.game(new_board=test_board, starting_side=side, board_width=game_width, board_height=game_height,\
                      chosen_side=side, gamemode=gamemode, difficulty=difficulty)
    game.NPC.execute()

    assert(game.current_board == expected_board)

def test_defend():
    side = 'X'
    gamemode = 'pve'
    difficulty = 'medium'
    test_board = [
        ['O', None, 'X'],
        [None, None, None],
        ['O', None, None],
    ]
    expected_board = [
        ['O', None, 'X'],
        ['X', None, None],
        ['O', None, None],
    ]

    game = main.game(new_board=test_board, starting_side=side, board_width=game_width, board_height=game_height,\
                      chosen_side=side, gamemode=gamemode, difficulty=difficulty)
    game.NPC.execute()

    assert(game.current_board == expected_board)