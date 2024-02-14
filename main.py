import random
import math
import time

game_height = 3
game_width = 3

gamemodes = [
    'pvp',
    'pve',
    'eve'
]
input_move_message = 'Input next move (ex. 1, 3 OR 1-9): '

class NPC:
    def __init__(self, game, difficulty=None):
        self.game = game
        self.mode = 'easy'

    def easy_play(self):
        ''' Chooses random spot '''

        spots = []

        for y in range(self.game.height):
            for x in range(self.game.width):
                spot = self.game.current_board[y][x]

                if spot == None:
                    spots.append((x, y))

        return spots[random.randint(0, len(spots)-1)]

    def execute(self):
        ''' Make moves based on difficulty '''
        coor = self.__getattribute__(f'{self.mode}_play')()
        self.game.new_move(coor)

class game:
    def __init__(self, board_width, board_height):
        self.gamemode = None

        while True:
            self.gamemode = input('Gamemodes:\n1. PvP\n2. PvE\n3. EvE\nSelect: ')

            try:
                self.gamemode = int(self.gamemode)
                self.gamemode = gamemodes[self.gamemode-1]
                break
            except (IndexError, ValueError):
                print('Error - Invalid input')

        self.width = board_width
        self.height = board_height
        self.x_marker = ' X '
        self.o_marker = ' O '
        self.side_boarder_marker = ' | '
        self.line_boarder_marker = ' - '

        # Start new game
        self.current_board = self.new_board()
        self.isX = True if random.randint(0, 1) == 1 else False

        if self.gamemode == 'eve':
            self.NPC = NPC(self)
        elif self.gamemode == 'pve':
            def recursive_input(m, l):
                new_input = input(m).lower()

                if new_input in l:
                    return l[new_input]
                else:
                    try:
                        new_input = int(new_input)

                        for i in l:
                            if i == new_input:
                                return i
                            
                        print('Error - Invalid input')
                        return recursive_input(m, l)
                    except (ValueError, IndexError):
                        print('Error - Invalid input')
                        return recursive_input(m, l)

            chosen_side = recursive_input('Choose side:\n1. X\n2. O\nSelect: ', [1, 2, 'x', 'o'])
            
            if chosen_side == 1 or chosen_side == 'X':
                chosen_side = True
            elif chosen_side == 2 or chosen_side == 'O':
                chosen_side = False
            
            difficulty = recursive_input('Choose NPC difficulty:\n1. Easy\n2. Medium\n3. Hard\nSelect: ', [1, 2, 3, 'easy', 'medium', 'hard'])
            
            if difficulty == 1:
                difficulty = 'easy'
            elif difficulty == 2:
                difficulty = 'medium'
            elif difficulty == 3:
                difficulty = 'hard'

            self.NPC = NPC(game=self, difficulty=difficulty)

            # Random NPC first move
            if chosen_side != self.isX:
                self.NPC.execute()
    
    def pvp(self):
        user_input = input(input_move_message)
        coor = self.get_user_coordinates(user_input)
        self.new_move(coor)

    def pve(self):
        user_input = input(input_move_message)
        coor = self.get_user_coordinates(user_input)
        self.new_move(coor)
        self.NPC.execute()

    def eve(self):
        time.sleep(1.5)
        print(f"\nNPC {'X' if self.isX else 'O'}'s move:")
        self.NPC.execute()        
    
    def start(self):
        print('Starting game...')
        self.render()

        while not self.is_over():
            self.__getattribute__(self.gamemode)()
            self.render()

        # Show winning/tied game board
        self.render()

    def new_board(self):
        return [[None for _ in range(self.width)] for _ in range(self.height)]
    
    def is_match(self, values, value):
        for i in values:
            if i != value:
                return None
        
        return values[0]
    
    def is_over(self):
        '''
            Winning patterns:
            
            # 1 (1, 1), 2 (2, 1), 3 (3, 1)
            # 4 (1, 2), 5 (2, 2), 6 (3, 2)
            # 7 (1, 3), 8 (2, 3), 9 (3, 3)

            # ↖   ↑   ↗
            #   ↘ ↓ ↙
            # n1 = i, 1
            # n2 = 2, 2
            # n3 = 4 - i, 3

            # ↑
            # ↓
            # n1 = i, 1
            # n2 = i, 2
            # n3 = i, 3

            # ←  →
            # n1 = 1, i
            # n2 = 2, i
            # n3 = 3, i
        '''
        
        # Setup scanners for winning patterns
        n = [
            lambda i: self.is_match([self.current_board[i][0], self.current_board[1][1], self.current_board[2 - i][2]], True) or self.is_match([self.current_board[i][0], self.current_board[1][1], self.current_board[2 - i][2]], False),
            lambda i: self.is_match([self.current_board[i][0], self.current_board[i][1], self.current_board[i][2]], True) or self.is_match([self.current_board[i][0], self.current_board[i][1], self.current_board[i][2]], False),
            lambda i: self.is_match([self.current_board[0][i], self.current_board[1][i], self.current_board[2][i]], True) or self.is_match([self.current_board[0][i], self.current_board[1][i], self.current_board[2][i]], False),
        ]

        # Execute scanners
        for i in range(3):
            for n_func in n:
                r = n_func(i)
                if r is not None:
                    print(f'Winner: {"X" if r else "O"}\nGame over!')
                    return True

        # Check if board still has moves left
        for x in self.current_board:
            for y in x:
                if y == None:
                    return

        # No moves left, board full
        print('Tie!\nGame over!')
        return True
    
    def get_user_coordinates(self, user_input):
        ''' Returns x, y coordinates from input x or input x, y '''

        try:
            pmove = user_input.split(',')

            # x, y
            if len(pmove) == 2:
                x = int(pmove[0])
                y = int(pmove[1])

                if (x <= 0 or x >= 4) or (y <= 0 or y >= 4):
                    print('Error - Invalid input')
                    return
                
                x = x if x - 1 < 0 else x - 1
                y = y if y - 1 < 0 else y - 1

                return [x, y]
            else:
                # x
                p1 = int(pmove[0])

                if p1 <= 0 or p1 >= 10:
                    print('Error - Invalid input')
                    return
                
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
                    # b = i % 3 ? 0: 3
                    
                    return [(3 if p1 % 3 == 0 else p1 % 3) - 1, math.ceil(p1 / 3) - 1]
        except:
            print('Error - Failed to process move')
            return
                                
    def new_move(self, coor:tuple):
        if not coor:
            return
        
        x, y = coor[0], coor[1]
        spot = self.current_board[y][x]

        if spot is not None:
            print(f'{"X" if spot else "O"} is on {x, y}')
            return self.new_move(self.get_user_coordinates(input(input_move_message)))

        self.current_board[y][x] = self.isX
        self.isX = not self.isX
                
    def render(self):
        game_map = ''
        line_board_n = 5

        game_map += ' '*len(self.line_boarder_marker) + ' 1  2  3\n' + self.line_boarder_marker*line_board_n + '\n'
        
        for y in range(self.height):
            game_map += self.side_boarder_marker

            for x in range(self.width):
                spot = self.current_board[y][x]

                if spot == True:
                    game_map += self.x_marker
                elif spot == False:
                    game_map += self.o_marker
                else:
                    game_map += ' '*3

            game_map += self.side_boarder_marker + f'{y+1} \n'

        game_map += self.line_boarder_marker*line_board_n

        print(game_map)

if __name__ == '__main__':
    ttt = game(board_height=game_height, board_width=game_width)
    ttt.start()
