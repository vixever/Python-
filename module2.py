#-*- coding:utf-8 -*-

import curses
from random import randrange, choice # generate and place new tile
from collections import defaultdict
import numpy,sys,random,pygame
from pygame.locals import*

Size = 4                                          #4*4行列
Block_WH = 110                                    #每个块的长度宽度
BLock_Space = 10                                  #两个块之间的间隙
Block_Size = Block_WH*Size+(Size+1)*BLock_Space
Matrix = numpy.zeros([Size,Size])                 #初始化矩阵4*4的0矩阵
Screen_Size = (Block_Size,Block_Size+110)
Title_Rect = pygame.Rect(0,0,Block_Size,110)      #设置标题矩形的大小
Score = 0

Block_Color = {
        0:(150,150,150),
        2:(255,255,255),
        4:(255,255,128),
        8:(255,255,0),
        16:(255,220,128),
        32:(255,220,0),
        64:(255,190,0),
        128:(255,160,0),
        256:(255,130,0),
        512:(255,100,0),
        1024:(255,70,0),
        2048:(255,40,0),
        4096:(255,10,0),
}                                                     #数块颜色


def drawBlock(screen,row,column,color,blocknum):
    font = pygame.font.SysFont('stxingkai',80)
    w = column*Block_WH+(column+1)*BLock_Space
    h = row*Block_WH+(row+1)*BLock_Space+110
    pygame.draw.rect(screen,color,(w,h,110,110))
    if blocknum != 0:
        w,fh = font.size(str(int(blocknum)))
        screen.blit(font.render(str(int(blocknum)),True,(0,0,0)),(w+(110-fw)/2,h+(110-fh)/2))


def drawSurface(cls,screen,matrix,score):
		pygame.draw.rect(screen,(255,255,255),Title_Rect)              #第一个参数是屏幕，第二个参数颜色，第三个参数rect大小，第四个默认参数
		font1 = pygame.font.SysFont('simsun',48)
		font2 = pygame.font.SysFont(None,32)
		screen.blit(font1.render('Score:',True,(255,127,0)),(20,25))     #font.render第一个参数是文本内容，第二个参数是否抗锯齿，第三个参数字体颜色
		screen.blit(font1.render('%s' % score,True,(255,127,0)),(170,25))
		screen.blit(font2.render('up',True,(255,127,0)),(360,20))
		screen.blit(font2.render('left  down  right',True,(255,127,0)),(300,50))
		a,b = matrix.shape
		for i in range(a):
			for j in range(b):
				cls.drawBlock(screen,i,j,Block_Color[matrix[i][j]],matrix[i][j])


letter_codes = [ord(ch) for ch in 'WASDRQwasdrq']
actions = ['Up', 'Left', 'Down', 'Right', 'Restart', 'Exit']
actions_dict = dict(zip(letter_codes, actions * 2))

def get_user_action(keyboard):
    char = "N"
    while char not in actions_dict:
        char = keyboard.getch()
    return actions_dict[char]

def transpose(field):
    return [list(row) for row in zip(*field)]

def invert(field):
    return [row[::-1] for row in field]

class GameField(object):
    def __init__(self, height=4, width=4, win=2048):
        self.height = height
        self.width = width
        self.win_value = win
        self.score = 0
        self.highscore = 0
        self.reset()

    def reset(self):
        if self.score > self.highscore:
            self.highscore = self.score
        self.score = 0
        self.field = [[0 for i in range(self.width)] for j in range(self.height)]
        self.spawn()
        self.spawn()

    def move(self, direction):
        def move_row_left(row):
            def tighten(row):   #把零散的非零单元挤到一块
                new_row=[i for i in row if i != 0]
                new_row += [0 for i in range(len(row) - len(new_row))]
                return new_row


            def merge(row):
                pair = False
                new_row = []
                for i in range(len(row)):
                    if pair:
                        new_row.append(2 * row[i])
                        self.score += 2 * row[i]
                        pair = False
                    else:
                        if i + 1 < len(row) and row[i] == row[i + 1]:
                            pair = True
                            new_row.append(0)
                        else:
                            new_row.append(row[i])
                assert len(new_row) == len(row)
                return new_row
            return tighten(merge(tighten(row)))

        moves = {}
        moves['Left']  = lambda field:                              \
                [move_row_left(row) for row in field]
        moves['Right'] = lambda field:                              \
                invert(moves['Left'](invert(field)))
        moves['Up']    = lambda field:                              \
                transpose(moves['Left'](transpose(field)))
        moves['Down']  = lambda field:                              \
                transpose(moves['Right'](transpose(field)))

        if direction in moves:
            if self.move_is_possible(direction):
                self.field = moves[direction](self.field)
                self.spawn()
                return True
            else:
                return False

    def is_win(self):
        return any(any(i >= self.win_value for i in row) for row in self.field)

    def is_gameover(self):
        return not any(self.move_is_possible(move) for move in actions)

    def spawn(self):
        new_element = 4 if randrange(100) > 89 else 2
        (i,j) = choice([(i,j) for i in range(self.width) for j in range(self.height) if self.field[i][j] == 0])
        self.field[i][j] = new_element

    def move_is_possible(self, direction):
        def row_is_left_movable(row):
            def change(i): # true if there'll be change in i-th tile
                if row[i] == 0 and row[i + 1] != 0: # Move
                    return True
                if row[i] != 0 and row[i + 1] == row[i]: # Merge
                    return True
                return False
            return any(change(i) for i in range(len(row) - 1))

        check = {}
        check['Left']  = lambda field:                              \
                any(row_is_left_movable(row) for row in field)

        check['Right'] = lambda field:                              \
                 check['Left'](invert(field))

        check['Up']    = lambda field:                              \
                check['Left'](transpose(field))

        check['Down']  = lambda field:                              \
                check['Right'](transpose(field))

        if direction in check:
            return check[direction](self.field)
        else:
            return False

def main(stdscr):
    pygame.init()
	screen = pygame.display.set_mode(Screen_Size,0,32)      #屏幕设置
	matrix = GameInit.initData(Size)
	currentscore = 0
	GameInit.drawSurface(screen,matrix,currentscore)
	pygame.display.update()
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit(0)
			elif event.type == pygame.KEYDOWN:
				actionObject = GameInit.keyDownPressed(event.key,matrix)     #创建各种动作类的对象
				matrix,score = actionObject.handleData()                     #处理数据
				currentscore += score
				GameInit.drawSurface(screen,matrix,currentscore)
				if matrix.min() != 0:
					GameInit.gameOver(matrix)
		pygame.display.update()
    def init():
        #重置游戏棋盘
        game_field.reset()
        return 'Game'

    def not_game(state):
        #画出 GameOver 或者 Win 的界面
        game_field.draw(stdscr)
        #读取用户输入得到action，判断是重启游戏还是结束游戏
        action = get_user_action(stdscr)
        responses = defaultdict(lambda: state) #默认是当前状态，没有行为就会一直在当前界面循环
        responses['Restart'], responses['Exit'] = 'Init', 'Exit' #对应不同的行为转换到不同的状态
        return responses[action]

    def game():
        #画出当前棋盘状态
        game_field.draw(stdscr)
        #读取用户输入得到action
        action = get_user_action(stdscr)

        if action == 'Restart':
            return 'Init'
        if action == 'Exit':
            return 'Exit'
        if game_field.move(action): # move successful
            if game_field.is_win():
                return 'Win'
            if game_field.is_gameover():
                return 'Gameover'
        return 'Game'


    state_actions = {
            'Init': init,
            'Win': lambda: not_game('Win'),
            'Gameover': lambda: not_game('Gameover'),
            'Game': game
        }

    curses.use_default_colors()

    # 设置终结状态最大数值为 32
    game_field = GameField(win=2048)


    state = 'Init'

    #状态机开始循环
    while state != 'Exit':
        state = state_actions[state]()

curses.wrapper(main)

