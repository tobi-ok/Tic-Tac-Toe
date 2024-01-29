import random
import math

game_height = 3
game_width = 3

class game:
    def __init__(self, gamemode='pve'):
        self.x_marker = ' X '
        self.o_marker = ' O '
        self.side_boarder_marker = ' | '
        self.line_boarder_marker = ' - '
        self.current_board = self.new_board()
        self.gamemode = gamemode
        self.isX = True if random.randint(0, 1) == 1 else False
        self.gameover = None

        self.render()

    def new_board(self):
        return [[None for _ in range(game_height)] for _ in range(game_width)]
    
    def is_match(self, values, value):
        for i in values:
            if i != value:
                return None
        
        return values[0]
    
    def check_game_state(self):
        '''
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
        
        n = [
            lambda i: self.is_match([self.current_board[i][0], self.current_board[1][1], self.current_board[2 - i][2]], True) or self.is_match([self.current_board[i][0], self.current_board[1][1], self.current_board[2 - i][2]], False),
            lambda i: self.is_match([self.current_board[i][0], self.current_board[i][1], self.current_board[i][2]], True) or self.is_match([self.current_board[i][0], self.current_board[i][1], self.current_board[i][2]], False),
            lambda i: self.is_match([self.current_board[0][i], self.current_board[1][i], self.current_board[2][i]], True) or self.is_match([self.current_board[0][i], self.current_board[1][i], self.current_board[2][i]], False),
        ]

        for i in range(3):
            for n_func in n:
                r = n_func(i)
                if r is not None:
                    print(f'Winner: {"X" if r else "O"}\nGame over!')
                    self.gameover = True
                    return

        for x in self.current_board:
            for y in x:
                if y ==  None:
                    return
                
        print('Tie!\nGame over!')
        self.gameover = True
    
    def get_coordinates(self, move):
        try:
            pmove = move.split(',')

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
                p1 = int(pmove[0])

                if p1 <= 0 or p1 >= 10:
                    print('Error - Invalid input')
                    return
                
                if p1 <= 3:
                    p1 = p1 if p1 - 1 < 0 else p1 - 1
                    return [0, p1]
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
                    
                    return [math.ceil(p1 / 3) - 1, (3 if p1 % 3 == 0 else p1 % 3) - 1]
        except:
            print('Error - Failed to process move')
            return
                                
    def new_move(self, input_move):
        coor = self.get_coordinates(input_move)

        if not coor:
            return

        x, y = coor[0], coor[1]
        spot = self.current_board[x][y]

        if spot is not None:
            print(f'{"X" if spot else "O"} is on {x, y}')
            return

        self.current_board[x][y] = self.isX
        self.isX = not self.isX

        self.render() 
        self.check_game_state()           
                
    def render(self):
        game_map = ''
        line_board_n = 5

        game_map += ' '*len(self.line_boarder_marker) + ' 1  2  3\n' + self.line_boarder_marker*line_board_n + '\n'
        
        for x in range(game_width):
            game_map += self.side_boarder_marker

            for y in range(game_height):
                spot = self.current_board[x][y]

                if spot == True:
                    game_map += self.x_marker
                elif spot == False:
                    game_map += self.o_marker
                else:
                    game_map += ' '*3

            game_map += self.side_boarder_marker + f'{x+1} \n'

        game_map += self.line_boarder_marker*line_board_n

        print(game_map)

ttt = game()

while not ttt.gameover:
    move = input('Input next move (ex. 1, 3 OR 1-9): ')
    ttt.new_move(move)
