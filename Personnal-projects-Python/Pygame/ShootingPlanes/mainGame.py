# -*- coding: utf-8 -*-
"""
@author: Leo
@optimised by ZHANG Chenyu
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
enemy_down_sound = pygame.mixer.Sound('resources/sound/enemy1_down.wav')
boss_down_sound = pygame.mixer.Sound('resources/sound/enemy2_down.wav')
game_over_sound = pygame.mixer.Sound('resources/sound/game_over.wav')
bullet_sound.set_volume(0.3)
enemy_down_sound.set_volume(0.3)
game_over_sound.set_volume(0.3)
pygame.mixer.music.load('resources/sound/game_music.wav')
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.25)

# load the background
background = pygame.image.load('resources/image/background.png').convert()
game_over = pygame.image.load('resources/image/gameover.png')

filename = 'resources/image/shoot.png'
resources = pygame.image.load(filename)

# 玩家子弹
bullet_rect = pygame.Rect(1004, 987, 9, 21)
bullet_img = resources.subsurface(bullet_rect)
#敌人子弹
bullet_enemy_rect = pygame.Rect(68, 77, 10, 22)
bullet_enemy_img = resources.subsurface(bullet_enemy_rect)

# set the parameters of the players
player_rect = []   # 注意这个rect取的方法，第一二个点事是图片的左上角坐标，然后两个数值是宽和高
player_rect.append(pygame.Rect(0, 99, 102, 126))        # 玩家精灵图片区域
player_rect.append(pygame.Rect(165, 360, 102, 126))
player_rect.append(pygame.Rect(165, 234, 102, 126))     # 玩家爆炸精灵图片区域
player_rect.append(pygame.Rect(330, 624, 102, 126))
player_rect.append(pygame.Rect(330, 498, 102, 126))
player_rect.append(pygame.Rect(432, 624, 102, 126))
player_pos = [300, 500]
player = Player(resources, player_rect, player_pos)

# boss
boss_rect = pygame.Rect(165, 750, 170, 245)
boss_images = []
boss_images.append(resources.subsurface(pygame.Rect(165, 750, 170, 245))) # 如果在这里定义boss_image 那下面就没有问题。。。
boss_images.append(resources.subsurface(pygame.Rect(505, 750, 170, 250))) # 下面两张是射击图
boss_images.append(resources.subsurface(pygame.Rect(335, 750, 170, 250)))

boss_down_images = []
boss_down_images.append(resources.subsurface(pygame.Rect(5, 485, 160, 245)))
boss_down_images.append(resources.subsurface(pygame.Rect(5, 225, 160, 245)))
boss_down_images.append(resources.subsurface(pygame.Rect(842, 750, 160, 245)))
boss_down_images.append(resources.subsurface(pygame.Rect(168, 485, 160, 250)))
boss_down_images.append(resources.subsurface(pygame.Rect(675, 750, 165, 250)))
boss_down_images.append(resources.subsurface(pygame.Rect(0, 750, 160, 220)))

boss_pos = [screen.get_rect().centerx - 85, 0]

# 定义子弹对象使用的surface相关参数 define les parameters of the bullet
# bullet_rect = pygame.Rect(1004, 987, 9, 21)
# bullet_img = resources.subsurface(bullet_rect)

# 定义敌机对象使用的surface相关参数
enemy_rect = pygame.Rect(538, 612, 50, 40)
enemy_img = resources.subsurface(pygame.Rect(538, 612, 50, 40))
enemy_down_imgs = []
enemy_down_imgs.append(resources.subsurface(pygame.Rect(267, 347, 57, 43)))
enemy_down_imgs.append(resources.subsurface(pygame.Rect(873, 697, 57, 43)))
enemy_down_imgs.append(resources.subsurface(pygame.Rect(267, 296, 57, 43)))
enemy_down_imgs.append(resources.subsurface(pygame.Rect(930, 697, 57, 43)))

enemies = pygame.sprite.Group()
bosses = pygame.sprite.Group()

# 存储被击毁的飞机，用来渲染击毁精灵动画
enemies_down = pygame.sprite.Group()
#bosses_down = pygame.sprite.Group()
shoot_enemy_frequency = 10
shoot_frequency = 15
bullet_number = 5
recharge_time = 80
recharging = 0
enemy_frequency = 1
boss_frequency = 1
boss_flag = 0
boss_down_flag = 0
boss_once_flag = 0
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
    if enemy_frequency % 500 == 0:
        enemy_pos = [random.randint(0, SCREEN_WIDTH - enemy_rect.width), 0]
        enemy = Enemy(enemy_img, enemy_down_imgs, enemy_pos)
        enemies.add(enemy)    
    enemy_frequency += 1
    if enemy_frequency >= 51:
        enemy_frequency = 1

    # 移动子弹，若超出窗口范围则删除
    for bullet in player.bullets:
        bullet.move()
        if bullet.rect.bottom < 0:
            player.bullets.remove(bullet)
    if boss_once_flag == 1:
        for enemy_bullet in boss.enemy_bullets:
            enemy_bullet.move()
            if enemy_bullet.rect.bottom > 700:
                boss.enemy_bullets.remove(enemy_bullet)    
                
    # 生成boss
    if boss_frequency % 100 == 0  and boss_flag == 0:
        boss = Boss(resources, boss_rect, boss_pos)
        if boss_once_flag == 0:
            boss_once_flag = 1
        boss_flag = 1
        boss_down_flag = 0
        boss_frequency = 1

    if boss_flag == 1:
        boss.move((player.rect.left + player.rect.right) / 2 - (boss.rect.left + boss.rect.right) / 2)
        if boss.bullet_number > 0:
            if boss.shoot_frequency == 15:
                boss.shoot(bullet_enemy_img)
                bullet_sound.play()
                boss.shoot_frequency = 0
                boss.bullet_number -= 1
            else:
                boss.shoot_frequency += 1
            boss_img_index = boss.shoot_frequency // 8 + 1
            screen.blit(boss_images[boss_img_index], boss.rect)
        else:
            if boss.recharge == 0:
                boss.bullet_number = 5;
                boss.recharge = 200
            else:
                boss.recharge -= 1
            screen.blit(boss_images[0], boss.rect)
         # 和玩家相撞   
        if pygame.sprite.collide_circle(boss, player):
            player.is_hit = True
            game_over_sound.play()
            boss.life = 0
            
   #     attack = pygame.sprite.spritecollideany(boss, player.bullets) # 发现没有合适的函数，要去看文档！！
        if pygame.sprite.spritecollideany(boss, player.bullets):
        #if pygame.sprite.collide_circle(boss, player.bullets):
            boss.life -= 1
            player.bullets.remove(bullet) #要注意一旦击中就要删除子弹，不然下次循环还会把这颗子弹算上去
            # 注意一开始player和boss的子弹都是bullet，然后就有问题了，remove不掉了，后来把boss的子弹名字改成enemy_bullet就OK了
        if boss.life == 0:
            boss_flag = 0
            boss_down_flag = 1
            score += 10000
            boss_down_sound.play()       
            
    else:
        boss_frequency += 1
        
    # 移动敌机，若超出窗口范围则删除
    for enemy in enemies:
        enemy.move()
        # 判断玩家是否被击中
        if pygame.sprite.collide_circle(enemy, player):
            enemies_down.add(enemy)
            enemies.remove(enemy)
            player.is_hit = True
            game_over_sound.play()
            break
        if enemy.rect.top > SCREEN_HEIGHT:
            enemies.remove(enemy)
            
    # if boss_flag == 1 :        
        # if pygame.sprite.collide_circle(boss, player):
            # player.is_hit = True
            # game_over_sound.play()
            
    # boss绘制        
    # if boss_flag == 1:        
        # attack = pygame.sprite.spritecollideany(boss, player.bullets) # 发现没有合适的函数，要去看文档！！
        # if attack != None:
            # boss.life -= 1
            # player.bullets.remove(bullet) #要注意一旦击中就要删除子弹，不然下次循环还会把这颗子弹算上去
        # if boss.life == 0:
            # boss_flag = 0
            # boss_down_flag = 1
            # score += 10000
            # boss_down_sound.play()
            
    if boss_down_flag == 1:
        img_index = boss.down_index // 10
        screen.blit(boss_down_images[img_index], boss.rect)
        boss.down_index += 1
        if boss.down_index == 59:
            boss_down_flag = 0
     
    if boss_once_flag == 1:
        if pygame.sprite.spritecollideany(player, boss.enemy_bullets) :
            boss.enemy_bullets.remove(enemy_bullet)
            player.is_hit = True
            game_over_sound.play()
        boss.enemy_bullets.draw(screen)   
        
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
            
   # 将被击中的敌机对象添加到击毁敌机Group中，用来渲染击毁动画
    enemies_shot = pygame.sprite.groupcollide(enemies, player.bullets, 1, 1)
    for enemy_down in enemies_shot:
        enemies_down.add(enemy_down)
        
    # 绘制击毁动画
    for enemy_down in enemies_down:
        if enemy_down.down_index == 0:
            enemy_down_sound.play()
        if enemy_down.down_index > 7:
            enemies_down.remove(enemy_down)
            score += 1000
            continue
        screen.blit(enemy_down.down_imgs[enemy_down.down_index // 2], enemy_down.rect)
        enemy_down.down_index += 1

    # 绘制子弹和敌机
    player.bullets.draw(screen)
    enemies.draw(screen)
        

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
        position = SCREEN_WIDTH - 65
        for i in range(0, bullet_number):
            screen.blit(bullet_img, ((position + i * 12), 10))
    else:
        bullet_text = bullet_font.render('Recharging...' , True, (128, 128, 128))
    bullet_rect = bullet_text.get_rect()
    bullet_rect.topleft = [SCREEN_WIDTH - 120, 13] # 确定位置
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
