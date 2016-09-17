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
import os
# 注意存放文件的文件夹命名不要有中文，不然会找不到同一个文件夹下的文件，比如gameRole

    # initialize the game
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('shootPlanes')

# load the music
pygame.mixer.init()
bullet_sound = pygame.mixer.Sound('resources/sound/bullet.wav')
enemy_down_sound = pygame.mixer.Sound('resources/sound/enemy1_down.wav')
boss_down_sound = pygame.mixer.Sound('resources/sound/enemy22_down.wav')
boss_show_sound = pygame.mixer.Sound('resources/sound/boss_show.wav')
get_double_bullet_sound = pygame.mixer.Sound('resources/sound/get_double_bullet.wav')
get_bomb_sound  = pygame.mixer.Sound('resources/sound/get_bomb.wav')
bomb_sound = pygame.mixer.Sound('resources/sound/use_bomb.wav')
game_over_sound = pygame.mixer.Sound('resources/sound/game_over.wav')
#设置音量
bullet_sound.set_volume(0.3)
enemy_down_sound.set_volume(0.3)
game_over_sound.set_volume(0.3)
boss_show_sound.set_volume(0.3)
get_double_bullet_sound.set_volume(0.3)
get_bomb_sound.set_volume(0.3)
bomb_sound.set_volume(0.3)
bgm = pygame.mixer.Sound('resources/sound/game_music.wav')
bgm.play(-1, 0)
bgm.set_volume(0.1)
#设置游戏资源
background = pygame.image.load('resources/image/back_ground.png').convert()
gameover = pygame.image.load('resources/image/game_over.png')
gameicon = pygame.image.load('resources/image/myPlane32.png')
resources = pygame.image.load('resources/image/shoot.png')

pygame.display.set_icon(gameicon) #可以在标题栏上出现一个小飞机，注意icon最好是32x32 的png

#奖励
#无限子弹 (268, 398, 57, 87) 有效触碰(279, 455, 43, 30)
#炮弹 (103, 120, 60, 105) 有效触碰(103, 186, 53, 37)
double_bullet_rect = pygame.Rect(268, 398, 57, 87)
double_bullet_img = resources.subsurface(double_bullet_rect)
double_bullet_effect = pygame.Rect(279, 455, 43, 30)
bomb_rect = pygame.Rect(103, 120, 60, 105)
bomb_img = resources.subsurface(bomb_rect)
bomb_effect = pygame.Rect(103, 186, 53, 37)

# 玩家子弹
bullet_rect = pygame.Rect(1004, 987, 9, 21)
bullet_img = resources.subsurface(bullet_rect)
#敌人子弹
bullet_enemy_rect = pygame.Rect(68, 77, 10, 22)
bullet_enemy_img = resources.subsurface(bullet_enemy_rect)

# 玩家飞机的图片
player_rect = []   # 注意这个rect取的方法，第一二个点事是图片的左上角坐标，然后两个数值是宽和高
player_rect.append(pygame.Rect(0, 99, 102, 126))        # 玩家精灵图片区域
player_rect.append(pygame.Rect(165, 360, 102, 126))
player_rect.append(pygame.Rect(165, 234, 102, 126))     # 玩家爆炸精灵图片区域
player_rect.append(pygame.Rect(330, 624, 102, 126))
player_rect.append(pygame.Rect(330, 498, 102, 126))
player_rect.append(pygame.Rect(432, 624, 102, 126))
player_img = []
player_img.append(resources.subsurface(player_rect[0]))
player_img.append(resources.subsurface(player_rect[1]))
player_down_img = []
player_down_img.append(resources.subsurface(player_rect[2]))
player_down_img.append(resources.subsurface(player_rect[3]))
player_down_img.append(resources.subsurface(player_rect[4]))
player_down_img.append(resources.subsurface(player_rect[5]))
player_pos = [360, 580]

# boss图片
boss_rect = pygame.Rect(165, 750, 170, 245)
boss_img = []
boss_img.append(resources.subsurface(pygame.Rect(165, 750, 170, 245))) # 如果在这里定义boss_image 那下面就没有问题。。。
boss_img.append(resources.subsurface(pygame.Rect(505, 750, 170, 250))) # 下面两张是射击图
boss_img.append(resources.subsurface(pygame.Rect(335, 750, 170, 250)))

boss_down_img = []
boss_down_img.append(resources.subsurface(pygame.Rect(5, 485, 160, 245)))
boss_down_img.append(resources.subsurface(pygame.Rect(5, 225, 160, 245)))
boss_down_img.append(resources.subsurface(pygame.Rect(842, 750, 160, 245)))
boss_down_img.append(resources.subsurface(pygame.Rect(168, 485, 160, 250)))
boss_down_img.append(resources.subsurface(pygame.Rect(675, 750, 165, 250)))
boss_down_img.append(resources.subsurface(pygame.Rect(0, 750, 160, 220)))

boss_pos = [screen.get_rect().centerx - 85, 0]
boss_pos_left = [screen.get_rect().centerx - 285, 0]
boss_pos_right = [screen.get_rect().centerx + 115, 0]

# 定义敌机对象使用的surface相关参数
enemy1_rect = pygame.Rect(538, 612, 50, 40)
enemy1_img = resources.subsurface(pygame.Rect(538, 612, 50, 40))
enemy1_down_img = []
enemy1_down_img.append(resources.subsurface(pygame.Rect(267, 347, 57, 43)))
enemy1_down_img.append(resources.subsurface(pygame.Rect(873, 697, 57, 43)))
enemy1_down_img.append(resources.subsurface(pygame.Rect(267, 296, 57, 43)))
enemy1_down_img.append(resources.subsurface(pygame.Rect(930, 697, 57, 43)))

#enemy2 
enemy2_rect = pygame.Rect(0, 2, 69, 90)
enemy2_img = []
enemy2_img.append(resources.subsurface(pygame.Rect(0, 2, 69, 90)))
enemy2_img.append(resources.subsurface(pygame.Rect(432, 528, 69, 92)))
enemy2_down_img = []
enemy2_down_img.append(resources.subsurface(pygame.Rect(534, 654, 69, 92)))
enemy2_down_img.append(resources.subsurface(pygame.Rect(603, 654, 69, 92)))
enemy2_down_img.append(resources.subsurface(pygame.Rect(672, 653, 69, 92)))
enemy2_down_img.append(resources.subsurface(pygame.Rect(741, 660, 69, 85)))

def level1(clock, player):
    enemies1 = pygame.sprite.Group()  # enemy1的group
    awards = pygame.sprite.Group()  # 奖励的group
    enemies1_down = pygame.sprite.Group()  # 被击毁的就放入这个group中一起处理

    award_frequency = 1
    award_time = 100  # 第一个award出现
    boss_flag = 0
    boss_down_flag = 0
    boss_once_flag = 0
    myTime = 0
    running = 1
    global myScore #注意global变量的声明一定要放在定义这个变量的block中，我是在level1中第一次定义myScore = player.score的，所以要在level1中声明myScore
    global myGame
    
    while running:
        # 控制游戏最大帧率为60
        clock.tick(60)
        # 绘制背景
        screen.fill(0)
        screen.blit(background, (0, 0))
        
        if boss_flag == 0 and boss_down_flag == 0:
            if myTime % (100 - int(myTime / 50)) == 0:  # 通过这个数字来确定出现的频率
                enemy1_pos = [random.randint(0, SCREEN_WIDTH - enemy1_rect.width), 0]
                enemy1 = Enemy1(enemy1_img, enemy1_down_img, enemy1_pos)
                enemies1.add(enemy1)    
                
         #生成boss
        if myTime >= 200  and boss_flag == 0 and boss_down_flag == 0:
            boss = Boss_level1(boss_img, boss_down_img, boss_pos)
            boss_once_flag = 1
            boss_flag = 1
    
        if boss_flag == 1:
            if boss.flag_showup == 1:
                boss.move((player.rect.left + player.rect.right) / 2 - (boss.rect.left + boss.rect.right) / 2)
                if boss.bullet > 0:
                    if boss.shoot_frequency == 15:
                        boss.normal_shoot(bullet_enemy_img)
                        bullet_sound.play()
                        boss.shoot_frequency = 0
                        boss.bullet -= 1
                    else:
                        boss.shoot_frequency += 1
                    boss.index = boss.shoot_frequency // 8 + 1
                    screen.blit(boss.images[boss.index], boss.rect)
                else:
                    if boss.recharge == 0:
                        boss.bullet = boss.bullet_max;
                        boss.recharge = 200
                    else:
                        boss.recharge -= 1
                    screen.blit(boss.images[0], boss.rect)
            else:
                boss.show()
                if boss.flag_sound == 0:
                    boss_show_sound.play()
                    boss.flag_sound = 1
                screen.blit(boss.images[0], boss.rect)
                
            #boss和玩家相撞   
            if pygame.sprite.collide_rect(boss, player):
                player.is_hit = True
                game_over_sound.play()
                boss.life = 0
                
            #发现没有合适的函数，要去看文档！！
            if pygame.sprite.spritecollideany(boss, player.bullets):
                if boss.flag_showup == 1:
                    boss.life -= 1
                player.bullets.remove(bullet) #要注意一旦击中就要删除子弹，不然下次循环还会把这颗子弹算上去
                #注意一开始player和boss的子弹都是bullet，然后就有问题了，remove不掉了，后来把boss的子弹名字改成enemy_bullet就OK了
            if boss.life <= 0:
                boss_flag = 0
                boss_down_flag = 1
                player.score += 300
                boss_down_sound.play() 
                
        enemies1_shot = pygame.sprite.groupcollide(enemies1, player.bullets, 1, 1)
        for enemy1_down in enemies1_shot:
            enemies1_down.add(enemy1_down) 
            
        # 移动子弹，若超出窗口范围则删除
        for bullet in player.bullets:
            bullet.move()
            if bullet.rect.bottom < 0:
                player.bullets.remove(bullet)
        if boss_once_flag == 1:
            for enemy_bullet in boss.enemy_bullets:
                enemy_bullet.move()
                if enemy_bullet.rect.bottom > SCREEN_HEIGHT:
                    boss.enemy_bullets.remove(enemy_bullet)   
                    
        # 移动敌机，若超出窗口范围则删除
        for enemy1 in enemies1:
            enemy1.move()
            # 判断玩家是否被击中
            if pygame.sprite.collide_rect(enemy1, player):
                enemies1_down.add(enemy1)
                enemies1.remove(enemy1)
                player.is_hit = True
                game_over_sound.play()
                break
            if enemy1.rect.top > SCREEN_HEIGHT:
                enemies1.remove(enemy1)   

        if boss_once_flag == 1:
            if pygame.sprite.spritecollideany(player, boss.enemy_bullets) :
                boss.enemy_bullets.remove(enemy_bullet)
                player.is_hit = True
                game_over_sound.play()
            boss.enemy_bullets.draw(screen)   
            
    # 绘制敌机和boss击毁动画
        for enemy1_down in enemies1_down:
            if enemy1_down.down_index == 0:
                enemy_down_sound.play()
            if enemy1_down.down_index > 7:
                enemies1_down.remove(enemy1_down)
                player.score += 10
                continue
            screen.blit(enemy1_down.down_imgs[enemy1_down.down_index // 2], enemy1_down.rect)
            enemy1_down.down_index += 1     
 
        if boss_down_flag == 1:
            img_index = boss.down_index // 10
            screen.blit(boss_down_img[img_index], boss.rect)
            boss.down_index += 1
            if boss.down_index == 59:
                boss_down_flag = 0
                running = 0
                myGame = 1
                myScore = player.score

        # 生成奖励
        if award_frequency == award_time:
            type = random.randint(0, 20)
            if type < 15:
                position = [random.randint(0, SCREEN_WIDTH - double_bullet_rect.width), 0]
                award = Award(double_bullet_img, double_bullet_effect, position)
                award.kind = 1
            else:
                position = [random.randint(0, SCREEN_WIDTH - bomb_rect.width), 0]
                award = Award(bomb_img, bomb_effect, position)
                award.kind = 2
                
            awards.add(award)
            award_frequency = 1
            award_time = random.randint(400,800)
        else:
            award_frequency += 1
            
        for award in awards:
            award.move()
                #是否获得奖励
            if pygame.sprite.collide_rect(player, award):
                if award.kind == 1:
                    player.NL_bullet_time = 400
                    get_double_bullet_sound.play()
                else:
                    if player.bomb < player.bomb_max:
                        player.bomb += 1
                        get_bomb_sound.play()
                awards.remove(award)
            
            if award.rect.bottom > 700:
                awards.remove(award)
                
# 绘制玩家飞机
        if not player.is_hit:
            screen.blit(player.image[player.index], player.rect)
            # 更换图片索引使飞机有动画效果
            player.index = player.shoot_frequency // 8  # 注意这里有一个射子弹喷火的小动画，所以子弹频率设成了15
        else:  
            player.index = player.down_index // 8 #用这种准循环来实现玩家飞机爆炸的效果
            screen.blit(player.down_imgs[player.index], player.rect)
            player.down_index += 1
            if player.down_index > 31:
                running = 0  # 效果结束后这个循环就结束了
                myGame = 0
                myScore = player.score
                
 # 绘制子弹和和奖励和敌机
        player.bullets.draw(screen)
        awards.draw(screen)
        enemies1.draw(screen)
            
        # 绘制得分
        score_font = pygame.font.Font('freesansbold.ttf', 32)  # 字体大小的
        score_text = score_font.render(str(player.score), True, (128, 128, 128))   # RGB三个通道，表示颜色是灰色
        text_rect = score_text.get_rect()
        text_rect.topleft = [10, 5]
        screen.blit(score_text, text_rect)
        # 绘制boss血量
        if boss_flag == 1 and boss_down_flag == 0:
            boss_life_font = pygame.font.Font('freesansbold.ttf', 22)
            strbosslife = ''
            for i in range(0, boss.life):
                strbosslife += '[]'
            boss_life_text = boss_life_font.render('Boss level1: ' + strbosslife, True, (128, 128, 128))
            boss_life_rect = boss_life_text.get_rect()
            boss_life_rect.topleft = [30, SCREEN_HEIGHT - 40]
            screen.blit(boss_life_text, boss_life_rect)
                
        # 绘制子弹数目和bomb数目
        bullet_font = pygame.font.Font('freesansbold.ttf', 20)
        if player.NL_bullet_time > 0:
            bullet_text = bullet_font.render('Bullet: (^_^)', True, (128, 128, 128))
        else:
            if player.bullet > 0:
                bullet_text = bullet_font.render('Bullet: ' , True, (128, 128, 128))
                position = SCREEN_WIDTH - 65
                for i in range(0, player.bullet):
                    screen.blit(bullet_img, ((position + i * 12), 10))
            else:
                bullet_text = bullet_font.render('Recharging...' , True, (128, 128, 128))
        bulletText_rect = bullet_text.get_rect()
        bulletText_rect.topleft = [SCREEN_WIDTH - 130, 10] # 确定bullet的位置
        screen.blit(bullet_text, bulletText_rect)
        bomb_font = pygame.font.Font('freesansbold.ttf', 20)
        bomb_text = bomb_font.render('Bomb x ' + str(player.bomb), True, (128, 128, 128))
        bombText_rect = bomb_text.get_rect()
        bombText_rect.topleft = [SCREEN_WIDTH - 130, 35]
        screen.blit(bomb_text, bombText_rect)
        
        # 监听键盘事件
        key_pressed = pygame.key.get_pressed()
        # 若玩家被击中，则无效
        if not player.is_hit:
            if key_pressed[K_SPACE]:
                if player.shoot_frequency % 15 == 0 and (player.bullet > 0 or player.NL_bullet_time > 0):
                    bullet_sound.play()
                    player.shoot(bullet_img)
                    player.shoot_frequency = 0
                    player.bullet -= 1
                    #使用炸弹
            if key_pressed[K_b]:
                if player.bomb_frequency % 15 == 0 and player.bomb > 0:
                    bomb_sound.play()
                    player.bomb -= 1
                    player.bomb_frequency = 0
                    if boss_flag == 1:
                        boss.life -= boss.bomb_damage
                        for enemy_bullet in boss.enemy_bullets:
                            boss.enemy_bullets.remove(enemy_bullet)                       
                    for enemy1 in enemies1:
                        enemies1_down.add(enemy1)
                        enemies1.remove(enemy1)
                        
            if key_pressed[K_w] or key_pressed[K_UP]:
                player.moveUp()
            if key_pressed[K_s] or key_pressed[K_DOWN]:
                player.moveDown()
            if key_pressed[K_a] or key_pressed[K_LEFT]:
                player.moveLeft()
            if key_pressed[K_d] or key_pressed[K_RIGHT]:
                player.moveRight()
            
        if player.shoot_frequency < 15:  # 现在飞机射子弹的频率下来了
            player.shoot_frequency += 1
        if player.bomb_frequency < 15:
            player.bomb_frequency += 1
            #recharge the bullets
        if player.recharging < player.recharge_time and player.bullet < player.bullet_max:
            player.recharging += 1
            if player.recharging == player.recharge_time:
                player.bullet += 1
                player.recharging = 0
        player.NL_bullet_time -= 1
        if player.NL_bullet_time == 0:
            player.bullet = player.bullet_max
                
        # 更新屏幕
        pygame.display.update()
        myTime += 1
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()   

def level2(clock, player):     
    enemies1 = pygame.sprite.Group()  # enemy1的group
    awards = pygame.sprite.Group()  # 奖励的group
    enemies1_down = pygame.sprite.Group()  # 被击毁的就放入这个group中一起处理

    award_frequency = 1
    award_time = 100  # 第一个award出现
    boss_flag = 0
    boss1_down_flag = 0
    boss2_down_flag = 0
    boss_once_flag = 0
    myTime = 0
    running = 1
    global myScore
    global myGame
    
    while running:
        # 控制游戏最大帧率为60
        clock.tick(60)
        # 绘制背景
        screen.fill(0)
        screen.blit(background, (0, 0))
        
        if boss_flag == 0 and boss1_down_flag == 0 and boss2_down_flag == 0:
            if myTime % (80 - int(myTime / 40)) == 0:  # 通过这个数字来确定出现的频率
                enemy1_pos = [random.randint(0, SCREEN_WIDTH - enemy1_rect.width), 0]
                enemy1 = Enemy1(enemy1_img, enemy1_down_img, enemy1_pos)
                enemies1.add(enemy1)    
                
         #生成boss
        if myTime == 200:
            boss1 = Boss_level1(boss_img, boss_down_img, boss_pos_left)
            boss2 = Boss_level2(boss_img, boss_down_img, boss_pos_right)
            boss_once_flag = 1
            boss_flag = 1
    
        if boss_flag == 1:
            if boss1.flag_showup == 1 and boss1_down_flag == 0:
                boss1.move((player.rect.left + player.rect.right) / 2 - (boss1.rect.left + boss1.rect.right) / 2)
                if boss1.bullet > 0:
                    if boss1.shoot_frequency == 15:
                        boss1.normal_shoot(bullet_enemy_img)
                        bullet_sound.play()
                        boss1.shoot_frequency = 0
                        boss1.bullet -= 1
                    else:
                        boss1.shoot_frequency += 1
                    boss1.index = boss1.shoot_frequency // 8 + 1
                    screen.blit(boss1.images[boss1.index], boss1.rect)
                else:
                    if boss1.recharge == 0:
                        boss1.bullet = boss1.bullet_max;
                        boss1.recharge = 200
                    else:
                        boss1.recharge -= 1
                    screen.blit(boss1.images[0], boss1.rect)
            elif boss1.flag_showup == 0 and boss1_down_flag == 0:
                boss1.show()
                if boss1.flag_sound == 0:
                    boss_show_sound.play()
                    boss1.flag_sound = 1
                screen.blit(boss1.images[0], boss1.rect)
                # boss2
            if boss2.flag_showup == 1 and boss2_down_flag == 0:
                boss2.move()
                if boss2.bullet > 0:
                    if boss2.shoot_frequency == 15:
                        boss2.normal_shoot(bullet_enemy_img)
                        bullet_sound.play()
                        boss2.shoot_frequency = 0
                        boss2.bullet -= 1
                    else:
                        boss2.shoot_frequency += 1
                    boss2.index = boss2.shoot_frequency // 8 + 1
                    screen.blit(boss2.images[boss2.index], boss2.rect)
                else:
                    if boss2.recharge == 0:
                        boss2.bullet = boss2.bullet_max;
                        boss2.recharge = 200
                    else:
                        boss2.recharge -= 1
                    screen.blit(boss2.images[0], boss2.rect)
            elif boss2.flag_showup == 0 and boss2_down_flag == 0:
                boss2.show()
                if boss2.flag_sound == 0:
                    boss_show_sound.play()
                    boss2.flag_sound = 1
                screen.blit(boss2.images[0], boss2.rect)
                
            #boss和玩家相撞   
            if pygame.sprite.collide_rect(boss1, player):
                player.is_hit = True
                game_over_sound.play()
                boss1.life = 0
            if pygame.sprite.collide_rect(boss2, player):
                player.is_hit = True
                game_over_sound.play()
                boss2.life = 0         
                
            #发现没有合适的函数，要去看文档！！
            if pygame.sprite.spritecollideany(boss1, player.bullets):
                if boss1.flag_showup == 1:
                    boss1.life -= 1
                player.bullets.remove(bullet) #要注意一旦击中就要删除子弹，不然下次循环还会把这颗子弹算上去
                #注意一开始player和boss的子弹都是bullet，然后就有问题了，remove不掉了，后来把boss的子弹名字改成enemy_bullet就OK了
            if pygame.sprite.spritecollideany(boss2, player.bullets):
                if boss2.flag_showup == 1:
                    boss2.life -= 1
                player.bullets.remove(bullet)
                
            if boss1.life <= 0:
                if boss1_down_flag == 0:
                    player.score += 300
                    boss1_down_flag = 1
                    boss_down_sound.play() 
            if boss2.life <= 0:
                if boss2_down_flag == 0: 
                    player.score += 300
                    boss2_down_flag = 1
                    boss_down_sound.play() 
            if (boss1_down_flag == 1 or boss1_down_flag == 2) and (boss2_down_flag == 1 or boss2_down_flag == 2):
                boss_flag = 0
                
        enemies1_shot = pygame.sprite.groupcollide(enemies1, player.bullets, 1, 1)
        for enemy1_down in enemies1_shot:
            enemies1_down.add(enemy1_down) 
            
        # 移动子弹，若超出窗口范围则删除
        for bullet in player.bullets:
            bullet.move()
            if bullet.rect.bottom < 0:
                player.bullets.remove(bullet)
        if boss_once_flag == 1:
            for enemy_bullet in boss1.enemy_bullets:
                enemy_bullet.move()
                if enemy_bullet.rect.bottom > SCREEN_HEIGHT:
                    boss1.enemy_bullets.remove(enemy_bullet)   
            for enemy_bullet in boss2.enemy_bullets:
                enemy_bullet.move()
                if enemy_bullet.rect.bottom > SCREEN_HEIGHT:
                    boss2.enemy_bullets.remove(enemy_bullet)   
                    
        # 移动敌机，若超出窗口范围则删除
        for enemy1 in enemies1:
            enemy1.move()
            # 判断玩家是否被击中
            if pygame.sprite.collide_rect(enemy1, player):
                enemies1_down.add(enemy1)
                enemies1.remove(enemy1)
                player.is_hit = True
                game_over_sound.play()
                break
            if enemy1.rect.top > SCREEN_HEIGHT:
                enemies1.remove(enemy1)   

        if boss_once_flag == 1:
            if pygame.sprite.spritecollideany(player, boss1.enemy_bullets) :
                boss1.enemy_bullets.remove(enemy_bullet)
                player.is_hit = True
                game_over_sound.play()
            boss1.enemy_bullets.draw(screen)   
            if pygame.sprite.spritecollideany(player, boss2.enemy_bullets) :
                boss2.enemy_bullets.remove(enemy_bullet)
                player.is_hit = True
                game_over_sound.play()
            boss2.enemy_bullets.draw(screen)   
            
    # 绘制敌机和boss击毁动画
        for enemy1_down in enemies1_down:
            if enemy1_down.down_index == 0:
                enemy_down_sound.play()
            if enemy1_down.down_index > 7:
                enemies1_down.remove(enemy1_down)
                player.score += 10
                continue
            screen.blit(enemy1_down.down_imgs[enemy1_down.down_index // 2], enemy1_down.rect)
            enemy1_down.down_index += 1     
 
        if boss1_down_flag == 1:
            img_index1 = boss1.down_index // 10
            screen.blit(boss1.down_images[img_index1], boss1.rect)
            boss1.down_index += 1
            if boss1.down_index == 59:
                boss1_down_flag = 2
                if boss_flag == 0:
                    running = 0
                    myGame = 1
                    myScore = player.score
                
        if boss2_down_flag == 1:
            img_index2 = boss2.down_index // 10
            screen.blit(boss2.down_images[img_index2], boss2.rect)
            boss2.down_index += 1
            if boss2.down_index == 59:
                boss2_down_flag = 2
                if boss_flag == 0:
                    running = 0
                    myGame = 1
                    myScore = player.score
              
        # 生成奖励
        if award_frequency == award_time:
            type = random.randint(0, 20)
            if type < 15:
                position = [random.randint(0, SCREEN_WIDTH - double_bullet_rect.width), 0]
                award = Award(double_bullet_img, double_bullet_effect, position)
                award.kind = 1
            else:
                position = [random.randint(0, SCREEN_WIDTH - bomb_rect.width), 0]
                award = Award(bomb_img, bomb_effect, position)
                award.kind = 2
                
            awards.add(award)
            award_frequency = 1
            award_time = random.randint(400,800)
        else:
            award_frequency += 1
            
        for award in awards:
            award.move()
                #是否获得奖励
            if pygame.sprite.collide_rect(player, award):
                if award.kind == 1:
                    player.NL_bullet_time = 400
                    get_double_bullet_sound.play()
                else:
                    if player.bomb < player.bomb_max:
                        player.bomb += 1
                        get_bomb_sound.play()
                awards.remove(award)
            
            if award.rect.bottom > 700:
                awards.remove(award)
                
# 绘制玩家飞机
        if not player.is_hit:
            screen.blit(player.image[player.index], player.rect)
            # 更换图片索引使飞机有动画效果
            player.index = player.shoot_frequency // 8  # 注意这里有一个射子弹喷火的小动画，所以子弹频率设成了15
        else:  
            player.index = player.down_index // 8 #用这种准循环来实现玩家飞机爆炸的效果
            screen.blit(player.down_imgs[player.index], player.rect)
            player.down_index += 1
            if player.down_index > 31:
                running = 0  # 效果结束后这个循环就结束了
                myGame = 0
                myScore = player.score
                
 # 绘制子弹和和奖励和敌机
        player.bullets.draw(screen)
        awards.draw(screen)
        enemies1.draw(screen)
            
        # 绘制得分
        score_font = pygame.font.Font('freesansbold.ttf', 32)  # 字体大小的
        score_text = score_font.render(str(player.score), True, (128, 128, 128))   # RGB三个通道，表示颜色是灰色
        text_rect = score_text.get_rect()
        text_rect.topleft = [10, 5]
        screen.blit(score_text, text_rect)
        # 绘制boss血量
        if boss_flag == 1 and boss1_down_flag == 0:
            boss_life_font = pygame.font.Font('freesansbold.ttf', 22)
            strbosslife = ''
            for i in range(0, boss1.life):
                strbosslife += '[]'
            boss_life_text = boss_life_font.render('Boss1 level2: ' + strbosslife, True, (128, 128, 128))
            boss_life_rect = boss_life_text.get_rect()
            boss_life_rect.topleft = [30, SCREEN_HEIGHT - 70]
            screen.blit(boss_life_text, boss_life_rect)
            
        if boss_flag == 1 and boss2_down_flag == 0:
            boss_life_font = pygame.font.Font('freesansbold.ttf', 22)
            strbosslife = ''
            for i in range(0, boss2.life):
                strbosslife += '[]'
            boss_life_text = boss_life_font.render('Boss2 level2: ' + strbosslife, True, (128, 128, 128))
            boss_life_rect = boss_life_text.get_rect()
            boss_life_rect.topleft = [30, SCREEN_HEIGHT - 40]
            screen.blit(boss_life_text, boss_life_rect)       
            
        # 绘制子弹数目和bomb数目
        bullet_font = pygame.font.Font('freesansbold.ttf', 20)
        if player.NL_bullet_time > 0:
            bullet_text = bullet_font.render('Bullet: (^_^)', True, (128, 128, 128))
        else:
            if player.bullet > 0:
                bullet_text = bullet_font.render('Bullet: ' , True, (128, 128, 128))
                position = SCREEN_WIDTH - 65
                for i in range(0, player.bullet):
                    screen.blit(bullet_img, ((position + i * 12), 10))
            else:
                bullet_text = bullet_font.render('Recharging...' , True, (128, 128, 128))
        bulletText_rect = bullet_text.get_rect()
        bulletText_rect.topleft = [SCREEN_WIDTH - 130, 10] # 确定bullet的位置
        screen.blit(bullet_text, bulletText_rect)
        bomb_font = pygame.font.Font('freesansbold.ttf', 20)
        bomb_text = bomb_font.render('Bomb x ' + str(player.bomb), True, (128, 128, 128))
        bombText_rect = bomb_text.get_rect()
        bombText_rect.topleft = [SCREEN_WIDTH - 130, 35]
        screen.blit(bomb_text, bombText_rect)
        
        # 监听键盘事件
        key_pressed = pygame.key.get_pressed()
        # 若玩家被击中，则无效
        if not player.is_hit:
            if key_pressed[K_SPACE]:
                if player.shoot_frequency % 15 == 0 and (player.bullet > 0 or player.NL_bullet_time > 0):
                    bullet_sound.play()
                    player.shoot(bullet_img)
                    player.shoot_frequency = 0
                    player.bullet -= 1
                    #使用炸弹
            if key_pressed[K_b]:
                if player.bomb_frequency % 15 == 0 and player.bomb > 0:
                    bomb_sound.play()
                    player.bomb -= 1
                    player.bomb_frequency = 0
                    if boss_flag == 1:
                        boss1.life -= boss1.bomb_damage
                        boss2.life -= boss2.bomb_damage
                        for enemy_bullet in boss1.enemy_bullets:
                            boss1.enemy_bullets.remove(enemy_bullet)  
                        for enemy_bullet in boss2.enemy_bullets:
                            boss2.enemy_bullets.remove(enemy_bullet)                                   
                    for enemy1 in enemies1:
                        enemies1_down.add(enemy1)
                        enemies1.remove(enemy1)
                        
            if key_pressed[K_w] or key_pressed[K_UP]:
                player.moveUp()
            if key_pressed[K_s] or key_pressed[K_DOWN]:
                player.moveDown()
            if key_pressed[K_a] or key_pressed[K_LEFT]:
                player.moveLeft()
            if key_pressed[K_d] or key_pressed[K_RIGHT]:
                player.moveRight()
            
        if player.shoot_frequency < 15:  # 现在飞机射子弹的频率下来了
            player.shoot_frequency += 1
        if player.bomb_frequency < 15:
            player.bomb_frequency += 1
            #recharge the bullets
        if player.recharging < player.recharge_time and player.bullet < player.bullet_max:
            player.recharging += 1
            if player.recharging == player.recharge_time:
                player.bullet += 1
                player.recharging = 0
        player.NL_bullet_time -= 1
        if player.NL_bullet_time == 0:
            player.bullet = player.bullet_max
                
        # 更新屏幕
        pygame.display.update()
        myTime += 1
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()      

def level3(clock, player):
    enemies1 = pygame.sprite.Group()  # enemy1的group
    enemies2 = pygame.sprite.Group()  # enemy2的group
    awards = pygame.sprite.Group()  # 奖励的group
    enemies1_down = pygame.sprite.Group()  # 被击毁的就放入这个group中一起处理
    enemies2_down = pygame.sprite.Group()
    enemy2_once_flag = 0
    award_frequency = 1
    award_time = 100  # 第一个award出现
    boss_flag = 0
    boss_down_flag = 0
    boss_once_flag = 0
    myTime = 0
    running = 1
    begin = 1
    global myScore 
    global myGame
    
    while running:
        # 控制游戏最大帧率为60
        clock.tick(60)
        # 绘制背景
        screen.fill(0)
        screen.blit(background, (0, 0))
        # 生成两种敌人
        if boss_flag == 0 and boss_down_flag == 0:
            if myTime % (100 - int(myTime / 40)) == 0:  # 通过这个数字来确定出现的频率
                enemy1_pos = [random.randint(0, SCREEN_WIDTH - enemy1_rect.width), 0]
                enemy1 = Enemy1(enemy1_img, enemy1_down_img, enemy1_pos)
                enemies1.add(enemy1)    
                
        if boss_flag == 0 and boss_down_flag == 0:
            if myTime % 2000 == 0:  # 通过这个数字来确定出现的频率
                enemy2_pos = [random.randint(0, SCREEN_WIDTH - enemy2_rect.width), 0]
                enemy2 = Enemy2(enemy2_img, enemy2_down_img, enemy2_pos)
                enemies2.add(enemy2)
                if enemy2_once_flag == 0:
                    enemy2_once_flag = 1
                
         #生成boss
        if myTime == 200:
            boss = Boss_level3(boss_img, boss_down_img, boss_pos)
            boss_once_flag = 1
            boss_flag = 1
    
        if boss_flag == 1:
            if boss.flag_showup == 1:
                target = (player.rect.left + player.rect.right) / 2 - (boss.rect.left + boss.rect.right) / 2
                playerleft = list(player.rect.topleft)
                playerright = list(player.rect.topright)
                positionx = (playerleft[0] + playerright[0]) / 2
                positiony = playerleft[1]
                # print positiony
                if begin == 1:
                    if positionx > 300 and positionx < 500:
                        boss.teleportation_defence(positionx)
                    begin = 0
                if boss.bullet > 6 and boss.mode == 0:
                    boss.mode = 1
                    boss.ishit_flag = 0
                elif boss.bullet < 3 and boss.mode == 1:
                    boss.mode = 0  
                    #瞬间移动
                if boss.ishit_flag == 1 and boss.mode == 0 and boss.teleportation == 0:
                    boss.teleportation_defence(positionx)
                    boss.ishit_flag = 0
                    boss.teleportation = boss.teleportation_recharge
                elif boss.mode == 1 and abs(target) > 200 and boss.teleportation == 0 and positiony < 350:
                    boss.teleportation_attack(positionx)
                    boss.teleportation = boss.teleportation_recharge
                    
                if boss.teleportation > 0:
                    boss.teleportation -= 1
                if boss.ishit_flag == 1:
                    boss.ishit_flag = 0  # 只是那一下才会触发，之后就没有ishit的flag了
                    
                boss.move(target, boss.mode)
                
                if boss.bullet > 0 and abs(target) < 100:
                    if boss.shoot_frequency == 15:
                        boss.normal_shoot(bullet_enemy_img)
                        bullet_sound.play()
                        boss.shoot_frequency = 0
                        boss.bullet -= 1
                    else:
                        boss.shoot_frequency += 1
                    boss.index = boss.shoot_frequency // 8 + 1
                    screen.blit(boss.images[boss.index], boss.rect)
                    
                if boss.bullet < boss.bullet_max:
                    if boss.recharging == 0:
                        boss.bullet += 1
                        boss.recharging = boss.recharge_time
                    else:
                        boss.recharging -= 1
                screen.blit(boss.images[0], boss.rect)
            else:
                boss.show()
                if boss.flag_sound == 0:
                    boss_show_sound.play()
                    boss.flag_sound = 1
                screen.blit(boss.images[0], boss.rect)
                
            #boss和玩家相撞   
            if pygame.sprite.collide_rect(boss, player):
                player.is_hit = True
                game_over_sound.play()
                boss.life = 0
                
            #发现没有合适的函数，要去看文档！！
            if pygame.sprite.spritecollideany(boss, player.bullets):
                if boss.flag_showup == 1:
                    boss.life -= 1
                    boss.ishit_flag = 1
                player.bullets.remove(bullet) #要注意一旦击中就要删除子弹，不然下次循环还会把这颗子弹算上去
                #注意一开始player和boss的子弹都是bullet，然后就有问题了，remove不掉了，后来把boss的子弹名字改成enemy_bullet就OK了
            if boss.life <= 0:
                boss_flag = 0
                boss_down_flag = 1
                player.score += 600
                boss_down_sound.play() 
                
        if boss_once_flag == 1:
            if pygame.sprite.spritecollideany(player, boss.enemy_bullets) :
                boss.enemy_bullets.remove(enemy_bullet)
                player.is_hit = True
                game_over_sound.play()
            boss.enemy_bullets.draw(screen)   
                            
        enemies1_shot = pygame.sprite.groupcollide(enemies1, player.bullets, 1, 1)
        for enemy1_down in enemies1_shot:
            enemies1_down.add(enemy1_down) 
            
        enemies2_shot = pygame.sprite.groupcollide(enemies2, player.bullets, 1, 1)
        for enemy2_down in enemies2_shot:
            enemies2_down.add(enemy2_down)          
            
        # 移动子弹，若超出窗口范围则删除
        for bullet in player.bullets:
            bullet.move()
            if bullet.rect.bottom < 0:
                player.bullets.remove(bullet)
        if boss_once_flag == 1:
            for enemy_bullet in boss.enemy_bullets:
                enemy_bullet.move()
                if enemy_bullet.rect.bottom > SCREEN_HEIGHT:
                    boss.enemy_bullets.remove(enemy_bullet)   
        if enemy2_once_flag == 1:
            for enemy_bullet in enemy2.enemy_bullets:
                enemy_bullet.move()
                if enemy_bullet.rect.bottom > SCREEN_HEIGHT:
                    enemy2.enemy_bullets.remove(enemy_bullet)   
                    
        # 移动敌机，若超出窗口范围则删除
        for enemy1 in enemies1:
            enemy1.move()
            # 判断玩家是否被击中
            if pygame.sprite.collide_rect(enemy1, player):
                enemies1_down.add(enemy1)
                enemies1.remove(enemy1)
                player.is_hit = True
                game_over_sound.play()
                break
            if enemy1.rect.top > SCREEN_HEIGHT:
                enemies1.remove(enemy1)   

        for enemy2 in enemies2:
            enemy2.move((player.rect.left + player.rect.right) / 2 - (enemy2.rect.left + enemy2.rect.right) / 2)
            if enemy2.shoot_frequency == enemy2.recharge_time:
                enemy2.shoot(bullet_enemy_img)
                enemy2.shoot_frequency = 0
                bullet_sound.play()
            else:
                enemy2.shoot_frequency += 1
            if enemy2.shoot_frequency > enemy2.recharge_time - 10:
                enemy2.img_index = 1
            else:
                enemy2.img_index = 0
            screen.blit(enemy2.images[enemy2.img_index], enemy2.rect)
            # 判断玩家是否被击中
            if pygame.sprite.collide_rect(enemy2, player):
                enemies2_down.add(enemy2)
                enemies2.remove(enemy2)
                player.is_hit = True
                game_over_sound.play()
                break
            if enemy2.rect.top > SCREEN_HEIGHT:
                enemies2.remove(enemy2)   

        if enemy2_once_flag == 1:
            if pygame.sprite.spritecollideany(player, enemy2.enemy_bullets) :
                enemy2.enemy_bullets.remove(enemy_bullet)
                player.is_hit = True
                game_over_sound.play()
            enemy2.enemy_bullets.draw(screen)             
            
    # 绘制敌机和boss击毁动画
        for enemy1_down in enemies1_down:
            if enemy1_down.down_index == 0:
                enemy_down_sound.play()
            if enemy1_down.down_index > 7:
                enemies1_down.remove(enemy1_down)
                player.score += 10
                continue
            screen.blit(enemy1_down.down_imgs[enemy1_down.down_index // 2], enemy1_down.rect)
            enemy1_down.down_index += 1     
 
        for enemy2_down in enemies2_down:
            if enemy2_down.down_index == 0:
                enemy_down_sound.play()
            if enemy2_down.down_index > 7:
                enemies2_down.remove(enemy2_down)
                player.score += 20
                continue
            screen.blit(enemy2_down.down_imgs[enemy2_down.down_index // 2], enemy2_down.rect)
            enemy2_down.down_index += 1    
            
        if boss_down_flag == 1:
            img_index = boss.down_index // 10
            screen.blit(boss_down_img[img_index], boss.rect)
            boss.down_index += 1
            if boss.down_index == 59:
                boss_down_flag = 0
                running = 0
                myGame = 1
                myScore = player.score

        # 生成奖励
        if award_frequency == award_time:
            type = random.randint(0, 20)
            if type < 15:
                position = [random.randint(0, SCREEN_WIDTH - double_bullet_rect.width), 0]
                award = Award(double_bullet_img, double_bullet_effect, position)
                award.kind = 1
            else:
                position = [random.randint(0, SCREEN_WIDTH - bomb_rect.width), 0]
                award = Award(bomb_img, bomb_effect, position)
                award.kind = 2
                
            awards.add(award)
            award_frequency = 1
            award_time = random.randint(300,600)
        else:
            award_frequency += 1
            
        for award in awards:
            award.move()
                #是否获得奖励
            if pygame.sprite.collide_rect(player, award):
                if award.kind == 1:
                    player.NL_bullet_time = 400
                    get_double_bullet_sound.play()
                else:
                    if player.bomb < player.bomb_max:
                        player.bomb += 1
                        get_bomb_sound.play()
                awards.remove(award)
            
            if award.rect.bottom > 700:
                awards.remove(award)
                
# 绘制玩家飞机
        if not player.is_hit:
            screen.blit(player.image[player.index], player.rect)
            # 更换图片索引使飞机有动画效果
            player.index = player.shoot_frequency // 8  # 注意这里有一个射子弹喷火的小动画，所以子弹频率设成了15
        else:  
            player.index = player.down_index // 8 #用这种准循环来实现玩家飞机爆炸的效果
            screen.blit(player.down_imgs[player.index], player.rect)
            player.down_index += 1
            if player.down_index > 31:
                running = 0  # 效果结束后这个循环就结束了
                myGame = 0
                myScore = player.score
                
 # 绘制子弹和和奖励和敌机
        player.bullets.draw(screen)
        awards.draw(screen)
        enemies1.draw(screen)
            
        # 绘制得分
        score_font = pygame.font.Font('freesansbold.ttf', 32)  # 字体大小的
        score_text = score_font.render(str(player.score), True, (128, 128, 128))   # RGB三个通道，表示颜色是灰色
        text_rect = score_text.get_rect()
        text_rect.topleft = [10, 5]
        screen.blit(score_text, text_rect)
        # 绘制boss血量
        if boss_flag == 1 and boss_down_flag == 0:
            boss_life_font = pygame.font.Font('freesansbold.ttf', 22)
            strbosslife = ''
            for i in range(0, boss.life):
                strbosslife += '[]'
            boss_life_text = boss_life_font.render('Boss level3: ' + strbosslife, True, (128, 128, 128))
            boss_life_rect = boss_life_text.get_rect()
            boss_life_rect.topleft = [30, SCREEN_HEIGHT - 40]
            screen.blit(boss_life_text, boss_life_rect)
                
        # 绘制子弹数目和bomb数目
        bullet_font = pygame.font.Font('freesansbold.ttf', 20)
        if player.NL_bullet_time > 0:
            bullet_text = bullet_font.render('Bullet: (^_^)', True, (128, 128, 128))
        else:
            if player.bullet > 0:
                bullet_text = bullet_font.render('Bullet: ' , True, (128, 128, 128))
                position = SCREEN_WIDTH - 65
                for i in range(0, player.bullet):
                    screen.blit(bullet_img, ((position + i * 12), 10))
            else:
                bullet_text = bullet_font.render('Recharging...' , True, (128, 128, 128))
        bulletText_rect = bullet_text.get_rect()
        bulletText_rect.topleft = [SCREEN_WIDTH - 130, 10] # 确定bullet的位置
        screen.blit(bullet_text, bulletText_rect)
        bomb_font = pygame.font.Font('freesansbold.ttf', 20)
        bomb_text = bomb_font.render('Bomb x ' + str(player.bomb), True, (128, 128, 128))
        bombText_rect = bomb_text.get_rect()
        bombText_rect.topleft = [SCREEN_WIDTH - 130, 35]
        screen.blit(bomb_text, bombText_rect)
        
        # 监听键盘事件
        key_pressed = pygame.key.get_pressed()
        # 若玩家被击中，则无效
        if not player.is_hit:
            if key_pressed[K_SPACE]:
                if player.shoot_frequency % 15 == 0 and (player.bullet > 0 or player.NL_bullet_time > 0):
                    bullet_sound.play()
                    player.shoot(bullet_img)
                    player.shoot_frequency = 0
                    player.bullet -= 1
                    #使用炸弹
            if key_pressed[K_b]:
                if player.bomb_frequency % 15 == 0 and player.bomb > 0:
                    bomb_sound.play()
                    player.bomb -= 1
                    player.bomb_frequency = 0
                    if boss_flag == 1:
                        boss.life -= boss.bomb_damage
                        for enemy_bullet in boss.enemy_bullets:
                            boss.enemy_bullets.remove(enemy_bullet)                       
                    for enemy1 in enemies1:
                        enemies1_down.add(enemy1)
                        enemies1.remove(enemy1)
                    if enemy2_once_flag == 1:          
                        for enemy_bullet in enemy2.enemy_bullets:
                            enemy2.enemy_bullets.remove(enemy_bullet)    
                        for enemy2 in enemies2:
                            enemies2_down.add(enemy2)
                            enemies2.remove(enemy2)     
                            
            if key_pressed[K_w] or key_pressed[K_UP]:
                player.moveUp()
            if key_pressed[K_s] or key_pressed[K_DOWN]:
                player.moveDown()
            if key_pressed[K_a] or key_pressed[K_LEFT]:
                player.moveLeft()
            if key_pressed[K_d] or key_pressed[K_RIGHT]:
                player.moveRight()
            
        if player.shoot_frequency < 15:  # 现在飞机射子弹的频率下来了
            player.shoot_frequency += 1
        if player.bomb_frequency < 15:
            player.bomb_frequency += 1
            #recharge the bullets
        if player.recharging < player.recharge_time and player.bullet < player.bullet_max:
            player.recharging += 1
            if player.recharging == player.recharge_time:
                player.bullet += 1
                player.recharging = 0
        player.NL_bullet_time -= 1
        if player.NL_bullet_time == 0:
            player.bullet = player.bullet_max
                
        # 更新屏幕
        pygame.display.update()
        myTime += 1
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()    
                
def over():
    clock = pygame.time.Clock()
    myX = [-3, 3, -3, 3]
    myY = [3, 3, -3, -3]
    myIndex1 = myIndex2 = 0
    flag1 = flag2 = 0
    running = 1
    myYesCenterx = screen.get_rect().centerx 
    myYesCentery = screen.get_rect().centery + 170
    myNoCenterx = screen.get_rect().centerx
    myNoCentery = screen.get_rect().centery + 220
    
    while running:
        clock.tick(60)
                
        screen.fill(0)
        screen.blit(gameover, (0, 0))
        
        font = pygame.font.Font('freesansbold.ttf', 48)
        scoreText = font.render('Score: '+ str(myScore), True, (100, 0, 0))
        scoreText_rect = scoreText.get_rect()
        scoreText_rect.centerx = screen.get_rect().centerx
        scoreText_rect.centery = screen.get_rect().centery + 24  # 这两句是用来调整player.score的位置的，现在是x轴上在
        #中间，y轴上往下来一点
        newgameText = font.render('Play again ?', True, (100, 0, 0))
        newgameText_rect = newgameText.get_rect()
        newgameText_rect.centerx = screen.get_rect().centerx
        newgameText_rect.centery = screen.get_rect().centery + 100 
        screen.blit(newgameText, newgameText_rect)
        choicefont = pygame.font.Font('freesansbold.ttf', 28)
        YesText = choicefont.render('Yes, I am brave and I like challenging', True, (100, 0, 0))
        NoText = choicefont.render('No, this game sucks and I am gonna watch some porns', True, (100, 0, 0))
        YesText_rect = YesText.get_rect()
        NoText_rect = NoText.get_rect()
        YesText_rect.centerx = screen.get_rect().centerx 
        YesText_rect.centery = screen.get_rect().centery + 170
        NoText_rect.centerx = screen.get_rect().centerx
        NoText_rect.centery = screen.get_rect().centery + 220
        screen.blit(scoreText, scoreText_rect)
        if flag1 == 0:
            screen.blit(YesText, YesText_rect)
        if flag2 == 0:
            screen.blit(NoText, NoText_rect)
        
        showlist = list(pygame.mouse.get_pos())
        #对于yes的回答
        if  showlist[0] > 155 and showlist[0] < 640 and showlist[1] > 500 and showlist[1] < 540:
            myIndex1 += 1
            flag1 = 1
            if myIndex1 // 4 >= 1 and myIndex1 % 4 == 0:
                YesText_rect.centerx = myYesCenterx + myX[myIndex1 // 4 - 1]
                YesText_rect.centery = myYesCentery + myY[myIndex1 // 4 - 1]
            if myIndex1 > 14:
                myIndex1 = 0
            screen.blit(YesText, YesText_rect)    
        else:
            myIndex1 = 0
            flag1 = 0
            #对于no的回答
        if  showlist[0] > 80 and showlist[0] < 730 and showlist[1] > 550 and showlist[1] < 590:
            myIndex2 += 1
            flag2 = 1
            if myIndex2 // 5 >= 1 and myIndex2 % 5 == 0:
                NoText_rect.centerx = myNoCenterx + myX[myIndex2 // 5 - 1]
                NoText_rect.centery = myNoCentery + myY[myIndex2 // 5 - 1]
            if myIndex2 > 23:
                myIndex2 = 0
            screen.blit(NoText, NoText_rect)    
        else:
            myIndex2 = 0
            flag2 = 0
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                poslist = list(pygame.mouse.get_pos())
                #print pygame.mouse.get_pos()  # 用于测试选择项的两个端点的坐标的
                if poslist[0] > 155 and poslist[0] < 640 and poslist[1] > 500 and poslist[1] < 540:
                    running = 0
                if poslist[0] > 80 and poslist[0] < 730 and poslist[1] > 550 and poslist[1] < 590:
                    pygame.quit()
                    exit()
        pygame.display.update()
    
def opening():   
    running = 1
    clock = pygame.time.Clock()
    error = 4
    myX = [-error, error, -error, error]
    myY = [error, error, -error, -error]
    myIndex = 0
    myCenterx = screen.get_rect().centerx
    myCentery = screen.get_rect().centery
    flag = 0
    
    while running:
        clock.tick(60)
    
        screen.fill(0)
        screen.blit(background, (0, 0))
        openingFont = pygame.font.Font('freesansbold.ttf', 50)
        introFont = pygame.font.Font('freesansbold.ttf', 12)
        welcomeText = openingFont.render("Welcome to this game!", True, (0, 0, 0))
        beginText = openingFont.render('New game', True, (0, 0, 0))
        introText1 = introFont.render('You can use direction keys to move your plane, tap space to shoot. Remember there is a recharging time after 5 bullets', True, (0, 0, 0))
        introText2 = introFont.render('There are two kinds of award, if you get the bullet award, you can have unlimited bullets for a while. ', True, (0, 0, 0))
        introText3 = introFont.render('If you get the bomb award you can tap b to use it and a bomb can take out all the enemies1 on the screen and enemy2\'s bullets. ', True, (0, 0, 0))
        introText4 = introFont.render('Nothing else to say, hope you have fun ! ', True, (0, 0, 0))
        introText5 = introFont.render('Please check  https://github.com/type-coder-engineer  to find more interesting projects by me ^_^', True, (0, 50, 200))
        introText1_rect = introText1.get_rect()
        introText2_rect = introText2.get_rect()
        introText3_rect = introText3.get_rect()
        introText4_rect = introText4.get_rect()
        introText5_rect = introText5.get_rect()
        welcomeText_rect = welcomeText.get_rect()
        beginText_rect = beginText.get_rect()
        
        welcomeText_rect.centerx =  screen.get_rect().centerx
        welcomeText_rect.centery = screen.get_rect().centery - 250
        introText1_rect.centerx = screen.get_rect().centerx
        introText1_rect.centery = screen.get_rect().centery - 200
        introText2_rect.centerx = screen.get_rect().centerx
        introText2_rect.centery = screen.get_rect().centery - 170
        introText3_rect.centerx = screen.get_rect().centerx
        introText3_rect.centery = screen.get_rect().centery - 140
        introText4_rect.centerx = screen.get_rect().centerx
        introText4_rect.centery = screen.get_rect().centery - 100
        beginText_rect.centerx =  screen.get_rect().centerx
        beginText_rect.centery = screen.get_rect().centery
        introText5_rect.centerx = screen.get_rect().centerx
        introText5_rect.centery = screen.get_rect().centery + 300
        screen.blit(welcomeText, welcomeText_rect)
        screen.blit(introText1, introText1_rect)
        screen.blit(introText2, introText2_rect)
        screen.blit(introText3, introText3_rect)
        screen.blit(introText4, introText4_rect)
        screen.blit(introText5, introText5_rect)
        if flag == 0:
            screen.blit(beginText, beginText_rect)
        
        showlist = list(pygame.mouse.get_pos())
        if showlist[0] > 280 and showlist[0] < 520 and showlist[1] > 330 and showlist[1] < 370:
            myIndex += 1
            flag = 1
            if myIndex // 5 >= 1 and myIndex % 5 == 0:
                beginText_rect.centerx = myCenterx + myX[myIndex // 5 - 1]
                beginText_rect.centery = myCentery + myY[myIndex // 5 - 1]
                # print myIndex
                # print beginText_rect.centerx
                # print beginText_rect.centery
            if myIndex > 23:
                myIndex = 0
            screen.blit(beginText, beginText_rect)
            # pygame.display.update()    
        else:
            myIndex = 0
            flag = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                poslist = list(pygame.mouse.get_pos())
                # print pygame.mouse.get_pos()  # 用于测试选择项的两个端点的坐标的
                if poslist[0] > 280 and poslist[0] < 520 and poslist[1] > 330 and poslist[1] < 370:
                    running = 0
        pygame.display.update()

def main(): 
    player = Player(player_img, player_down_img, player_pos)
    clock = pygame.time.Clock()
    
    # level1(clock, player)
    # if myGame == 1:
        # level2(clock, player)
        # if myGame == 1:
            # level3(clock, player)
    level3(clock, player)
    
if __name__ == '__main__': 
    opening()
    while 1:    
        main()
        over()
        
        