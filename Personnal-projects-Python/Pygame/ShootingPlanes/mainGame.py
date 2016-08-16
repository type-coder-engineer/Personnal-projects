# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 11:05:00 2013

@author: Leo
"""

import pygame
from sys import exit
from pygame.locals import *
from gameRole import *
import random
# 注意存放文件的文件夹命名不要有中文，不然会找不到同一个文件夹下的文件，比如gameRole

# initialize the game
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('shootPlans')

# load the music
bullet_sound = pygame.mixer.Sound('resources/sound/bullet.wav')
enemy1_down_sound = pygame.mixer.Sound('resources/sound/enemy1_down.wav')
game_over_sound = pygame.mixer.Sound('resources/sound/game_over.wav')
bullet_sound.set_volume(0.3)
enemy1_down_sound.set_volume(0.3)
game_over_sound.set_volume(0.3)
pygame.mixer.music.load('resources/sound/game_music.wav')
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.25)

# load the background
background = pygame.image.load('resources/image/background.png').convert()
game_over = pygame.image.load('resources/image/gameover.png')

filename = 'resources/image/shoot.png'
plane_img = pygame.image.load(filename)

# set the parameters of the players
player_rect = []   # 注意这个rect取的方法，第一二个点事是图片的左上角坐标，然后两个数值是宽和高
player_rect.append(pygame.Rect(0, 99, 102, 126))        # 玩家精灵图片区域
player_rect.append(pygame.Rect(165, 360, 102, 126))
player_rect.append(pygame.Rect(165, 234, 102, 126))     # 玩家爆炸精灵图片区域
player_rect.append(pygame.Rect(330, 624, 102, 126))
player_rect.append(pygame.Rect(330, 498, 102, 126))
player_rect.append(pygame.Rect(432, 624, 102, 126))
player_pos = [200, 600]
player = Player(plane_img, player_rect, player_pos)

# boss
# (0,255,165,465) boss破损图
# （165, 750, 335, 995） boss 正常图
# boss_down_rect = []
# boss_down_rect.append(pygame.Rect(0, 225, 165, 240))
boss_image = plane_img.subsurface(pygame.Rect(165, 750, 170, 225))
boss_down_image = []
boss_down_image.append(plane_img.subsurface(pygame.Rect(0, 225, 165, 240)))
boss_pos = [screen.get_rect().centerx - 115, 0]

# 定义子弹对象使用的surface相关参数 define les parameters of the bullet
bullet_rect = pygame.Rect(1004, 987, 9, 21)
bullet_img = plane_img.subsurface(bullet_rect)

# 定义敌机对象使用的surface相关参数
enemy1_rect = pygame.Rect(534, 612, 57, 43)
enemy1_img = plane_img.subsurface(enemy1_rect)
enemy1_down_imgs = []
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(267, 347, 57, 43)))
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(873, 697, 57, 43)))
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(267, 296, 57, 43)))
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(930, 697, 57, 43)))

enemies1 = pygame.sprite.Group()
bosses1 = pygame.sprite.Group()

# 存储被击毁的飞机，用来渲染击毁精灵动画
enemies_down = pygame.sprite.Group()
bosses_down = pygame.sprite.Group()

shoot_frequency = 10
bullet_number = 5
recharge_time = 80
recharging = 0
enemy_frequency = 1
boss_frequency = 1
boss_flag = 0
player_down_index = 16

score = 0

clock = pygame.time.Clock()

running = True

while running:
    # 控制游戏最大帧率为60
    clock.tick(60)
        # 绘制背景
    screen.fill(0)
    screen.blit(background, (0, 0))
    
    # 生成敌机
    if enemy_frequency % 30 == 0:
        enemy1_pos = [random.randint(0, SCREEN_WIDTH - enemy1_rect.width), 0]
        enemy1 = Enemy(enemy1_img, enemy1_down_imgs, enemy1_pos)
        enemies1.add(enemy1)    
    enemy_frequency += 1
    if enemy_frequency >= 31:
        enemy_frequency = 1

    # 移动子弹，若超出窗口范围则删除
    for bullet in player.bullets:
        bullet.move()
        if bullet.rect.bottom < 0:
            player.bullets.remove(bullet)
            
    # boss
    if boss_frequency % 100 == 0  and boss_flag == 0:
        boss = Boss(boss_image, boss_down_image, boss_pos)
        boss_flag == 1
        boss_frequency = 1
        bosses1.add(boss)
 
    if boss_flag == 1:
        boss.move(player.rect.left - boss.rect.left)
    else:
        boss_frequency += 1
    # 移动敌机，若超出窗口范围则删除
    for enemy in enemies1:
        enemy.move()
        # 判断玩家是否被击中
        if pygame.sprite.collide_circle(enemy, player):
            enemies_down.add(enemy)
            enemies1.remove(enemy)
            player.is_hit = True
            game_over_sound.play()
            break
        if enemy.rect.top > SCREEN_HEIGHT:
            enemies1.remove(enemy)
            
    if boss_flag == 1:        
        if pygame.sprite.collide_circle(boss, player):
                bosses1.remove(boss)
                player.is_hit = True
                game_over_sound.play()
                break

    # 将被击中的敌机对象添加到击毁敌机Group中，用来渲染击毁动画
    enemies1_down = pygame.sprite.groupcollide(enemies1, player.bullets, 1, 1)
    for enemy_down in enemies1_down:
        enemies_down.add(enemy_down)

    # 绘制背景
    # screen.fill(0)
    # screen.blit(background, (0, 0))

    # 绘制玩家飞机
    if not player.is_hit:
        screen.blit(player.image[player.img_index], player.rect)
        # 更换图片索引使飞机有动画效果
        player.img_index = shoot_frequency // 8  # 注意这里有一个射子弹喷火的小动画，所以子弹频率设成了15
    else:
        player.img_index = player_down_index // 8 #用这种准循环来实现玩家飞机爆炸的效果
        screen.blit(player.image[player.img_index], player.rect)
        player_down_index += 1
        if player_down_index > 47:
            running = False  # 效果结束后这个循环就结束了

    # 绘制击毁动画
    for enemy_down in enemies_down:
        if enemy_down.down_index == 0:
            enemy1_down_sound.play()
        if enemy_down.down_index > 7:
            enemies_down.remove(enemy_down)
            score += 1000
            continue
        screen.blit(enemy_down.down_imgs[enemy_down.down_index // 2], enemy_down.rect)
        enemy_down.down_index += 1

    # 绘制子弹和敌机
    player.bullets.draw(screen)
    enemies1.draw(screen)
    bosses1.draw(screen)

    # 绘制得分
    score_font = pygame.font.Font(None, 36)  # 字体大小的
    score_text = score_font.render(str(score), True, (128, 128, 128))   # RGB三个通道，表示颜色是灰色
    text_rect = score_text.get_rect()
    text_rect.topleft = [10, 10]
    screen.blit(score_text, text_rect)
    # 绘制子弹数目
    bullet_font = pygame.font.Font(None, 24)
    if bullet_number > 0:
        bullet_text = bullet_font.render('Bullet: ' , True, (128, 128, 128))
        position = 415
        for i in range(0, bullet_number):
            screen.blit(bullet_img, ((position + i * 12), 10))
    else:
        bullet_text = bullet_font.render('Recharging...' , True, (128, 128, 128))
    bullet_rect = bullet_text.get_rect()
    bullet_rect.topleft = [360, 15] # 确定位置
    screen.blit(bullet_text, bullet_rect)
            
    # 监听键盘事件
    key_pressed = pygame.key.get_pressed()
    # 若玩家被击中，则无效
    if not player.is_hit:
        if key_pressed[K_SPACE]:
            if shoot_frequency % 15 == 0 and bullet_number > 0:
                bullet_sound.play()
                player.shoot(bullet_img)
                shoot_frequency = 0
                bullet_number -= 1
                
        if key_pressed[K_w] or key_pressed[K_UP]:
            player.moveUp()
        if key_pressed[K_s] or key_pressed[K_DOWN]:
            player.moveDown()
        if key_pressed[K_a] or key_pressed[K_LEFT]:
            player.moveLeft()
        if key_pressed[K_d] or key_pressed[K_RIGHT]:
            player.moveRight()
            
    if shoot_frequency < 15:  # 现在飞机射子弹的频率下来了
        shoot_frequency += 1
    if bullet_number == 0 and recharging < recharge_time:
        recharging += 1
        if recharging == recharge_time:
            bullet_number = 5
            recharging = 0
            
       # 更新屏幕
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()  

font = pygame.font.Font(None, 48)
text = font.render('Score: '+ str(score), True, (255, 0, 0))
text_rect = text.get_rect()
text_rect.centerx = screen.get_rect().centerx
text_rect.centery = screen.get_rect().centery + 24  # 这两句是用来调整score的位置的，现在是x轴上在
#中间，y轴上往下来一点
screen.blit(game_over, (0, 0))
screen.blit(text, text_rect)

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    pygame.display.update()
