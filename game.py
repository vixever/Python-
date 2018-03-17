# -*- coding: utf-8 -*-
import pygame
from sys import exit
from pygame.locals import *
import random

# ������Ϸ��Ļ��С
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 800

# �ӵ���
class Bullet(pygame.sprite.Sprite):
    def __init__(self, bullet_img, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.midbottom = init_pos
        self.speed = 10

    def move(self):
        self.rect.top -= self.speed

# ��ҷɻ���
class Player(pygame.sprite.Sprite):
    def __init__(self, plane_img, player_rect, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = []                                 # �����洢��ҷɻ�ͼƬ���б�
        for i in range(len(player_rect)):
            self.image.append(plane_img.subsurface(player_rect[i]).convert_alpha())
        self.rect = player_rect[0]                      # ��ʼ��ͼƬ���ڵľ���
        self.rect.topleft = init_pos                    # ��ʼ�����ε����Ͻ�����
        self.speed = 8                                  # ��ʼ����ҷɻ��ٶȣ�������һ��ȷ����ֵ
        self.bullets = pygame.sprite.Group()            # ��ҷɻ���������ӵ��ļ���
        self.img_index = 0                              # ��ҷɻ�ͼƬ����
        self.is_hit = False                             # ����Ƿ񱻻���

    # �����ӵ�
    def shoot(self, bullet_img):
        bullet = Bullet(bullet_img, self.rect.midtop)
        self.bullets.add(bullet)

    # �����ƶ�����Ҫ�жϱ߽�
    def moveUp(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        else:
            self.rect.top -= self.speed

    # �����ƶ�����Ҫ�жϱ߽�
    def moveDown(self):
        if self.rect.top >= SCREEN_HEIGHT - self.rect.height:
            self.rect.top = SCREEN_HEIGHT - self.rect.height
        else:
            self.rect.top += self.speed

    # �����ƶ�����Ҫ�жϱ߽�
    def moveLeft(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        else:
            self.rect.left -= self.speed

    # �����ƶ�����Ҫ�жϱ߽�        
    def moveRight(self):
        if self.rect.left >= SCREEN_WIDTH - self.rect.width:
            self.rect.left = SCREEN_WIDTH - self.rect.width
        else:
            self.rect.left += self.speed

# �л���
class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_img, enemy_down_imgs, init_pos):
       pygame.sprite.Sprite.__init__(self)
       self.image = enemy_img
       self.rect = self.image.get_rect()
       self.rect.topleft = init_pos
       self.down_imgs = enemy_down_imgs
       self.speed = 2
       self.down_index = 0

    # �л��ƶ����߽��жϼ�ɾ������Ϸ��ѭ���ﴦ��
    def move(self):
        self.rect.top += self.speed

# ��ʼ��PyGame
pygame.init()

# ������Ϸ�����С������ͼƬ������
# ��Ϸ�������ش�С
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# ��Ϸ�������
pygame.display.set_caption('plane')

background = pygame.image.load('E:/python/PyCharm/train/PythonShootGame/resources/image/background.png').convert()#背景图

game_over = pygame.image.load('E:/python/PyCharm/train/PythonShootGame/resources/image/gameover.png') #游戏结束背景图

plane_img = pygame.image.load('E:/python/PyCharm/train/PythonShootGame/resources/image/shoot.png') #飞机图

# ������ҷɻ���ͬ״̬��ͼƬ�б�����ͼƬչʾΪ����Ч��
player_rect = []
player_rect.append(pygame.Rect(0, 99, 102, 126))        # ��ҷɻ�ͼƬ
player_rect.append(pygame.Rect(165, 360, 102, 126))
player_rect.append(pygame.Rect(165, 234, 102, 126))     # ��ұ�ըͼƬ
player_rect.append(pygame.Rect(330, 624, 102, 126))
player_rect.append(pygame.Rect(330, 498, 102, 126))
player_rect.append(pygame.Rect(432, 624, 102, 126))
player_pos = [200, 600]
player = Player(plane_img, player_rect, player_pos)

# �ӵ�ͼƬ
bullet_rect = pygame.Rect(1004, 987, 9, 21)
bullet_img = plane_img.subsurface(bullet_rect)

# �л���ͬ״̬��ͼƬ�б�����ͼƬչʾΪ����Ч��
enemy1_rect = pygame.Rect(534, 612, 57, 43)
enemy1_img = plane_img.subsurface(enemy1_rect)
enemy1_down_imgs = []
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(267, 347, 57, 43)))
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(873, 697, 57, 43)))
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(267, 296, 57, 43)))
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(930, 697, 57, 43)))

enemies1 = pygame.sprite.Group()

# �洢�����ٵķɻ���������Ⱦ���ٶ���
enemies_down = pygame.sprite.Group()

# ��ʼ��������л��ƶ�Ƶ��
shoot_frequency = 0
enemy_frequency = 0

# ��ҷɻ������к��Ч������
player_down_index = 16

# ��ʼ������
score = 0

# ��Ϸѭ��֡������
clock = pygame.time.Clock()

# �ж���Ϸѭ���˳��Ĳ���
running = True

# ��Ϸ��ѭ��
while running:
    # ������Ϸ���֡��Ϊ60
    clock.tick(60)

    # �����ӵ�����Ҫ���Ʒ���Ƶ��
    # �����ж���ҷɻ�û�б�����
    if not player.is_hit:
        if shoot_frequency % 15 == 0:
            player.shoot(bullet_img)
        shoot_frequency += 1
        if shoot_frequency >= 15:
            shoot_frequency = 0

    # ���ɵл�����Ҫ��������Ƶ��
    if enemy_frequency % 50 == 0:
        enemy1_pos = [random.randint(0, SCREEN_WIDTH - enemy1_rect.width), 0]
        enemy1 = Enemy(enemy1_img, enemy1_down_imgs, enemy1_pos)
        enemies1.add(enemy1)
    enemy_frequency += 1
    if enemy_frequency >= 100:
        enemy_frequency = 0

    for bullet in player.bullets:
        # �Թ̶��ٶ��ƶ��ӵ�
        bullet.move()
        # �ƶ�����Ļ��ɾ���ӵ�
        if bullet.rect.bottom < 0:
            player.bullets.remove(bullet)   

    for enemy in enemies1:
        #2. �ƶ��л�
        enemy.move()
        #3. �л�����ҷɻ���ײЧ������
        if pygame.sprite.collide_circle(enemy, player):
            enemies_down.add(enemy)
            enemies1.remove(enemy)
            player.is_hit = True
            break
        #4. �ƶ�����Ļ��ɾ���ɻ�    
        if enemy.rect.top < 0:
            enemies1.remove(enemy)

    #�л����ӵ�����Ч������
    # �������еĵл�������ӵ����ٵл�Group�У�������Ⱦ���ٶ���
    enemies1_down = pygame.sprite.groupcollide(enemies1, player.bullets, 1, 1)
    for enemy_down in enemies1_down:
        enemies_down.add(enemy_down)

    # ���Ʊ���
    screen.fill(0)
    screen.blit(background, (0, 0))

    # ������ҷɻ�
    if not player.is_hit:
        screen.blit(player.image[player.img_index], player.rect)
        # ����ͼƬ����ʹ�ɻ��ж���Ч��
        player.img_index = shoot_frequency // 8
    else:
        # ��ҷɻ������к��Ч������
        player.img_index = player_down_index // 8
        screen.blit(player.image[player.img_index], player.rect)
        player_down_index += 1
        if player_down_index > 47:
            # ����Ч��������ɺ���Ϸ����
            running = False

    # �л����ӵ�����Ч����ʾ
    for enemy_down in enemies_down:
        if enemy_down.down_index == 0:
            pass
        if enemy_down.down_index > 7:
            enemies_down.remove(enemy_down)
            score += 1000
            continue
        screen.blit(enemy_down.down_imgs[enemy_down.down_index // 2], enemy_down.rect)
        enemy_down.down_index += 1

    # ��ʾ�ӵ�
    player.bullets.draw(screen)
    # ��ʾ�л�
    enemies1.draw(screen)

    # ���Ƶ÷�
    score_font = pygame.font.Font(None, 36)
    score_text = score_font.render(str(score), True, (128, 128, 128))
    text_rect = score_text.get_rect()
    text_rect.topleft = [10, 10]
    screen.blit(score_text, text_rect)

    # ������Ļ
    pygame.display.update()

    # ������Ϸ�˳�
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            
    # ��ȡ�����¼����������Ұ�����
    key_pressed = pygame.key.get_pressed()

    # ��������¼����ƶ��ɻ���λ�ã�
    if key_pressed[K_w] or key_pressed[K_UP]:
        player.moveUp()
    if key_pressed[K_s] or key_pressed[K_DOWN]:
        player.moveDown()
    if key_pressed[K_a] or key_pressed[K_LEFT]:
        player.moveLeft()
    if key_pressed[K_d] or key_pressed[K_RIGHT]:
        player.moveRight()

# ��ϷGame Over����ʾ���յ÷�
font = pygame.font.Font(None, 48)
text = font.render('Score: '+ str(score), True, (255, 0, 0))
text_rect = text.get_rect()
text_rect.centerx = screen.get_rect().centerx
text_rect.centery = screen.get_rect().centery + 24
screen.blit(game_over, (0, 0))
screen.blit(text, text_rect)

# ��ʾ�÷ֲ�������Ϸ�˳�
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    pygame.display.update()


