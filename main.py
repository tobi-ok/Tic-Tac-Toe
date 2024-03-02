import random
import math
import time
import utils

GAME_WIDTH = 3
GAME_HEIGHT = 3
INPUT_MOVE_MESSAGE = 'Input next move (ex. 1, 3 OR 1-9): '
GAMEMODES = [
    'pvp',
    'pve',
    'eve'
]

class NPC:
    def __init__(self, game, difficulty=None):
        self.game = game
        self.mode = difficulty

        if difficulty is None:
            difficulty = utils.recursive_input('Choose NPC difficulty:\n1. Easy\n2. Hard\nSelect: ', [1, 2, 'easy', 'hard'])
            
            if difficulty == 1:
                difficulty = 'easy'
            elif difficulty == 2:
                difficulty = 'hard'

            self.mode = difficulty
                    
    def hard_play(self):
        # Setup scanners for all patterns
        current_side = self.game.current_side
        other_side = 'O' if self.game.turn_isX() else 'X'
        ours = [
            lambda i: self.game.almost_is_match([(i, 0), (1, 1), (2 - i, 2)], current_side),
            lambda i: self.game.almost_is_match([(i, 0), (i, 1), (i, 2)], current_side),
            lambda i: self.game.almost_is_match([(0, i), (1, i), (2, i)], current_side),
        ]
        theirs = [
            lambda i: self.game.almost_is_match([(i, 0), (1, 1), (2 - i, 2)], other_side),
            lambda i: self.game.almost_is_match([(i, 0), (i, 1), (i, 2)], other_side),
            lambda i: self.game.almost_is_match([(0, i), (1, i), (2, i)], other_side),
        ]

        # Execute scanners
        def find_winning_moves(l):
            for i in range(3):
                for func in l:
                    r = func(i)

                    # One move away from winning
                    if len(r) == 1:
                        x, y = r[0][0], r[0][1]
                        spot = self.game.current_board[y][x]

                        if spot is None:
                            # Strike
                            return r[0]
    
        defence_spot = find_winning_moves(theirs)
        attack_spot = find_winning_moves(ours)

        if defence_spot or attack_spot:
            # Play targeted move

            if attack_spot:
                return attack_spot
            elif defence_spot:
                return defence_spot
        else:
            # Play random move
            return self.easy_play()

    def easy_play(self):
        ''' Chooses random spot '''

        spots = []

        for x in range(self.game.width):
            for y in range(self.game.height):
                spot = self.game.current_board[y][x]

                if spot is None:
                    spots.append((x, y))

        if spots:
            return spots[random.randint(0, len(spots)-1)]

    def execute(self):
        ''' Make moves based on difficulty '''

        print(f'\nNPC {self.game.current_side} is playing...')

        time.sleep(random.random())
        coor = self.__getattribute__(f'{self.mode}_play')()
        self.game.new_move(coor)

class game:
    def __init__(self, board_width, board_height, **k):
        self.width = board_width
        self.height = board_height
        self.X_marker = ' X '
        self.O_marker = ' O '
        self.side_boarder_marker = ' | '
        self.line_boarder_marker = ' - '

        # Start new game
        self.current_board = k.get('new_board') or self.new_board()
        self.current_side = k.get('starting_side') or ('X' if random.randint(0, 1) == 1 else 'O')

        self.change_gamemode(k.get('gamemode'))

        if self.gamemode == 'eve':
            self.NPC = NPC(game=self, difficulty=k.get('difficulty'))
        elif self.gamemode == 'pve':
            chosen_side = k.get('chosen_side') or utils.recursive_input('Choose side:\n1. X\n2. O\nSelect: ', [1, 2, 'X', 'O'])
            
            if chosen_side == 1:
                chosen_side = 'X'
            elif chosen_side == 2:
                chosen_side = 'O'
            
            self.NPC = NPC(game=self, difficulty=k.get('difficulty'))

            # Random NPC first move
            if chosen_side != self.current_side:
                self.NPC.execute()
    
    def change_gamemode(self, gamemode):
        while True:
            gamemode = gamemode or input('Gamemodes:\n1. PvP\n2. PvE\n3. EvE\nSelect: ')

            if gamemode.lower() in GAMEMODES:
                self.gamemode = gamemode.lower()
                return

            try:
                gamemode = int(gamemode)
                gamemode = GAMEMODES[gamemode-1]
                self.gamemode = gamemode
                return
            except (IndexError, ValueError):
                print('Error - Invalid input')
            finally:
                gamemode = None
    
    def turn_isX(self):
        if self.current_side == 'X':
            return True
        
    def change_sides(self):
        if self.turn_isX():
            self.current_side = 'O'
        else:
            self.current_side = 'X'

    def pvp(self):
        user_input = input(INPUT_MOVE_MESSAGE)
        coor = self.get_user_coordinates(user_input)
        self.new_move(coor)

    def pve(self):
        user_input = input(INPUT_MOVE_MESSAGE)
        coor = self.get_user_coordinates(user_input)
        self.new_move(coor)

        # Render to see player's move
        self.render()
        
        # Run npc's move
        self.eve()

    def eve(self):
        self.NPC.execute()        
    
    def start(self):
        print('Starting game...')
        self.render()

        while not self.is_over():
            print(f"{self.current_side}'s turn")
            self.__getattribute__(self.gamemode)()
            self.render()

        # Show winning/tied game board        
        if self.winner:
            print(f'\nWinner: {self.winner}\nGame over!')
        else:
            print('\nTie!\nGame over!')

        self.render()

    def new_board(self):
        return [[None for _ in range(self.width)] for _ in range(self.height)]

    def almost_is_match(self, values, value):
        ''' Returns matching values '''
        missing = []

        for i in values:
            spot = self.current_board[i[1]][i[0]]

            if spot != value:
                missing.append(i)

        return missing
    
    def is_match(self, values, value):
        ''' True if all values match '''
        for i in values:
            spot = self.current_board[i[1]][i[0]]

            if spot != value:
                return
        
        return True
    
    def is_over(self):
        '''
            Winning patterns:
            
            # 1 (1, 1), 2 (2, 1), 3 (3, 1)
            # 4 (1, 2), 5 (2, 2), 6 (3, 2)
            # 7 (1, 3), 8 (2, 3), 9 (3, 3)

            # ↖   ↑   ↗
            #   ↘ ↓ ↙
            # i1 = i, 1
            # i2 = 2, 2
            # i3 = 4 - i, 3

            # ↑
            # ↓
            # i1 = i, 1
            # i2 = i, 2
            # i3 = i, 3

            # ←  →
            # i1 = 1, i
            # i2 = 2, i
            # i3 = 3, i
        '''
        
        # Setup scanners for winning patterns
        n = [
            lambda i: self.is_match([(i, 0), (1, 1), (2 - i, 2)], 'X') or self.is_match([(i, 0), (1, 1), (2 - i, 2)], 'O'),
            lambda i: self.is_match([(i, 0), (i, 1), (i, 2)], 'X') or self.is_match([(i, 0), (i, 1), (i, 2)], 'O'),
            lambda i: self.is_match([(0, i), (1, i), (2, i)], 'X') or self.is_match([(0, i), (1, i), (2, i)], 'O'),
        ]

        # Execute scanners
        for i in range(3):
            for n_func in n:
                r = n_func(i)
                if r:
                    self.winner = 'O' if self.turn_isX() else 'X'
                    return True

        # Check if board still has moves left
        for x in self.current_board:
            for y in x:
                if y == None:
                    return

        # No moves left, board full
        return True
    
    def get_user_coordinates(self, user_input):
        ''' Returns x, y coordinates from input x or input x, y '''

        while True:
            user_input = user_input or input(INPUT_MOVE_MESSAGE)

            try:
                pmove = user_input.split(',')

                # x, y
                if len(pmove) == 2:
                    x = int(pmove[0])
                    y = int(pmove[1])

                    if (x <= 0 or x >= 4) or (y <= 0 or y >= 4):
                        print('Error - Invalid input')
                        continue
                    
                    x = x if x - 1 < 0 else x - 1
                    y = y if y - 1 < 0 else y - 1

                    return [x, y]
                else:
                    # x
                    p1 = int(pmove[0])

                    if p1 <= 0 or p1 >= 10:
                        print('Error - Invalid input')
                        continue
                    
                    if p1 <= 3:
                        p1 = p1 if p1 - 1 < 0 else p1 - 1
                        return [p1, 0]
                    else:
                        # x = (a, b)

                        # 1, 2, 3 = 1
                        # 4, 5, 6 = 2
                        # 7, 8, 9 = 3
                        # a = ceil(i / 3) - 1
                        
                        # 1, 4, 7 = 1
                        # 2, 5, 8 = 2
                        # 3, 6, 9 = 3
                        # b = i % 3 if 0; 3
                        
                        return [(3 if p1 % 3 == 0 else p1 % 3) - 1, math.ceil(p1 / 3) - 1]
            except:
                print('Error - Failed to process move')
            finally:
                user_input = None

    def new_move(self, coor:tuple):
        if not coor:
            return
        
        x, y = coor[0], coor[1]
        spot = self.current_board[y][x]

        if spot is not None:
            print(f'{spot} is on {x, y}')
            return

        self.current_board[y][x] = self.current_side
        self.change_sides()
                
    def render(self):
        game_map = ''
        line_board_n = 5

        game_map += ' '*len(self.line_boarder_marker) + ' 1  2  3\n' + self.line_boarder_marker*line_board_n + '\n'
        
        for y in range(self.height):
            game_map += self.side_boarder_marker

            for x in range(self.width):
                spot = self.current_board[y][x]

                if spot is not None:
                    game_map += self.__getattribute__(f'{spot}_marker')
                else:
                    game_map += ' '*3

            game_map += self.side_boarder_marker + f'{y+1} \n'

        game_map += self.line_boarder_marker*line_board_n

        print('\n' + game_map)

if __name__ == '__main__':
    ttt = game(board_height=GAME_HEIGHT, board_width=GAME_WIDTH)
    ttt.start()
