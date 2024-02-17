import main
import sys

game_width = 3
game_height = 3
CL_inputs = {
    'gamemode': ['pvp', 'pve', 'eve'],
    'chosen_side': ['x', 'o'],
    'difficulty': ['easy', 'medium', 'hard']
}

argv = sys.argv[1:]
kwargs = {t: a for t, v in CL_inputs.items() for a in argv if a in v}
game = main.game(board_width=game_width, board_height=game_height, **kwargs)
game.start()
