# _*_ coding:utf-8 _*_

import pygame
import random
from sys import exit
from pygame.locals import *

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 800

class Bullet(pygame.sprite.Sprite):
    def __init__(self, bullet_img, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.midbottom = init_pos
        self.speed = 10

    def move(self):
        self.rect.top -= self.speed

class Player(pygame.sprite.Sprite):
    def __init__(self,plane_img, player_rect, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = [] #储存玩家飞机图片列表
        for i in range(len(player_rect)):
            self.image.append(plane_img.subsurface(player_rect[i]).convert_alpha())
            #subsurface根据位置截取图片 convert_alpha转换图片格式，同时隐藏鼠标
        self.rect = player_rect[0] #初始化图片所在的矩形
        self.rect.topleft = init_pos #初始化矩形的左上角坐标
        self.speed = 8
        self.bullets = pygame.sprite.Group() #玩家所发射的子弹的集合
        self.img_index = 0 #玩家飞机图片索引
        self.is_hit = False

    def shoot(self, bullet_img):
        bullet = Bullet(bullet_img, self.rect.midtop)
        self.bullets.add(bullet)

    def move_up(self): #向上移动考虑边界
        if self.rect.top <= 0:
            self.rect.top  = 0
        else:
            self.rect.top -= self.speed

    def move_down(self):
        if self.rect.top >= SCREEN_HEIGHT - self.rect.height:
            self.rect.top = SCREEN_HEIGHT - self.rect.height
        else:
            self.rect.top += self.speed

    def move_left(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        else:
            self.rect.left -= self.speed

    def move_right(self):
        if self.rect.right >= SCREEN_WIDTH - self.rect.width:
            self.rect.width = SCREEN_WIDTH - self.rect.width
        else:
            self.rect.left += self.speed

class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_img, enemy_down_imgs, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.rect.topleft = init_pos
        self.down_imgs = enemy_down_imgs
        self.speed = 2
        self.down_index = 0

    def move(self):
        self.rect.top += self.speed

#初始化
pygame.init()

screen = pygame.display.set_mode((480,800)) #设置界面大小

pygame.display.set_caption('打飞机') #界面标题

background = pygame.image.load('E:/python/PyCharm/train/PythonShootGame/resources/image/background.png').convert()#背景图

game_over = pygame.image.load('E:/python/PyCharm/train/PythonShootGame/resources/image/gameover.png') #游戏结束背景图

plane_img = pygame.image.load('E:/python/PyCharm/train/PythonShootGame/resources/image/shoot.png') #飞机图

player_rect = []
player_rect.append(pygame.Rect(0, 99, 102, 126))#截取玩家飞机图
player_rect.append(pygame.Rect(165, 360, 102, 126))
player_rect.append(pygame.Rect(165, 234, 102, 126))     # 玩家爆炸图片
player_rect.append(pygame.Rect(330, 624, 102, 126))
player_rect.append(pygame.Rect(330, 498, 102, 126))
player_rect.append(pygame.Rect(432, 624, 102, 126))
player_pos = [200, 600]
player = Player(plane_img, player_rect, player_pos)

bullet_rect = pygame.Rect(1004, 987, 9, 21)
bullet_img = plane_img.subsurface(bullet_rect)

enemy1_rect = pygame.Rect(534, 612, 57, 43)
enemy1_img = plane_img.subsurface(enemy1_rect)
enemy1_down_imgs = []
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(267, 347, 57, 43)))
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(873, 697, 57, 43)))
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(267, 296, 57, 43)))
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(930, 697, 57, 43)))

enemies1 = pygame.sprite.Group()

enemies_down = pygame.sprite.Group() #储存被击毁的飞机

shoot_frequency = 0
enemy_frequency = 0

player_down_index = 16 #玩家击中后的效果处理

score = 0

clock = pygame.time.Clock() #游戏循环帧率设置

running = True #判断游戏循环退出的参数

while running:
    clock.tick(60) #控制游戏最大帧率60

    if not player.is_hit:
        if shoot_frequency % 15 == 0:
            player.shoot(bullet_img)
        shoot_frequency += 1
        if shoot_frequency >= 15:
            shoot_frequency = 0

    if enemy_frequency % 50 == 0:
        enemy1_pos = [random.randint(0, SCREEN_WIDTH - enemy1_rect.width), 0]
        enemy1 = Enemy(enemy1_img, enemy1_down_imgs, enemy1_pos)
        enemies1.add(enemy1)
    enemy_frequency += 1
    if enemy_frequency >= 100:
        enemy_frequency = 0

    for bullet in player.bullets:
        bullet.move()
        if bullet.rect.bottom < 0:
            player.bullets.remove(bullet)

    for enemy in enemies1:
        enemy.move()
        if pygame.sprite.collide_circle(enemy, player):
            enemies_down.add(enemy)
            enemies1.remove(enemy)
            player.is_hit = True
            break

        if enemy.rect.top < 0:
            enemies1.remove(enemy)

    enemies1_down = pygame.sprite.groupcollide(enemies1, player.bullets, 1, 1)
    for enemy_down in enemies1_down:
        enemies_down.add(enemy_down)

    #绘制背景
    screen.fill(0)
    screen.blit(background, (0, 0))

    if not player.is_hit:
        screen.blit(player.image[player.img_index], player.rect)
        #更换图片索引使飞机有动画效果
        player.img_index = shoot_frequency // 8
    else:
        player.img_index = player_down_index // 8
        screen.blit(player.image[player.img_index], player.rect)
        player_down_index += 1
        if player_down_index > 47: #击中效果处理完后结束游戏
            running = False

    for enemy_down in enemies_down:
        if enemy_down.down_index == 0:
            pass
        if enemy_down.down_index > 7:
            enemies_down.remove(enemy_down)
            score += 1000
            continue
        screen.blit(enemy_down.down_imgs[enemy_down.down_index // 2], enemy_down.rect)
        enemy_down.down_index += 1

    player.bullets.draw(screen)
    enemies1.draw(screen)

    score_font = pygame.font.Font(None, 36)
    score_text = score_font.render(str(score), True, (128, 128, 128))
    text_rect = score_text.get_rect()
    text_rect.topleft = [10, 10]
    screen.blit(score_text, text_rect)

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    key_pressed = pygame.key.get_pressed()

    if key_pressed[K_w] or key_pressed[K_UP]:
        player.move_up()
    if key_pressed[K_s] or key_pressed[K_DOWN]:
        player.move_down()
    if key_pressed[K_a] or key_pressed[K_LEFT]:
        player.move_left()
    if key_pressed[K_d] or key_pressed[K_RIGHT]:
        player.move_right()

font = pygame.font.Font(None, 48)
text = font.render('Score: ' + str(score), True, (255, 0, 0))
text1_rect = text.get_rect()
text1_rect.centerx = screen.get_rect().centerx
text1_rect.centery = screen.get_rect().centery + 24
screen.blit(game_over, (0, 0))
screen.blit(text, text_rect)

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    pygame.display.update()















