# -*- coding: utf-8 -*-
"""
My first game, wrote by pygame 
@author: ZHANG Chenyu
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
if os.name == 'posix':   # mac环境中运行必须要这么设置，不然刷新频率太低
    flags = FULLSCREEN | DOUBLEBUF
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags)
    screen.set_alpha(None)
else:
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.set_alpha(None)
pygame.display.set_caption('shootPlanes')

# load the music
pygame.mixer.init()
bullet_sound     = pygame.mixer.Sound('resources/sound/bullet.wav')
enemy_down_sound = pygame.mixer.Sound('resources/sound/enemy1_down.wav')
boss_down_sound  = pygame.mixer.Sound('resources/sound/enemy2_down.wav')
boss_show_sound  = pygame.mixer.Sound('resources/sound/boss_show.wav')
get_bullet_sound = pygame.mixer.Sound('resources/sound/get_bullet.wav')
get_bomb_sound   = pygame.mixer.Sound('resources/sound/get_bomb.wav')
bomb_sound       = pygame.mixer.Sound('resources/sound/use_bomb.wav')
game_over_sound  = pygame.mixer.Sound('resources/sound/game_over.wav')
beat_boss_sound  = pygame.mixer.Sound('resources/sound/vectory.wav')

#设置音量
bullet_sound.set_volume(0.3)
enemy_down_sound.set_volume(0.3)
game_over_sound.set_volume(0.3)
boss_show_sound.set_volume(0.3)
get_bullet_sound.set_volume(0.4)
get_bomb_sound.set_volume(0.4)
bomb_sound.set_volume(0.3)
beat_boss_sound.set_volume(0.3)
bgm = pygame.mixer.Sound('resources/sound/game_music.wav')
bgm.play(-1, 0)
bgm.set_volume(0.1)

#设置游戏资源
background = pygame.image.load('resources/image/back_ground.png').convert()
gameover = pygame.image.load('resources/image/game_over.png')
gameicon = pygame.image.load('resources/image/myPlane32.png')
resources = pygame.image.load('resources/image/shoot.png')
# timeout_icon = pygame.image.load('resources/image/timeout.png')

pygame.display.set_icon(gameicon) #可以在标题栏上出现一个小飞机，注意icon最好是32x32 的png

# 暂停按钮
# timeout_rect = pygame.Rect(1, 1, 58, 58)
# timeout_img = timeout_icon.subsurface(timeout_rect)
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

# 玩家飞机素材
player_rect = []   # 注意这个rect取的方法，第一二个点是图片的左上角坐标，然后两个数值是宽和高
player_rect.append(pygame.Rect(0, 99, 102, 126))       
player_rect.append(pygame.Rect(165, 360, 102, 126))
player_rect.append(pygame.Rect(165, 234, 102, 126))     
player_rect.append(pygame.Rect(330, 624, 102, 126))
player_rect.append(pygame.Rect(330, 498, 102, 126))
player_rect.append(pygame.Rect(432, 624, 102, 126))
# 玩家精灵图片区域
player_img = []
player_img.append(resources.subsurface(player_rect[0]))
player_img.append(resources.subsurface(player_rect[1]))
# 玩家爆炸精灵图片区域
player_down_img = []
player_down_img.append(resources.subsurface(player_rect[2]))
player_down_img.append(resources.subsurface(player_rect[3]))
player_down_img.append(resources.subsurface(player_rect[4]))
player_down_img.append(resources.subsurface(player_rect[5]))
player_pos = [360, 580]

# 每关boss相关素材
boss_rect = []
boss_rect.append(pygame.Rect(165, 750, 170, 245))
boss_rect.append(pygame.Rect(505, 750, 170, 250))
boss_rect.append(pygame.Rect(335, 750, 170, 250))
boss_rect.append(pygame.Rect(  5, 485, 160, 245))
boss_rect.append(pygame.Rect(  5, 225, 160, 245))
boss_rect.append(pygame.Rect(842, 750, 160, 245))
boss_rect.append(pygame.Rect(168, 485, 160, 250))
boss_rect.append(pygame.Rect(675, 750, 165, 250))
boss_rect.append(pygame.Rect(  0, 750, 160, 220))
# boss正常和设计图片
boss_img = []
boss_img.append(resources.subsurface(boss_rect[0])) # 如果在这里定义boss_image 那下面就没有问题。。。
boss_img.append(resources.subsurface(boss_rect[1]))
boss_img.append(resources.subsurface(boss_rect[2]))
# boss爆炸图片
boss_down_img = []
boss_down_img.append(resources.subsurface(boss_rect[3]))
boss_down_img.append(resources.subsurface(boss_rect[4]))
boss_down_img.append(resources.subsurface(boss_rect[5]))
boss_down_img.append(resources.subsurface(boss_rect[6]))
boss_down_img.append(resources.subsurface(boss_rect[7]))
boss_down_img.append(resources.subsurface(boss_rect[8]))

boss_pos = [screen.get_rect().centerx - 85, 0]
boss_pos_left = [screen.get_rect().centerx - 285, 0]
boss_pos_right = [screen.get_rect().centerx + 115, 0]
boss_level5_pos = [screen.get_rect().centerx - 15, 0]

# 定义敌机对象使用的surface相关参数, enemy1 不会发射子弹
enemy1_rect = []
enemy1_rect.append(pygame.Rect(538, 612, 50, 40))
enemy1_rect.append(pygame.Rect(267, 347, 57, 43))
enemy1_rect.append(pygame.Rect(873, 697, 57, 43))
enemy1_rect.append(pygame.Rect(267, 296, 57, 43))
enemy1_rect.append(pygame.Rect(930, 697, 57, 43))
# 正常图片
enemy1_img = resources.subsurface(enemy1_rect[0])
# 爆炸图片
enemy1_down_img = []
enemy1_down_img.append(resources.subsurface(enemy1_rect[1]))
enemy1_down_img.append(resources.subsurface(enemy1_rect[2]))
enemy1_down_img.append(resources.subsurface(enemy1_rect[3]))
enemy1_down_img.append(resources.subsurface(enemy1_rect[4]))

# 第二种敌机，可以发射子弹
enemy2_rect = []
enemy2_rect.append(pygame.Rect(  0,   2, 69, 90))
enemy2_rect.append(pygame.Rect(432, 528, 69, 92))
enemy2_rect.append(pygame.Rect(534, 654, 69, 92))
enemy2_rect.append(pygame.Rect(603, 654, 69, 92))
enemy2_rect.append(pygame.Rect(672, 653, 69, 92))
enemy2_rect.append(pygame.Rect(741, 660, 69, 85))
# 敌机正常的图片
enemy2_img = []
enemy2_img.append(resources.subsurface(enemy2_rect[0]))
enemy2_img.append(resources.subsurface(enemy2_rect[1]))
# 爆炸图片
enemy2_down_img = []
enemy2_down_img.append(resources.subsurface(enemy2_rect[2]))
enemy2_down_img.append(resources.subsurface(enemy2_rect[3]))
enemy2_down_img.append(resources.subsurface(enemy2_rect[4]))
enemy2_down_img.append(resources.subsurface(enemy2_rect[5]))

def classicMode():
    enemies1 = pygame.sprite.Group()  # enemy1的group
    awards = pygame.sprite.Group()  # 奖励的group
    enemies1_down = pygame.sprite.Group()  # 被击毁的就放入这个group中一起处理
    enemy1_frequency = 0
    interval = 0
    award_frequency = 1
    award_time = 100  # 第一个award出现
    myTime = 0
    running = 1
    flag_betweenLevel = 0
    index_betweenLevel = 0
    timeout_frequency = 20
    flag_timeout = False
    
    player = Player(player_img, player_down_img, player_pos)
    clock = pygame.time.Clock()
    global myScore #注意global变量的声明一定要放在定义这个变量的block中，我是在level1中第一次定义myScore = player.score的，所以要在level1中声明myScore
    score_font = pygame.font.Font('freesansbold.ttf', 32)  # 字体大小的
    bullet_font = pygame.font.Font('freesansbold.ttf', 20)
    bomb_font = pygame.font.Font('freesansbold.ttf', 20)
    timeout_font = pygame.font.Font('freesansbold.ttf', 50)
    timeout_text = timeout_font.render('Time Out...', True, (0, 100, 200))
    
    while running:
        # 控制游戏最大帧率为60
        clock.tick(60)
        # 绘制背景
        screen.fill(0)
        screen.blit(background, (0, 0))
        
        if enemy1_frequency == interval:  # 通过这个数字来确定出现的频率
            enemy1_pos = [random.randint(0, SCREEN_WIDTH - enemy1_rect[0].width), 0]
            enemy1 = Enemy1(enemy1_img, enemy1_down_img, enemy1_pos)
            enemies1.add(enemy1)    
            enemy1_frequency = 0
            interval = 100 - int(myTime / 50)   
            if interval < 10:
                interval = 10
        else:
            enemy1_frequency += 1
            
        enemies1_shot = pygame.sprite.groupcollide(enemies1, player.bullets, 1, 1)
        for enemy1_down in enemies1_shot:
            enemies1_down.add(enemy1_down) 
            
        # 移动子弹，若超出窗口范围则删除
        for bullet in player.bullets:
            bullet.move()
            if bullet.rect.bottom < 0:
                player.bullets.remove(bullet)
                    
        # 移动敌机，若超出窗口范围则删除
        for enemy1 in enemies1:
            enemy1.move()
            # 判断玩家是否被击中
            if pygame.sprite.collide_rect(enemy1, player):
                if (enemy1.rect.centery - player.rect.centery) < -35:
                    if abs(enemy1.rect.centerx - player.rect.centerx) < 30:
                        enemies1_down.add(enemy1)
                        enemies1.remove(enemy1)
                        player.is_hit = True
                        game_over_sound.play() 
                        break
                    else:
                        pass
                        
                elif (enemy1.rect.centery - player.rect.centery) > 50:                    
                    pass
                else:
                    enemies1_down.add(enemy1)
                    enemies1.remove(enemy1)
                    player.is_hit = True
                    game_over_sound.play() 
                    break
                    
            if enemy1.rect.top > SCREEN_HEIGHT:
                enemies1.remove(enemy1)   
            
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

        # 生成奖励
        if award_frequency == award_time and flag_betweenLevel == 0:
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
            min_time = 600 - int(player.score / 8)
            if min_time < 280:
                min_time = 280
            max_time = 1000 - int(player.score / 6)
            if max_time < 600:
                max_time = 600
            award_time = random.randint(min_time, max_time)
        else:
            award_frequency += 1
            
        for award in awards:
            award.move()
                #是否获得奖励
            if pygame.sprite.collide_rect(player, award):
                if award.kind == 1:
                    player.NL_bullet_time = 400
                    get_bullet_sound.play()
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
        # score_font = pygame.font.Font('freesansbold.ttf', 32)  # 字体大小的
        score_text = score_font.render(str(player.score), True, (128, 128, 128))   # RGB三个通道，表示颜色是灰色
        text_rect = score_text.get_rect()
        text_rect.topleft = [10, 5]
        screen.blit(score_text, text_rect)
                
        # 绘制子弹数目和bomb数目
        # 绘制timeout按钮
        # bullet_font = pygame.font.Font('freesansbold.ttf', 20)
        if player.NL_bullet_time > 0:
            bullet_text = bullet_font.render('Bullet: ', True, (128, 128, 128))
            position = SCREEN_WIDTH - 65
            for i in range(0, 5):
                screen.blit(bullet_img, ((position + i * 12), 10))
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
        # bomb_font = pygame.font.Font('freesansbold.ttf', 20)
        bomb_text = bomb_font.render('Bomb x ' + str(player.bomb), True, (128, 128, 128))
        bombText_rect = bomb_text.get_rect()
        bombText_rect.topleft = [SCREEN_WIDTH - 130, 35]
        screen.blit(bomb_text, bombText_rect)
        # screen.blit(timeout_img, (SCREEN_WIDTH - 100, 60))
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
                
            if timeout_frequency < 20:
                timeout_frequency += 1
            if key_pressed[K_t] and timeout_frequency == 20:
                flag_timeout = True
                timeout_frequency = 0
                while(1): 
                    clock.tick(60)
                    timeout_rect = timeout_text.get_rect()
                    timeout_rect.centerx = screen.get_rect().centerx
                    timeout_rect.centery = screen.get_rect().centery
                    screen.blit(timeout_text, timeout_rect)
                    pygame.display.update()
                    if timeout_frequency < 20:
                        timeout_frequency += 1
                    if not flag_timeout:
                        timeout_frequency = 0
                        break
                    key_pressed = pygame.key.get_pressed()
                    if key_pressed[K_t] and timeout_frequency == 20:
                        flag_timeout = False
                        timeout_frequency = 0
                    for timeout_event in pygame.event.get():
                        if timeout_event.type == pygame.QUIT:
                            pygame.quit()
                            exit()   
        
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
            get_bullet_sound.play()  # 效果失效时提醒一下
                
        # 更新屏幕
        pygame.display.update()
        myTime += 1
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()   

def level1(clock, player, flag_saw_boss, again):
    if again == 1:
        player.bullet = 5
        player.bomb = 1
        player.index = 0
        player.down_index = 0
        player.rect.topleft = player_pos
        player.is_hit = False
        player.score = 0
        player.NL_bullet_time = 0
        
    enemies1 = pygame.sprite.Group()  # enemy1的group
    awards = pygame.sprite.Group()  # 奖励的group
    enemies1_down = pygame.sprite.Group()  # 被击毁的就放入这个group中一起处理

    award_frequency = 1
    award_time = 100  # 第一个award出现
    boss_flag = flag_saw_boss
    if boss_flag == 1:
        myTime = 3300
    else:
        myTime = 0
    boss_down_flag = 0
    boss_once_flag = 0
    running = 1
    flag_betweenLevel = 0
    index_betweenLevel = 0
    global myScore #注意global变量的声明一定要放在定义这个变量的block中，我是在level1中第一次定义myScore = player.score的，所以要在level1中声明myScore
    global myGame
    global pass_level
    openingFont = pygame.font.Font('freesansbold.ttf', 50)
    level1Text = openingFont.render("--LEVEL1--", True, (0, 0, 0))
    level2Text = openingFont.render("--LEVEL2--", True, (0, 0, 0))
    level1Text_rect = level1Text.get_rect()
    level2Text_rect = level2Text.get_rect()
    myCenterx = screen.get_rect().centerx - 830
    myCentery = screen.get_rect().centery
    speed_rect_slow = 0.5
    speed_rect_fast = 80
    score_font = pygame.font.Font('freesansbold.ttf', 32)  # 字体大小的
    boss_life_font = pygame.font.Font('freesansbold.ttf', 22)
    bullet_font = pygame.font.Font('freesansbold.ttf', 20)
    bomb_font = pygame.font.Font('freesansbold.ttf', 20)
    timeout_frequency = 20
    flag_timeout = False
    timeout_font = pygame.font.Font('freesansbold.ttf', 50)
    timeout_text = timeout_font.render('Time Out...', True, (0, 100, 200))
    
    while boss_flag == 0:
        clock.tick(60)
        screen.fill(0)
        level1Text_rect.centerx = myCenterx
        level1Text_rect.centery = myCentery
        screen.blit(background, (0, 0))
        
        screen.blit(level1Text, level1Text_rect)       
        if myCenterx < screen.get_rect().centerx - 30 or myCenterx > screen.get_rect().centerx + 30:
            myCenterx += speed_rect_fast
        else:
            myCenterx += speed_rect_slow
        if myCenterx > screen.get_rect().centerx + 800:
            myCenterx = screen.get_rect().centerx - 830
            break
            
        screen.blit(player.image[player.index], player.rect)
        pygame.display.update()
        
    while running:
        # 控制游戏最大帧率为60
        clock.tick(60)
        # print clock.get_fps()
        # 绘制背景
        screen.fill(0)
        screen.blit(background, (0, 0))
        
        if flag_betweenLevel == 1:
            if index_betweenLevel == 0:
                beat_boss_sound.play()
            index_betweenLevel += 1
            
            if index_betweenLevel >= 200 and index_betweenLevel <= 350:
                level2Text_rect.centerx = myCenterx
                level2Text_rect.centery = myCentery
                
                screen.blit(level2Text, level2Text_rect)       
                if myCenterx < screen.get_rect().centerx - 30 or myCenterx > screen.get_rect().centerx + 30:
                    myCenterx += speed_rect_fast
                else:
                    myCenterx += speed_rect_slow
            
            if index_betweenLevel == 400:
                if pass_level < 2:
                    pass_level = 2
                    save_game()
                return 1
            
        if boss_flag == 0 and boss_down_flag == 0 and flag_betweenLevel == 0:
            if myTime % (100 - int(myTime / 80)) == 0 and myTime <= 3000:  # 通过这个数字来确定出现的频率
                enemy1_pos = [random.randint(0, SCREEN_WIDTH - enemy1_rect[0].width), 0]
                enemy1 = Enemy1(enemy1_img, enemy1_down_img, enemy1_pos)
                enemies1.add(enemy1)    
                
         #生成boss
        if myTime == 3300:
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
                if player.is_hit is not True:
                    player.is_hit = True
                    game_over_sound.play()
                    boss.life -= boss.bomb_damage
                else:
                    pass
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
                if (enemy1.rect.centery - player.rect.centery) < -35:
                    if abs(enemy1.rect.centerx - player.rect.centerx) < 30:
                        enemies1_down.add(enemy1)
                        enemies1.remove(enemy1)
                        player.is_hit = True
                        game_over_sound.play() 
                        break
                    else:
                        pass
                        
                elif (enemy1.rect.centery - player.rect.centery) > 50:                    
                    pass
                else:
                    enemies1_down.add(enemy1)
                    enemies1.remove(enemy1)
                    player.is_hit = True
                    game_over_sound.play() 
                    break
                    
            if enemy1.rect.top > SCREEN_HEIGHT:
                enemies1.remove(enemy1)   

        if boss_once_flag == 1:
            if pygame.sprite.spritecollideany(player, boss.enemy_bullets) :
                if (enemy_bullet.rect.centery - player.rect.centery) < -35:
                    if abs(enemy_bullet.rect.centerx - player.rect.centerx) < 20:
                        boss.enemy_bullets.remove(enemy_bullet)
                        player.is_hit = True
                        game_over_sound.play() 
                    else:
                        pass
                        
                elif (enemy_bullet.rect.centery - player.rect.centery)  > 40:                    
                    pass
                else:
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
                flag_betweenLevel = 1
                myGame = 1
                myScore = player.score

        # 生成奖励
        if award_frequency == award_time and flag_betweenLevel == 0:
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
            min_time = 1000 - int(player.score / 12)
            if min_time < 800:
                min_time = 800
            max_time = 1300 - int(player.score / 10)
            if max_time < 1000:
                max_time = 1000
            award_time = random.randint(min_time, max_time)
        else:
            award_frequency += 1
            
        for award in awards:
            award.move()
                #是否获得奖励
            if pygame.sprite.collide_rect(player, award):
                if award.kind == 1:
                    player.NL_bullet_time = 400
                    get_bullet_sound.play()
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
                return boss_flag
                
 # 绘制子弹和和奖励和敌机
        player.bullets.draw(screen)
        awards.draw(screen)
        enemies1.draw(screen)
            
        # 绘制得分
        # score_font = pygame.font.Font('freesansbold.ttf', 32)  # 字体大小的
        score_text = score_font.render(str(player.score), True, (128, 128, 128))   # RGB三个通道，表示颜色是灰色
        text_rect = score_text.get_rect()
        text_rect.topleft = [10, 5]
        screen.blit(score_text, text_rect)
        # 绘制boss血量
        if boss_flag == 1 and boss_down_flag == 0:
            # boss_life_font = pygame.font.Font('freesansbold.ttf', 22)
            strbosslife = ''
            for i in range(0, boss.life):
                strbosslife += '[]'
            boss_life_text = boss_life_font.render('Boss level1: ' + strbosslife, True, (128, 128, 128))
            boss_life_rect = boss_life_text.get_rect()
            boss_life_rect.topleft = [30, SCREEN_HEIGHT - 40]
            screen.blit(boss_life_text, boss_life_rect)
                
        # 绘制子弹数目和bomb数目
        # bullet_font = pygame.font.Font('freesansbold.ttf', 20)
        if player.NL_bullet_time > 0:
            bullet_text = bullet_font.render('Bullet: ', True, (128, 128, 128))
            position = SCREEN_WIDTH - 65
            for i in range(0, 5):
                screen.blit(bullet_img, ((position + i * 12), 10))
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
        # bomb_font = pygame.font.Font('freesansbold.ttf', 20)
        bomb_text = bomb_font.render('Bomb x ' + str(player.bomb), True, (128, 128, 128))
        bombText_rect = bomb_text.get_rect()
        bombText_rect.topleft = [SCREEN_WIDTH - 130, 35]
        screen.blit(bomb_text, bombText_rect)
        # screen.blit(timeout_img, (SCREEN_WIDTH - 100, 60))
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
                    if boss_flag == 1 and boss.flag_showup == 1:
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
                
         # 按t来暂停
            if timeout_frequency < 20:
                timeout_frequency += 1
            if key_pressed[K_t] and timeout_frequency == 20:
                flag_timeout = True
                timeout_frequency = 0
                while(1): 
                    clock.tick(60)
                    timeout_rect = timeout_text.get_rect()
                    timeout_rect.centerx = screen.get_rect().centerx
                    timeout_rect.centery = screen.get_rect().centery
                    screen.blit(timeout_text, timeout_rect)
                    pygame.display.update()
                    if timeout_frequency < 20:
                        timeout_frequency += 1
                    if not flag_timeout:
                        timeout_frequency = 0
                        break
                    key_pressed = pygame.key.get_pressed()
                    if key_pressed[K_t] and timeout_frequency == 20:
                        flag_timeout = False
                        timeout_frequency = 0
                    for timeout_event in pygame.event.get():
                        if timeout_event.type == pygame.QUIT:
                            pygame.quit()
                            exit()   
                            
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
            get_bullet_sound.play()  # 效果失效时提醒一下
            
        # 更新屏幕
        pygame.display.update()
        myTime += 1
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()   

def level2(clock, player, flag_saw_boss, again):  
    if again == 1:
        player.bullet = 5
        player.bomb = 1
        player.index = 0
        player.down_index = 0
        player.rect.topleft = player_pos
        player.is_hit = False
        player.score = 0
        player.NL_bullet_time = 0
        
    enemies1 = pygame.sprite.Group()  # enemy1的group
    awards = pygame.sprite.Group()  # 奖励的group
    enemies1_down = pygame.sprite.Group()  # 被击毁的就放入这个group中一起处理

    award_frequency = 1
    award_time = 100  # 第一个award出现
    boss_flag = flag_saw_boss
    if boss_flag == 1:
        myTime = 3300
    else:
        myTime = 0
    boss1_down_flag = 0
    boss2_down_flag = 0
    boss_once_flag = 0
    running = 1
    flag_betweenLevel = 0
    index_betweenLevel = 0
    global myScore
    global myGame
    global pass_level
    openingFont = pygame.font.Font('freesansbold.ttf', 50)
    level3Text = openingFont.render("--LEVEL3--", True, (0, 0, 0))
    level3Text_rect = level3Text.get_rect()
    myCenterx = screen.get_rect().centerx - 830
    myCentery = screen.get_rect().centery
    speed_rect_slow = 0.5
    speed_rect_fast = 80
    score_font = pygame.font.Font('freesansbold.ttf', 32)  # 字体大小的
    boss_life_font = pygame.font.Font('freesansbold.ttf', 22)
    bullet_font = pygame.font.Font('freesansbold.ttf', 20)
    bomb_font = pygame.font.Font('freesansbold.ttf', 20)
    timeout_frequency = 20
    flag_timeout = False
    timeout_font = pygame.font.Font('freesansbold.ttf', 50)
    timeout_text = timeout_font.render('Time Out...', True, (0, 100, 200))
    
    while running:
        # 控制游戏最大帧率为60
        clock.tick(60)
        # 绘制背景
        screen.fill(0)
        screen.blit(background, (0, 0))

        if flag_betweenLevel == 1:
            if index_betweenLevel == 0:
                beat_boss_sound.play()
            index_betweenLevel += 1
            
            if index_betweenLevel >= 200 and index_betweenLevel <= 350:
                level3Text_rect.centerx = myCenterx
                level3Text_rect.centery = myCentery
                
                screen.blit(level3Text, level3Text_rect)       
                if myCenterx < screen.get_rect().centerx - 30 or myCenterx > screen.get_rect().centerx + 30:
                    myCenterx += speed_rect_fast
                else:
                    myCenterx += speed_rect_slow
                    
            if index_betweenLevel == 400:
                if pass_level < 3:
                    pass_level = 3
                    save_game()
                return 1
                
        if boss_flag == 0 and boss1_down_flag == 0 and boss2_down_flag == 0 and flag_betweenLevel == 0:
            if myTime % (80 - int(myTime / 60)) == 0 and myTime <= 3000:  # 通过这个数字来确定出现的频率
                enemy1_pos = [random.randint(0, SCREEN_WIDTH - enemy1_rect[0].width), 0]
                enemy1 = Enemy1(enemy1_img, enemy1_down_img, enemy1_pos)
                enemies1.add(enemy1)    
                
         #生成boss
        if myTime == 3300:
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
                if player.is_hit is not True:
                    player.is_hit = True
                    game_over_sound.play()
                    boss1.life -= boss1.bomb_damage
                else:
                    pass
            if pygame.sprite.collide_rect(boss2, player):
                if player.is_hit is not True:
                    player.is_hit = True
                    game_over_sound.play()
                    boss2.life -= boss2.bomb_damage         
                else:
                    pass
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
                if (enemy1.rect.centery - player.rect.centery) < -35:
                    if abs(enemy1.rect.centerx - player.rect.centerx) < 30:
                        enemies1_down.add(enemy1)
                        enemies1.remove(enemy1)
                        player.is_hit = True
                        game_over_sound.play() 
                        break
                    else:
                        pass
                        
                elif (enemy1.rect.centery - player.rect.centery) > 50:                    
                    pass
                else:
                    enemies1_down.add(enemy1)
                    enemies1.remove(enemy1)
                    player.is_hit = True
                    game_over_sound.play() 
                    break
                    
            if enemy1.rect.top > SCREEN_HEIGHT:
                enemies1.remove(enemy1)   

        if boss_once_flag == 1:
            if pygame.sprite.spritecollideany(player, boss1.enemy_bullets) :
                if (enemy_bullet.rect.centery - player.rect.centery) < -35:
                    if abs(enemy_bullet.rect.centerx - player.rect.centerx) < 20:
                        boss1.enemy_bullets.remove(enemy_bullet)
                        player.is_hit = True
                        game_over_sound.play() 
                    else:
                        pass
                        
                elif (enemy_bullet.rect.centery - player.rect.centery)  > 40:                    
                    pass
                else:
                    boss1.enemy_bullets.remove(enemy_bullet)
                    player.is_hit = True
                    game_over_sound.play()
                    
            boss1.enemy_bullets.draw(screen)   
            if pygame.sprite.spritecollideany(player, boss2.enemy_bullets) :
                if (enemy_bullet.rect.centery - player.rect.centery) < -35:
                    if abs(enemy_bullet.rect.centerx - player.rect.centerx) < 20:
                        boss2.enemy_bullets.remove(enemy_bullet)
                        player.is_hit = True
                        game_over_sound.play() 
                    else:
                        pass
                        
                elif (enemy_bullet.rect.centery - player.rect.centery)  > 40:                    
                    pass
                else:
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
                    flag_betweenLevel = 1
                    myGame = 1
                    myScore = player.score
                
        if boss2_down_flag == 1:
            img_index2 = boss2.down_index // 10
            screen.blit(boss2.down_images[img_index2], boss2.rect)
            boss2.down_index += 1
            if boss2.down_index == 59:
                boss2_down_flag = 2
                if boss_flag == 0:
                    flag_betweenLevel = 1
                    myGame = 1
                    myScore = player.score
              
        # 生成奖励
        if award_frequency == award_time and flag_betweenLevel == 0:
            type = random.randint(0, 20)
            if type < 13:
                position = [random.randint(0, SCREEN_WIDTH - double_bullet_rect.width), 0]
                award = Award(double_bullet_img, double_bullet_effect, position)
                award.kind = 1
            else:
                position = [random.randint(0, SCREEN_WIDTH - bomb_rect.width), 0]
                award = Award(bomb_img, bomb_effect, position)
                award.kind = 2
                
            awards.add(award)
            award_frequency = 1
            min_time = 900 - int(player.score / 12)
            if min_time < 750:
                min_time = 750
            max_time = 1200 - int(player.score / 10)
            if max_time < 1000:
                max_time = 1000
            award_time = random.randint(min_time, max_time)
        else:
            award_frequency += 1
            
        for award in awards:
            award.move()
                #是否获得奖励
            if pygame.sprite.collide_rect(player, award):
                if award.kind == 1:
                    player.NL_bullet_time = 400
                    get_bullet_sound.play()
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
                myGame = 0
                myScore = player.score
                return boss_flag # 效果结束后这个循环就结束了
                
 # 绘制子弹和和奖励和敌机
        player.bullets.draw(screen)
        awards.draw(screen)
        enemies1.draw(screen)
            
        # 绘制得分
        # score_font = pygame.font.Font('freesansbold.ttf', 32)  # 字体大小的
        score_text = score_font.render(str(player.score), True, (128, 128, 128))   # RGB三个通道，表示颜色是灰色
        text_rect = score_text.get_rect()
        text_rect.topleft = [10, 5]
        screen.blit(score_text, text_rect)
        # 绘制boss血量
        if boss_flag == 1 and boss1_down_flag == 0:
            # boss_life_font = pygame.font.Font('freesansbold.ttf', 22)
            strbosslife = ''
            for i in range(0, boss1.life):
                strbosslife += '[]'
            boss_life_text = boss_life_font.render('Boss1 level2: ' + strbosslife, True, (128, 128, 128))
            boss_life_rect = boss_life_text.get_rect()
            boss_life_rect.topleft = [30, SCREEN_HEIGHT - 70]
            screen.blit(boss_life_text, boss_life_rect)
            
        if boss_flag == 1 and boss2_down_flag == 0:
            # boss_life_font = pygame.font.Font('freesansbold.ttf', 22)
            strbosslife = ''
            for i in range(0, boss2.life):
                strbosslife += '[]'
            boss_life_text = boss_life_font.render('Boss2 level2: ' + strbosslife, True, (128, 128, 128))
            boss_life_rect = boss_life_text.get_rect()
            boss_life_rect.topleft = [30, SCREEN_HEIGHT - 40]
            screen.blit(boss_life_text, boss_life_rect)       
            
        # 绘制子弹数目和bomb数目
        # bullet_font = pygame.font.Font('freesansbold.ttf', 20)
        if player.NL_bullet_time > 0:
            bullet_text = bullet_font.render('Bullet: ', True, (128, 128, 128))
            position = SCREEN_WIDTH - 65
            for i in range(0, 5):
                screen.blit(bullet_img, ((position + i * 12), 10))
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
        # bomb_font = pygame.font.Font('freesansbold.ttf', 20)
        bomb_text = bomb_font.render('Bomb x ' + str(player.bomb), True, (128, 128, 128))
        bombText_rect = bomb_text.get_rect()
        bombText_rect.topleft = [SCREEN_WIDTH - 130, 35]
        screen.blit(bomb_text, bombText_rect)
        # screen.blit(timeout_img, (SCREEN_WIDTH - 100, 60))
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
                    if boss_flag == 1 and boss1.flag_showup == 1:
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
                
         # 按t来暂停
            if timeout_frequency < 20:
                timeout_frequency += 1
            if key_pressed[K_t] and timeout_frequency == 20:
                flag_timeout = True
                timeout_frequency = 0
                while(1): 
                    clock.tick(60)
                    timeout_rect = timeout_text.get_rect()
                    timeout_rect.centerx = screen.get_rect().centerx
                    timeout_rect.centery = screen.get_rect().centery
                    screen.blit(timeout_text, timeout_rect)
                    pygame.display.update()
                    if timeout_frequency < 20:
                        timeout_frequency += 1
                    if not flag_timeout:
                        timeout_frequency = 0
                        break
                    key_pressed = pygame.key.get_pressed()
                    if key_pressed[K_t] and timeout_frequency == 20:
                        flag_timeout = False
                        timeout_frequency = 0
                    for timeout_event in pygame.event.get():
                        if timeout_event.type == pygame.QUIT:
                            pygame.quit()
                            exit()   
            
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
            get_bullet_sound.play()  # 效果失效时提醒一下
            
        # 更新屏幕
        pygame.display.update()
        myTime += 1
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()      

def level3(clock, player, flag_saw_boss, again):
    if again == 1:
        player.bullet = 5
        player.bomb = 1
        player.index = 0
        player.down_index = 0
        player.rect.topleft = player_pos
        player.is_hit = False
        player.score = 0
        player.NL_bullet_time = 0
        
    enemies1 = pygame.sprite.Group()  # enemy1的group
    enemies2 = pygame.sprite.Group()  # enemy2的group
    awards = pygame.sprite.Group()  # 奖励的group
    enemies1_down = pygame.sprite.Group()  # 被击毁的就放入这个group中一起处理
    enemies2_down = pygame.sprite.Group()
    enemy2_once_flag = 0
    award_frequency = 1
    award_time = 100  # 第一个award出现
    boss_flag = flag_saw_boss
    if boss_flag == 1:
        myTime = 3400
    else:
        myTime = 0
    boss_down_flag = 0
    boss_once_flag = 0
    running = 1
    boss_begin = 1 # boss第一次出现的flag
    flag_betweenLevel = 0
    index_betweenLevel = 0
    global myScore 
    global myGame
    global pass_level
    openingFont = pygame.font.Font('freesansbold.ttf', 50)
    level4Text = openingFont.render("--LEVEL4--", True, (0, 0, 0))
    level4Text_rect = level4Text.get_rect()
    myCenterx = screen.get_rect().centerx - 830
    myCentery = screen.get_rect().centery
    speed_rect_slow = 0.5
    speed_rect_fast = 80
    score_font = pygame.font.Font('freesansbold.ttf', 32)  # 字体大小的
    boss_life_font = pygame.font.Font('freesansbold.ttf', 22)
    bullet_font = pygame.font.Font('freesansbold.ttf', 20)
    bomb_font = pygame.font.Font('freesansbold.ttf', 20)
    timeout_frequency = 20
    flag_timeout = False
    timeout_font = pygame.font.Font('freesansbold.ttf', 50)
    timeout_text = timeout_font.render('Time Out...', True, (0, 100, 200))
    
    while running:
        # 控制游戏最大帧率为60
        clock.tick(60)
        # 绘制背景
        screen.fill(0)
        screen.blit(background, (0, 0))
        
        if flag_betweenLevel == 1:
            if index_betweenLevel == 0:
                beat_boss_sound.play()
            index_betweenLevel += 1
            
            if index_betweenLevel >= 200 and index_betweenLevel <= 350:
                level4Text_rect.centerx = myCenterx
                level4Text_rect.centery = myCentery
                
                screen.blit(level4Text, level4Text_rect)       
                if myCenterx < screen.get_rect().centerx - 30 or myCenterx > screen.get_rect().centerx + 30:
                    myCenterx += speed_rect_fast
                else:
                    myCenterx += speed_rect_slow
                    
            if index_betweenLevel == 400:
                if pass_level < 4:
                    pass_level = 4
                    save_game()
                return 1
                
        # 生成两种敌人
        if boss_flag == 0 and boss_down_flag == 0 and flag_betweenLevel == 0:
            if myTime % (100 - int(myTime / 70)) == 0 and myTime <= 3200:  # 通过这个数字来确定出现的频率
                enemy1_pos = [random.randint(0, SCREEN_WIDTH - enemy1_rect[0].width), 0]
                enemy1 = Enemy1(enemy1_img, enemy1_down_img, enemy1_pos)
                enemies1.add(enemy1)    
                
        if boss_flag == 0 and boss_down_flag == 0 and flag_betweenLevel == 0:
            if myTime % 500 == 0 and myTime > 0:  # 通过这个数字来确定出现的频率, 不要一上来就有
                enemy2_pos = [random.randint(0, SCREEN_WIDTH - enemy2_rect[0].width), 0]
                enemy2 = Enemy2(enemy2_img, enemy2_down_img, enemy2_pos)
                enemies2.add(enemy2)
                if enemy2_once_flag == 0:
                    enemy2_once_flag = 1
                
         #生成boss
        if myTime == 3400:
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
                if boss_begin == 1:
                    if positionx > 300 and positionx < 500:
                        boss.teleportation_defence(positionx)
                    boss_begin = 0
                if boss.bullet > 5 and boss.mode == 0:
                    boss.mode = 1
                    boss.ishit_flag = 0
                elif boss.bullet < 2 and boss.mode == 1:
                    boss.mode = 0  
                    #瞬间移动
                if boss.ishit_flag == 1 and boss.mode == 0 and boss.teleportation == 0:
                    boss.teleportation_defence(positionx)
                    boss.ishit_flag = 0
                    boss.teleportation = boss.teleportation_recharge
                    boss.mode = 1
                elif boss.mode == 1 and abs(target) > 200 and boss.teleportation == 0 and positiony < 350:
                    boss.teleportation_attack(positionx)
                    boss.teleportation = boss.teleportation_recharge
                    
                if boss.teleportation > 0:
                    boss.teleportation -= 1
                if boss.ishit_flag == 1:
                    boss.ishit_flag = 0  # 只是那一下才会触发，之后就没有ishit的flag了
                    
                boss.move(target, boss.mode)
                
                if boss.bullet > 0: 
                    if boss.mode == 1:
                        if boss.shoot_frequency >= 20:
                            if abs(target) < 100:
                                boss.normal_shoot(bullet_enemy_img)
                                bullet_sound.play()
                                boss.shoot_frequency = 0
                                boss.bullet -= 1
                                boss.shoot_flag = 1
                        else:
                            boss.shoot_frequency += 1
                            
                    if boss.mode == 0:
                        if boss.shoot_frequency >= 40:
                            if abs(target) < 150:
                                boss.normal_shoot(bullet_enemy_img)
                                bullet_sound.play()
                                boss.shoot_frequency = 0
                                boss.bullet -= 1
                                boss.shoot_flag = 1 # 绘制攻击的boss
                        else:
                            boss.shoot_frequency += 1     
                            
                if boss.bullet < boss.bullet_max:
                    if boss.recharging == 0:
                        boss.bullet += 1
                        boss.recharging = boss.recharge_time
                    else:
                        boss.recharging -= 1
                        
            else:
                boss.show()
                if boss.flag_sound == 0:
                    boss_show_sound.play()
                    boss.flag_sound = 1
                # screen.blit(boss.images[0], boss.rect)
            if boss.shoot_flag == 1:
                boss.index = (boss.shoot_frequency // (int(boss.shoot_frequency / 2) + 1)) + 1
                screen.blit(boss.images[boss.index], boss.rect)
                if (boss.shoot_frequency == 20 and boss.mode == 1) or (boss.shoot_frequency == 40 and boss.mode == 0):
                    boss.shoot_flag = 0
            else:
                screen.blit(boss.images[0], boss.rect)        
                    
            #boss和玩家相撞   
            if pygame.sprite.collide_rect(boss, player):
                if player.is_hit is not True:
                    player.is_hit = True
                    game_over_sound.play()
                    boss.life -= boss.bomb_damage
                else:
                    pass
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
                if (enemy_bullet.rect.centery - player.rect.centery) < -35:
                    if abs(enemy_bullet.rect.centerx - player.rect.centerx) < 20:
                        boss.enemy_bullets.remove(enemy_bullet)
                        player.is_hit = True
                        game_over_sound.play() 
                    else:
                        pass
                        
                elif (enemy_bullet.rect.centery - player.rect.centery)  > 40:                    
                    pass
                else:
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
                if (enemy1.rect.centery - player.rect.centery) < -35:
                    if abs(enemy1.rect.centerx - player.rect.centerx) < 30:
                        enemies1_down.add(enemy1)
                        enemies1.remove(enemy1)
                        player.is_hit = True
                        game_over_sound.play() 
                        break
                    else:
                        pass
                        
                elif (enemy1.rect.centery - player.rect.centery) > 50:                    
                    pass
                else:
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
                if (enemy2.rect.centery - player.rect.centery) < -50:
                    if abs(enemy2.rect.centerx - player.rect.centerx) < 35:
                        enemies2_down.add(enemy2)
                        enemies2.remove(enemy2)
                        player.is_hit = True
                        game_over_sound.play() 
                        break

                    else:
                        pass
                        
                elif (enemy2.rect.centery - player.rect.centery) > 70:                    
                    pass
                else:
                    enemies2_down.add(enemy2)
                    enemies2.remove(enemy2)
                    player.is_hit = True
                    game_over_sound.play() 
                    break

            if enemy2.rect.top > SCREEN_HEIGHT:
                enemies2.remove(enemy2)   

        if enemy2_once_flag == 1:
            if pygame.sprite.spritecollideany(player, enemy2.enemy_bullets) :
                if (enemy_bullet.rect.centery - player.rect.centery) < -35:
                    if abs(enemy_bullet.rect.centerx - player.rect.centerx) < 20:
                        enemy2.enemy_bullets.remove(enemy_bullet)
                        player.is_hit = True
                        game_over_sound.play() 
                    else:
                        pass
                        
                elif (enemy_bullet.rect.centery - player.rect.centery)  > 40:                    
                    pass
                else:
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
                flag_betweenLevel = 1
                myGame = 1
                myScore = player.score

        # 生成奖励
        if award_frequency == award_time and flag_betweenLevel == 0:
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
            min_time = 700 - int(player.score / 15)
            if min_time < 500:
                min_time = 500
            max_time = 900 - int(player.score / 10)
            if max_time < 650:
                max_time = 650
            award_time = random.randint(min_time, max_time)
        else:
            award_frequency += 1
            
        for award in awards:
            award.move()
                #是否获得奖励
            if pygame.sprite.collide_rect(player, award):
                if award.kind == 1:
                    player.NL_bullet_time = 400
                    get_bullet_sound.play()
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
                # 效果结束后这个循环就结束了
                myGame = 0
                myScore = player.score
                return boss_flag
                
 # 绘制子弹和和奖励和敌机
        player.bullets.draw(screen)
        awards.draw(screen)
        enemies1.draw(screen)
            
        # 绘制得分
        # score_font = pygame.font.Font('freesansbold.ttf', 32)  # 字体大小的
        score_text = score_font.render(str(player.score), True, (128, 128, 128))   # RGB三个通道，表示颜色是灰色
        text_rect = score_text.get_rect()
        text_rect.topleft = [10, 5]
        screen.blit(score_text, text_rect)
        # 绘制boss血量
        if boss_flag == 1 and boss_down_flag == 0:
            # boss_life_font = pygame.font.Font('freesansbold.ttf', 22)
            strbosslife = ''
            for i in range(0, boss.life):
                strbosslife += '[]'
            boss_life_text = boss_life_font.render('Boss level3: ' + strbosslife, True, (128, 128, 128))
            boss_life_rect = boss_life_text.get_rect()
            boss_life_rect.topleft = [30, SCREEN_HEIGHT - 40]
            screen.blit(boss_life_text, boss_life_rect)
                
        # 绘制子弹数目和bomb数目
        # bullet_font = pygame.font.Font('freesansbold.ttf', 20)
        if player.NL_bullet_time > 0:
            bullet_text = bullet_font.render('Bullet: ', True, (128, 128, 128))
            position = SCREEN_WIDTH - 65
            for i in range(0, 5):
                screen.blit(bullet_img, ((position + i * 12), 10))
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
        # bomb_font = pygame.font.Font('freesansbold.ttf', 20)
        bomb_text = bomb_font.render('Bomb x ' + str(player.bomb), True, (128, 128, 128))
        bombText_rect = bomb_text.get_rect()
        bombText_rect.topleft = [SCREEN_WIDTH - 130, 35]
        screen.blit(bomb_text, bombText_rect)
        # screen.blit(timeout_img, (SCREEN_WIDTH - 100, 60))
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
                    if boss_flag == 1 and boss.flag_showup == 1:
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
                
         # 按t来暂停
            if timeout_frequency < 20:
                timeout_frequency += 1
            if key_pressed[K_t] and timeout_frequency == 20:
                flag_timeout = True
                timeout_frequency = 0
                while(1): 
                    clock.tick(60)
                    timeout_rect = timeout_text.get_rect()
                    timeout_rect.centerx = screen.get_rect().centerx
                    timeout_rect.centery = screen.get_rect().centery
                    screen.blit(timeout_text, timeout_rect)
                    pygame.display.update()
                    if timeout_frequency < 20:
                        timeout_frequency += 1
                    if not flag_timeout:
                        timeout_frequency = 0
                        break
                    key_pressed = pygame.key.get_pressed()
                    if key_pressed[K_t] and timeout_frequency == 20:
                        flag_timeout = False
                        timeout_frequency = 0
                    for timeout_event in pygame.event.get():
                        if timeout_event.type == pygame.QUIT:
                            pygame.quit()
                            exit()   
            
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
            get_bullet_sound.play()  # 效果失效时提醒一下
            
        # 更新屏幕
        pygame.display.update()
        myTime += 1
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()    

def level4(clock, player, flag_saw_boss, again):
    if again == 1:
        player.bullet = 5
        player.bomb = 1
        player.index = 0
        player.down_index = 0
        player.rect.topleft = player_pos
        player.is_hit = False
        player.score = 0
        player.NL_bullet_time = 0
        
    enemies1 = pygame.sprite.Group()  # enemy1的group
    enemies2 = pygame.sprite.Group()  # enemy2的group
    awards = pygame.sprite.Group()  # 奖励的group
    enemies1_down = pygame.sprite.Group()  # 被击毁的就放入这个group中一起处理
    enemies2_down = pygame.sprite.Group() 
    enemy2_once_flag = 0
    award_frequency = 1
    award_time = 100  # 第一个award出现
    boss_flag = flag_saw_boss
    if boss_flag == 1:
        myTime = 3900
    else:
        myTime = 0
    boss_down_flag = 0
    boss_once_flag = 0
    running = 1
    boss_begin = 1 # boss第一次出现的flag
    flag_betweenLevel = 0
    index_betweenLevel = 0
    flag_enemy1_boss = 0 # boss放小飞机的flag
    enemy1_boss_frequency = 1
    flag_enemy1_boss_once = 0 #出现过的flag
    global myScore 
    global myGame
    global pass_level
    openingFont = pygame.font.Font('freesansbold.ttf', 50)
    level5Text = openingFont.render("--LEVEL5--", True, (0, 0, 0))
    level5Text_rect = level5Text.get_rect()
    myCenterx = screen.get_rect().centerx - 830
    myCentery = screen.get_rect().centery
    speed_rect_slow = 0.5
    speed_rect_fast = 80
    score_font = pygame.font.Font('freesansbold.ttf', 32)  # 字体大小的
    boss_life_font = pygame.font.Font('freesansbold.ttf', 22)
    bullet_font = pygame.font.Font('freesansbold.ttf', 20)
    bomb_font = pygame.font.Font('freesansbold.ttf', 20)
    timeout_frequency = 20
    flag_timeout = False
    timeout_font = pygame.font.Font('freesansbold.ttf', 50)
    timeout_text = timeout_font.render('Time Out...', True, (0, 100, 200))
    
    while running:
        # 控制游戏最大帧率为60
        clock.tick(60)
        # 绘制背景
        screen.fill(0)
        screen.blit(background, (0, 0))
        
        if flag_betweenLevel == 1:
            if index_betweenLevel == 0:
                beat_boss_sound.play() 
            index_betweenLevel += 1
            
            if index_betweenLevel >= 200 and index_betweenLevel <= 350:
                level5Text_rect.centerx = myCenterx
                level5Text_rect.centery = myCentery
                
                screen.blit(level5Text, level5Text_rect)       
                if myCenterx < screen.get_rect().centerx - 30 or myCenterx > screen.get_rect().centerx + 30:
                    myCenterx += speed_rect_fast
                else:
                    myCenterx += speed_rect_slow
                    
            if index_betweenLevel == 400:
                if pass_level < 5:
                    pass_level = 5
                    save_game()
                return 1
                
        # 生成两种敌人
        if boss_flag == 0 and boss_down_flag == 0 and flag_betweenLevel == 0:
            if myTime % (70 - int(myTime / 120)) == 0 and myTime <= 3600:  # 通过这个数字来确定出现的频率
                enemy1_pos = [random.randint(0, SCREEN_WIDTH - enemy1_rect[0].width), 0]
                enemy1 = Enemy1_level4(enemy1_img, enemy1_down_img, enemy1_pos)
                enemies1.add(enemy1)    
                
        if boss_flag == 0 and boss_down_flag == 0 and flag_betweenLevel == 0:
            if myTime % 500 == 0 and myTime > 0:  # 通过这个数字来确定出现的频率
                enemy2_pos = [random.randint(0, SCREEN_WIDTH - enemy2_rect[0].width), 0]
                enemy2 = Enemy2(enemy2_img, enemy2_down_img, enemy2_pos)
                enemies2.add(enemy2)
                if enemy2_once_flag == 0:
                    enemy2_once_flag = 1
                
         #生成boss
        if myTime == 3900:
            boss = Boss_level4(boss_img, boss_down_img, boss_pos)
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
                if boss_begin == 1:
                    if positionx > 300 and positionx < 500:
                        boss.teleportation_defence(positionx)
                    boss_begin = 0
                if boss.bullet > 5 and boss.mode == 0:
                    boss.mode = 1
                    boss.ishit_flag = 0
                elif boss.bullet < 2 and boss.mode == 1:
                    boss.mode = 0  
                    #瞬间移动
                if boss.ishit_flag == 1 and boss.mode == 0 and boss.teleportation == 0:
                    boss.teleportation_defence(positionx)
                    boss.ishit_flag = 0
                    boss.teleportation = boss.teleportation_recharge
                    boss.mode = 1
                elif boss.mode == 1 and abs(target) > 200 and boss.teleportation == 0 and positiony < 350:
                    boss.teleportation_attack(positionx)
                    boss.teleportation = boss.teleportation_recharge
                    
                if boss.teleportation > 0:
                    boss.teleportation -= 1
                if boss.ishit_flag == 1:
                    boss.ishit_flag = 0  # 只是那一下才会触发，之后就没有ishit的flag了
                # 放小兵
                if boss.life <= 10:
                    if boss.enemy1_frequency <= 0:
                        flag_enemy1_boss = 1
                        boss.enemy1_number = 5
                        boss.enemy1_frequency = boss.enemy1_frequency_recharge
                    else:
                        boss.enemy1_frequency -= 1
                        
                if flag_enemy1_boss == 1:      
                    if enemy1_boss_frequency % 15 == 0:
                        enemy1_boss_frequency = 1
                        enemy1_pos = [random.randint(0, SCREEN_WIDTH - enemy1_rect[0].width), 0]
                        enemy1_boss = Enemy1_Boss(enemy1_img, enemy1_down_img, enemy1_pos)
                        enemies1.add(enemy1_boss)
                        boss.enemy1_number -= 1
                        if flag_enemy1_boss_once == 0:
                            flag_enemy1_boss_once = 1
                        if boss.enemy1_number == 0:
                            flag_enemy1_boss = 0
                    else:
                        enemy1_boss_frequency += 1
                    
                boss.move(target, boss.mode)
                
                if boss.bullet > 0: 
                    if boss.mode == 1:
                        if boss.shoot_frequency >= 15:
                            if abs(target) < 100:
                                if boss.furious_frequency <= 0:
                                    boss.furious_shoot(bullet_enemy_img)
                                    boss.furious_shoot_number -= 1
                                    if boss.furious_shoot_number == 0:
                                        boss.furious_frequency = boss.furious_frequency_recharge
                                        boss.furious_shoot_number = 10
                                else:
                                    boss.normal_shoot(bullet_enemy_img)
                                    boss.furious_frequency -= 1
                                bullet_sound.play()
                                boss.shoot_frequency = 0
                                boss.bullet -= 1
                                boss.shoot_flag = 1
                            else:
                                boss.furious_frequency -= 1
                        else:
                            boss.shoot_frequency += 1
                            boss.furious_frequency -= 1
                            
                    if boss.mode == 0:
                        if boss.shoot_frequency >= 40:
                            if abs(target) < 150:
                                if boss.furious_frequency <= 0:
                                    boss.furious_shoot(bullet_enemy_img)
                                    boss.furious_shoot_number -= 1
                                    if boss.furious_shoot_number == 0:
                                        boss.furious_frequency = boss.furious_frequency_recharge
                                        boss.furious_shoot_number = 10
                                else:
                                    boss.normal_shoot(bullet_enemy_img)
                                    boss.furious_frequency -= 1                            
                                bullet_sound.play()
                                boss.shoot_frequency = 0
                                boss.bullet -= 1
                                boss.shoot_flag = 1 # 绘制攻击的boss
                            else:
                                boss.furious_frequency -= 1
                        else:
                            boss.shoot_frequency += 1
                            boss.furious_frequency -= 1                           
                            
                if boss.bullet < boss.bullet_max:
                    if boss.recharging == 0:
                        boss.bullet += 1
                        boss.recharging = boss.recharge_time
                    else:
                        boss.recharging -= 1
                        
            else:
                boss.show()
                if boss.flag_sound == 0:
                    boss_show_sound.play()
                    boss.flag_sound = 1
            if boss.shoot_flag == 1:
                boss.index = (boss.shoot_frequency // (int(boss.shoot_frequency / 2) + 1)) + 1
                screen.blit(boss.images[boss.index], boss.rect)
                if (boss.shoot_frequency == 20 and boss.mode == 1) or (boss.shoot_frequency == 40 and boss.mode == 0):
                    boss.shoot_flag = 0
            else:
                screen.blit(boss.images[0], boss.rect)        
                    
            #boss和玩家相撞   
            if pygame.sprite.collide_rect(boss, player):
                if player.is_hit is not True:
                    player.is_hit = True
                    game_over_sound.play()
                    boss.life -= boss.bomb_damage
                else:
                    pass
            #发现没有合适的函数，要去看文档！！
            if pygame.sprite.spritecollideany(boss, player.bullets):
                if boss.flag_showup == 1:
                    boss.life -= 1
                    boss.ishit_flag = 1
                player.bullets.remove(bullet) #要注意一旦击中就要删除子弹，不然下次循环还会把这颗子弹算上去
                #注意一开始player和boss的子弹都是bullet，然后就有问题了，remove不掉了，后来把boss的子弹名字改成enemy_bullet就OK了
            if boss.life <= 0:
                if flag_enemy1_boss:
                    for enemy1 in enemies1:
                        enemies1_down.add(enemy1)
                        enemies1.remove(enemy1)
                boss_flag = 0
                boss_down_flag = 1
                player.score += 1000
                boss_down_sound.play() 
                
        if boss_once_flag == 1:
            if pygame.sprite.spritecollideany(player, boss.enemy_bullets) :
                if (enemy_bullet.rect.centery - player.rect.centery) < -35:
                    if abs(enemy_bullet.rect.centerx - player.rect.centerx) < 20:
                        boss.enemy_bullets.remove(enemy_bullet)
                        player.is_hit = True
                        game_over_sound.play() 
                    else:
                        pass
                        
                elif (enemy_bullet.rect.centery - player.rect.centery)  > 40:                    
                    pass
                else:
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
            if flag_enemy1_boss_once == 1:
                target = (player.rect.left + player.rect.right) / 2 - (enemy1.rect.left + enemy1.rect.right) / 2
                enemy1.move(target)
            else:
                enemy1.move()
            # 判断玩家是否被击中
            if pygame.sprite.collide_rect(enemy1, player):
                if (enemy1.rect.centery - player.rect.centery) < -35:
                    if abs(enemy1.rect.centerx - player.rect.centerx) < 30:
                        enemies1_down.add(enemy1)
                        enemies1.remove(enemy1)
                        player.is_hit = True
                        game_over_sound.play() 
                        break
                    else:
                        pass
                        
                elif (enemy1.rect.centery - player.rect.centery) > 50:                    
                    pass
                else:
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
                if (enemy2.rect.centery - player.rect.centery) < -50:
                    if abs(enemy2.rect.centerx - player.rect.centerx) < 35:
                        enemies2_down.add(enemy2)
                        enemies2.remove(enemy2)
                        player.is_hit = True
                        game_over_sound.play() 
                        break

                    else:
                        pass
                        
                elif (enemy2.rect.centery - player.rect.centery) > 70:                    
                    pass
                else:
                    enemies2_down.add(enemy2)
                    enemies2.remove(enemy2)
                    player.is_hit = True
                    game_over_sound.play() 
                    break
                    
            if enemy2.rect.top > SCREEN_HEIGHT:
                enemies2.remove(enemy2)   

        if enemy2_once_flag == 1:
            if pygame.sprite.spritecollideany(player, enemy2.enemy_bullets) :
                if (enemy_bullet.rect.centery - player.rect.centery) < -35:
                    if abs(enemy_bullet.rect.centerx - player.rect.centerx) < 20:
                        enemy2.enemy_bullets.remove(enemy_bullet)
                        player.is_hit = True
                        game_over_sound.play() 
                    else:
                        pass
                        
                elif (enemy_bullet.rect.centery - player.rect.centery)  > 40:                    
                    pass
                else:
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
            img_index = boss.down_index // 25
            screen.blit(boss_down_img[img_index], boss.rect)
            boss.down_index += 1
            target = (player.rect.left + player.rect.right) / 2 - (boss.rect.left + boss.rect.right) / 2
            boss.suicide_move(target)
            if pygame.sprite.collide_rect(boss, player):
                if player.is_hit is not True:
                    player.is_hit = True
                    game_over_sound.play()
            if boss.down_index == 149:
                boss_down_flag = 0
                boss_flag = 0
                flag_betweenLevel = 1
                myGame = 1
                myScore = player.score
        
        # 生成奖励
        if award_frequency == award_time and flag_betweenLevel == 0:
            type = random.randint(0, 20)
            if type < 13:
                position = [random.randint(0, SCREEN_WIDTH - double_bullet_rect.width), 0]
                award = Award(double_bullet_img, double_bullet_effect, position)
                award.kind = 1
            else:
                position = [random.randint(0, SCREEN_WIDTH - bomb_rect.width), 0]
                award = Award(bomb_img, bomb_effect, position)
                award.kind = 2
                
            awards.add(award)
            award_frequency = 1
            min_time = 700 - int(player.score / 20)
            if min_time < 400:
                min_time = 400
            max_time = 900 - int(player.score / 15)
            if max_time < 600:
                max_time = 600
            award_time = random.randint(min_time, max_time)
        else:
            award_frequency += 1
            
        for award in awards:
            award.move()
                #是否获得奖励
            if pygame.sprite.collide_rect(player, award):
                if award.kind == 1:
                    player.NL_bullet_time = 400
                    get_bullet_sound.play()
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
                myGame = 0
                myScore = player.score
                return (boss_flag or boss_down_flag)
                
 # 绘制子弹和和奖励和敌机
        player.bullets.draw(screen)
        awards.draw(screen)
        enemies1.draw(screen)
            
        # 绘制得分
        # score_font = pygame.font.Font('freesansbold.ttf', 32)  # 字体大小的
        score_text = score_font.render(str(player.score), True, (128, 128, 128))   # RGB三个通道，表示颜色是灰色
        text_rect = score_text.get_rect()
        text_rect.topleft = [10, 5]
        screen.blit(score_text, text_rect)
        # 绘制boss血量
        if boss_flag == 1 and boss_down_flag == 0:
            # boss_life_font = pygame.font.Font('freesansbold.ttf', 22)
            strbosslife = ''
            for i in range(0, boss.life):
                strbosslife += '[]'
            boss_life_text = boss_life_font.render('Boss level4: ' + strbosslife, True, (128, 128, 128))
            boss_life_rect = boss_life_text.get_rect()
            boss_life_rect.topleft = [30, SCREEN_HEIGHT - 40]
            screen.blit(boss_life_text, boss_life_rect)
                
        # 绘制子弹数目和bomb数目
        # bullet_font = pygame.font.Font('freesansbold.ttf', 20)
        if player.NL_bullet_time > 0:
            bullet_text = bullet_font.render('Bullet: ', True, (128, 128, 128))
            position = SCREEN_WIDTH - 65
            for i in range(0, 5):
                screen.blit(bullet_img, ((position + i * 12), 10))
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
        # bomb_font = pygame.font.Font('freesansbold.ttf', 20)
        bomb_text = bomb_font.render('Bomb x ' + str(player.bomb), True, (128, 128, 128))
        bombText_rect = bomb_text.get_rect()
        bombText_rect.topleft = [SCREEN_WIDTH - 130, 35]
        screen.blit(bomb_text, bombText_rect)
        # screen.blit(timeout_img, (SCREEN_WIDTH - 100, 60))
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
                    if boss_flag == 1 and boss.flag_showup == 1:
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
                
         # 按t来暂停
            if timeout_frequency < 20:
                timeout_frequency += 1
            if key_pressed[K_t] and timeout_frequency == 20:
                flag_timeout = True
                timeout_frequency = 0
                while(1): 
                    clock.tick(60)
                    timeout_rect = timeout_text.get_rect()
                    timeout_rect.centerx = screen.get_rect().centerx
                    timeout_rect.centery = screen.get_rect().centery
                    screen.blit(timeout_text, timeout_rect)
                    pygame.display.update()
                    if timeout_frequency < 20:
                        timeout_frequency += 1
                    if not flag_timeout:
                        timeout_frequency = 0
                        break
                    key_pressed = pygame.key.get_pressed()
                    if key_pressed[K_t] and timeout_frequency == 20:
                        flag_timeout = False
                        timeout_frequency = 0
                    for timeout_event in pygame.event.get():
                        if timeout_event.type == pygame.QUIT:
                            pygame.quit()
                            exit()   
            
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
            get_bullet_sound.play()  # 效果失效时提醒一下
            
        # 更新屏幕
        pygame.display.update()
        myTime += 1
            
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
  
def level5(clock, player, flag_saw_boss, again):
    if again == 1:
        player.bullet = 5
        player.bomb = 1
        player.index = 0
        player.down_index = 0
        player.rect.topleft = player_pos
        player.is_hit = False
        player.score = 0
        player.NL_bullet_time = 0
        
    enemies1 = pygame.sprite.Group()  # enemy1的group
    enemies2 = pygame.sprite.Group()  # enemy2的group
    awards = pygame.sprite.Group()  # 奖励的group
    enemies1_down = pygame.sprite.Group()  # 被击毁的就放入这个group中一起处理
    enemies2_down = pygame.sprite.Group()
    enemy2_once_flag = 0
    award_frequency = 1
    award_time = 100  # 第一个award出现
    boss_flag = flag_saw_boss
    if boss_flag == 1:
        myTime = 3900
    else:
        myTime = 0
    boss_down_flag = 0
    boss_once_flag = 0
    running = 1
    boss_begin = 1 # boss第一次出现的flag
    flag_betweenLevel = 0
    index_betweenLevel = 0
    boss_summon_flag = 0 # boss召唤的flag
    boss_summon_down_flag = 0
    boss_summon_once_flag = 0
    global myScore 
    global myGame
    plotFont = pygame.font.Font('freesansbold.ttf', 19)    
    flag_dialog = 0
    flag_firstDialog = 0
    plot = []
    plot.append("(You can use the space key to read the conversation or use 'b' to skip it)")
    plot.append("[Player: You seem a little different.]")
    plot.append("[Boss: Well I am the final boss so that makes sense]")
    plot.append("[Player: ...You, really?]")
    plot.append("[Boss: Have you heard 'Don't juge a book by its cover?']")
    plot.append("[Player: That's true. This game is full of surprise...]")
    plot.append("[Boss: Well that's because the designer is a genius]")
    plot.append("[Boss: I must say that you are not bad to come through all these enemies.]")
    plot.append("[Boss: And here you are in front of me.]")
    plot.append("[Player: I didn't expect the final boss to be so, so you...]")
    plot.append("[Boss: That's because you are too young and sometimes, too naive.]")
    plot.append("[Boss: You should always be careful of the ordinary.]")
    plot.append("[Player: Ok I got the point. So we are gonna fight or not?]") 
    plot.append("[Boss: Of course, I just want you to live longer ^_^]")
    plot.append("[Player: Let's cut the bullshit and I will give you some colors to look look!]")
    plot.append("[Boss: That's the spirit, may the better of us win ^_^]")    
    plot.append("(You can use the space key to read the conversation or use 'b' to skip it)")
    plot.append("[Boss: I lost! I didn't see it coming... You are good]")   
    plot.append("[Player: This fight was legen, wait for it... dary! Legendary!]")
    plot.append("[Boss: Whatever, either way we are gonna be deleted to free the memory]")
    plot.append("[Player: What are you talking about??]")
    plot.append("[Boss: Wake up young boy, we are just the objects in the program]")    
    plot.append("[Boss: And now after the fight, it's time to vanish. It is just our fates.]")  
    plot.append("[Player: No!! So this journey I came through means nothing?]")
    plot.append("[Boss: No, actually that's the point of life. We come alone and leave with nothing.]")
    plot.append("[Boss: You may have some legacies, but what's important is to enjoy this unique life]")
    plot.append("[Boss: Time to go, may you find your own joy in the real world ^_^]") 
    
    # myTime = 0
    x = 0 # index of plot
    dialog_index = 1 # 用来防止一按空格就连按了
    score_font = pygame.font.Font('freesansbold.ttf', 32)  # 字体大小的
    boss_life_font = pygame.font.Font('freesansbold.ttf', 22)
    bullet_font = pygame.font.Font('freesansbold.ttf', 20)
    bomb_font = pygame.font.Font('freesansbold.ttf', 20)
    timeout_frequency = 20
    flag_timeout = False
    timeout_font = pygame.font.Font('freesansbold.ttf', 50)
    timeout_text = timeout_font.render('Time Out...', True, (0, 100, 200))
    
    while running:
        # 控制游戏最大帧率为60
        clock.tick(60)
        # 绘制背景
        screen.fill(0)
        screen.blit(background, (0, 0))
        
        if flag_betweenLevel == 1 and flag_dialog == 0:
            if index_betweenLevel == 0:
                beat_boss_sound.play()
            index_betweenLevel += 1
            if index_betweenLevel == 30: 
                return 1

        # print flag_dialog
        # print x
        if flag_betweenLevel == 0 and flag_dialog == 1:    
            if x == 16:
                flag_dialog = 0
                flag_firstDialog = 1
                player.shoot_frequency = 1 # 为了防止最后一下空格发子弹，不是很重要，就是觉得这样比较完善。 The perfection is the cruel mistress ^^
            elif x < 16:
                plotText = plotFont.render(plot[x], True, (0, 50, 150))   # 灰蓝色的文字
                plotText_rect = plotText.get_rect()
                plotText_rect.centerx = screen.get_rect().centerx
                plotText_rect.centery = screen.get_rect().centery + 100
                screen.blit(plotText, plotText_rect)
                
        if flag_betweenLevel == 1 and flag_dialog == 1:    
           if x == 27:
               flag_dialog = 0
               player.shoot_frequency = 1 # 为了防止最后一下空格发子弹，不是很重要，就是觉得这样比较完善。 The perfection is the cruel mistress ^^
           elif x < 27:
               plotText = plotFont.render(plot[x], True, (0, 50, 150))   # 灰蓝色的文字
               plotText_rect = plotText.get_rect()
               plotText_rect.centerx = screen.get_rect().centerx
               plotText_rect.centery = screen.get_rect().centery + 100
               screen.blit(plotText, plotText_rect)            
               
        # enmey1有三种随机的行为模式
        if boss_flag == 0 and boss_down_flag == 0 and flag_betweenLevel == 0:
            if myTime % (70 - int(myTime / 120)) == 0 and myTime <= 3600:  # 通过这个数字来确定出现的频率
                enemy1_pos = [random.randint(0, SCREEN_WIDTH - enemy1_rect[0].width), 0]
                enemy1 = Enemy1_level5(enemy1_img, enemy1_down_img, enemy1_pos)
                enemies1.add(enemy1)    
         # enemy2 有enemy1的保护       
        if boss_flag == 0 and boss_down_flag == 0 and flag_betweenLevel == 0:
            if myTime % 500 == 0 and myTime > 0 and myTime <= 3500:  # 通过这个数字来确定出现的频率
                enemy2_pos = [random.randint(0, SCREEN_WIDTH - enemy2_rect[0].width), 0]
                enemy2 = Enemy2(enemy2_img, enemy2_down_img, enemy2_pos)
                enemies2.add(enemy2)
                # 致敬安德的游戏
                enemy1 = Enemy1_Ender(enemy1_img, enemy1_down_img, enemy2, -40, 0)
                enemies1.add(enemy1)   
                enemy1 = Enemy1_Ender(enemy1_img, enemy1_down_img, enemy2, -30, 30)
                enemies1.add(enemy1)   
                enemy1 = Enemy1_Ender(enemy1_img, enemy1_down_img, enemy2, 0, 55)
                enemies1.add(enemy1)   
                enemy1 = Enemy1_Ender(enemy1_img, enemy1_down_img, enemy2, 30, 30)
                enemies1.add(enemy1)   
                enemy1 = Enemy1_Ender(enemy1_img, enemy1_down_img, enemy2, 40, 0)
                enemies1.add(enemy1)   
                
                if enemy2_once_flag == 0:
                    enemy2_once_flag = 1
                
         #生成boss
        if myTime == 3900:
            boss = Boss_level5(enemy1_img, enemy1_down_img, boss_level5_pos)
            boss_once_flag = 1
            boss_flag = 1
                
        if boss_flag == 1:
            # print boss.flag_showup
            # print flag_dialog
            if boss.flag_showup == 1 and flag_dialog == 0:
                target = player.rect.centerx - boss.rect.centerx
                playerleft = list(player.rect.topleft)
                playerright = list(player.rect.topright)
                positionx = (playerleft[0] + playerright[0]) / 2
                positiony = playerleft[1]
                # print positiony
                if boss_begin == 1:
                    if positionx > 300 and positionx < 500:
                        boss.teleportation_defence(positionx)
                    boss_begin = 0
                if boss.bullet > 5 and boss.mode == 0:
                    boss.mode = 1
                    boss.ishit_flag = 0
                if boss.bullet < 2 and (boss.mode == 1 or boss.mode == 2):
                    boss.mode = 0
                    #瞬间移动
                    #防御模式被打倒躲到最远的地方
                if boss.ishit_flag == 1 and boss.mode == 0 and boss.teleportation == 0:
                    boss.teleportation_defence(positionx)
                    boss.ishit_flag = 0
                    boss.teleportation = boss.teleportation_recharge
                    boss.mode = 1
                    # 攻击模式如果发现player靠的很近就瞬移到玩家面前干他 LOL
                if boss.mode == 1 and abs(target) > 200 and boss.teleportation == 0 and positiony < 350:
                    boss.teleportation_attack(positionx)
                    boss.teleportation = boss.teleportation_recharge
                    # 计策模式，如果玩家靠着边太近就从旁边包抄干他 LOL
                if boss.mode == 1 and abs(target) > 500 and boss.teleportation == 0 and positionx < 150: 
                    boss.teleportation_attack(positionx + 300)
                    boss.teleportation = boss.teleportation_recharge
                    boss.mode = 2
                if boss.mode == 1 and abs(target) > 500 and boss.teleportation == 0 and positionx > 650: 
                    boss.teleportation_attack(positionx - 300)
                    boss.teleportation = boss.teleportation_recharge
                    boss.mode = 2
                    
                if boss.teleportation > 0:
                    boss.teleportation -= 1
                if boss.ishit_flag == 1:
                    boss.ishit_flag = 0  # 只是那一下才会触发，之后就没有ishit的flag了
                 
                if boss.life < 25 and boss.summon == 0 and boss_summon_flag == 0 and boss_summon_down_flag == 0:
                    boss_summon = Boss_summon(boss_img, boss_down_img, boss_pos)
                    boss_summon_flag = 1
                    boss_summon_once_flag = 1
                    boss.summon = boss.summon_recharge
                if boss.summon > 0:
                    boss.summon -= 1
                
                if boss.life < 15 and (boss.enemy1 == 0 or boss.enemy1 == 30 or boss.enemy1 == 60 or boss.enemy1 == 90):
                    for one in range(0, 5):
                        enemy1_pos = [random.randint(0, SCREEN_WIDTH - enemy1_rect[0].width), 0]
                        enemy1 = Enemy1_level5(enemy1_img, enemy1_down_img, enemy1_pos)
                        enemies1.add(enemy1)
                    if boss.enemy1 == 0:
                        boss.enemy1 = boss.enemy1_recharge
                if boss.life < 15:
                    if boss.enemy1 > 0:
                        boss.enemy1 -= 1
                    
                if boss.life < 10 and boss.bullet_max == 8:
                    # print 'Now boss raise the attack'
                    boss.bullet_max = 10
                    boss.bullet = 10
                    boss.shoot_frequency_time = 25
                    boss.recharge_time = 30
                    boss.speed = 7
                    boss.bomb_damage = 1
                    
                boss.move(target, boss.mode)
                
                if boss.bullet > 0: 
                    if boss.mode == 2:
                        if boss.shoot_frequency >= boss.shoot_frequency_time:
                            boss.normal_shoot(bullet_enemy_img)
                            bullet_sound.play()
                            boss.shoot_frequency = 0
                            boss.bullet -= 1
                            boss.shoot_flag = 1
                        else:
                            boss.shoot_frequency += 1                        
                    if boss.mode == 1:
                        if boss.shoot_frequency >= boss.shoot_frequency_time:
                            if abs(target) < 150:
                                boss.normal_shoot(bullet_enemy_img)
                                bullet_sound.play()
                                boss.shoot_frequency = 0
                                boss.bullet -= 1
                                boss.shoot_flag = 1
                        else:
                            boss.shoot_frequency += 1
                            
                    if boss.mode == 0:
                        if boss.shoot_frequency >= 50:
                            if abs(target) < 200:
                                boss.normal_shoot(bullet_enemy_img)
                                bullet_sound.play()
                                boss.shoot_frequency = 0
                                boss.bullet -= 1
                                boss.shoot_flag = 1 # 绘制攻击的boss
                        else:
                            boss.shoot_frequency += 1     
                            
                if boss.bullet < boss.bullet_max:
                    if boss.recharging == 0:
                        boss.bullet += 1
                        boss.recharging = boss.recharge_time
                    else:
                        boss.recharging -= 1
                        
            else:
                if flag_dialog == 0:
                    boss.show()
                if boss.rect.top > 1 and flag_dialog == 0 and not flag_firstDialog:
                    flag_dialog = 1
                                                           
            screen.blit(boss.image, boss.rect)        
            
            if pygame.sprite.collide_rect(boss, player):
                if player.is_hit is not True:
                    player.is_hit = True
                    game_over_sound.play()
                    boss.life -= boss.bomb_damage
                else:
                    pass
            #发现没有合适的函数，要去看文档！！
            if pygame.sprite.spritecollideany(boss, player.bullets):
                if boss.flag_showup == 1:
                    boss.life -= 1
                    boss.ishit_flag = 1
                player.bullets.remove(bullet) #要注意一旦击中就要删除子弹，不然下次循环还会把这颗子弹算上去
                #注意一开始player和boss的子弹都是bullet，然后就有问题了，remove不掉了，后来把boss的子弹名字改成enemy_bullet就OK了
            if boss.life <= 0:
                for enemy1 in enemies:
                    enemies1_down.add(enemy1)
                    enemies1.remove(enemy1)
                boss_flag = 0
                boss_down_flag = 1
                player.score += 2000
                boss_down_sound.play() 
                
        if boss_summon_flag == 1:
            if boss_summon.flag_showup == 1:
                boss_summon.move((player.rect.left + player.rect.right) / 2 - (boss_summon.rect.left + boss_summon.rect.right) / 2)
                if boss_summon.bullet > 0:
                    if boss_summon.shoot_frequency == 15:
                        boss_summon.normal_shoot(bullet_enemy_img)
                        bullet_sound.play()
                        boss_summon.shoot_frequency = 0
                        boss_summon.bullet -= 1
                    else:
                        boss_summon.shoot_frequency += 1
                    boss_summon.index = boss_summon.shoot_frequency // 8 + 1
                    screen.blit(boss_summon.images[boss_summon.index], boss_summon.rect)
                else:
                    if boss_summon.recharge == 0:
                        boss_summon.bullet = boss_summon.bullet_max;
                        boss_summon.recharge = 200
                    else:
                        boss_summon.recharge -= 1
                    screen.blit(boss_summon.images[0], boss_summon.rect)
            else:
                boss_summon.show()
                if boss_summon.flag_sound == 0:
                    boss_show_sound.play()
                    boss_summon.flag_sound = 1
                screen.blit(boss_summon.images[0], boss_summon.rect)                    
                
            # summon 和玩家相撞
            if pygame.sprite.collide_rect(boss_summon, player):
                if player.is_hit is not True:
                    player.is_hit = True
                    game_over_sound.play()
                    boss_summon.life -= boss_summon.bomb_damage
                else:
                    pass
                    
            if pygame.sprite.spritecollideany(boss_summon, player.bullets):
                if boss_summon.flag_showup == 1:
                    boss_summon.life -= 1
                    boss_summon.ishit_flag = 1
                player.bullets.remove(bullet)
            if boss_summon.life <= 0 or boss.life <= 0:
                boss_summon_flag = 0
                boss_summon_down_flag = 1
                player.score += 300
                boss_down_sound.play()      
                
        if boss_once_flag == 1:
            if pygame.sprite.spritecollideany(player, boss.enemy_bullets) :
                if (enemy_bullet.rect.centery - player.rect.centery) < -35:
                    if abs(enemy_bullet.rect.centerx - player.rect.centerx) < 20:
                        boss.enemy_bullets.remove(enemy_bullet)
                        player.is_hit = True
                        game_over_sound.play() 
                    else:
                        pass
                        
                elif (enemy_bullet.rect.centery - player.rect.centery)  > 40:                    
                    pass
                else:
                    boss.enemy_bullets.remove(enemy_bullet)
                    player.is_hit = True
                    game_over_sound.play()
                    
            boss.enemy_bullets.draw(screen)   
            
        if boss_summon_once_flag == 1:
            if pygame.sprite.spritecollideany(player, boss_summon.enemy_bullets) :
                if (enemy_bullet.rect.centery - player.rect.centery) < -35:
                    if abs(enemy_bullet.rect.centerx - player.rect.centerx) < 20:
                        boss_summon.enemy_bullets.remove(enemy_bullet)
                        player.is_hit = True
                        game_over_sound.play() 
                    else:
                        pass
                        
                elif (enemy_bullet.rect.centery - player.rect.centery)  > 40:                    
                    pass
                else:
                    boss_summon.enemy_bullets.remove(enemy_bullet)
                    player.is_hit = True
                    game_over_sound.play()
                    
            boss_summon.enemy_bullets.draw(screen)     
            
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
        if boss_summon_once_flag == 1:
            for enemy_bullet in boss_summon.enemy_bullets:
                enemy_bullet.move()
                if enemy_bullet.rect.bottom > SCREEN_HEIGHT:
                    boss_summon.enemy_bullets.remove(enemy_bullet)   
        if enemy2_once_flag == 1:
            for enemy_bullet in enemy2.enemy_bullets:
                enemy_bullet.move()
                if enemy_bullet.rect.bottom > SCREEN_HEIGHT:
                    enemy2.enemy_bullets.remove(enemy_bullet)   
                    
        # 移动敌机，若超出窗口范围则删除
        for enemy1 in enemies1:
            enemy1.move((player.rect.left + player.rect.right) / 2 - (enemy1.rect.left + enemy1.rect.right) / 2)
            # 判断玩家是否被击中
            if pygame.sprite.collide_rect(enemy1, player) and not player.is_hit:
                if (enemy1.rect.centery - player.rect.centery) < -35:
                    if abs(enemy1.rect.centerx - player.rect.centerx) < 30:
                        enemies1_down.add(enemy1)
                        enemies1.remove(enemy1)
                        player.is_hit = True
                        game_over_sound.play() 
                        break
                    else:
                        pass
                        
                elif (enemy1.rect.centery - player.rect.centery) > 50:                    
                    pass
                else:
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
            # 判断玩家是否被击中, 如果已经击中就不用重复判断了
            if pygame.sprite.collide_rect(enemy2, player) and not player.is_hit:
                if (enemy2.rect.centery - player.rect.centery) < -50:
                    if abs(enemy2.rect.centerx - player.rect.centerx) < 35:
                        enemies2_down.add(enemy2)
                        enemies2.remove(enemy2)
                        player.is_hit = True
                        game_over_sound.play() 
                        break
                    else:
                        pass
                        
                elif (enemy2.rect.centery - player.rect.centery) > 70:                    
                    pass
                else:
                    enemies2_down.add(enemy2)
                    enemies2.remove(enemy2)
                    player.is_hit = True
                    game_over_sound.play() 
                    break
                    
            if enemy2.rect.top > SCREEN_HEIGHT:
                enemies2.remove(enemy2)   

        if enemy2_once_flag == 1:
            if pygame.sprite.spritecollideany(player, enemy2.enemy_bullets) :
                if (enemy_bullet.rect.centery - player.rect.centery) < -35:
                    if abs(enemy_bullet.rect.centerx - player.rect.centerx) < 20:
                        enemy2.enemy_bullets.remove(enemy_bullet)
                        player.is_hit = True
                        game_over_sound.play() 
                    else:
                        pass
                        
                elif (enemy_bullet.rect.centery - player.rect.centery)  > 40:                    
                    pass
                else:
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
            screen.blit(boss.down_imgs[boss.down_index // 5], boss.rect)
            boss.down_index += 1
            if boss.down_index == 19:
                boss_down_flag = 0
                flag_betweenLevel = 1  # 表示boss已经结束了
                flag_dialog = 1
                myGame = 1
                myScore = player.score
                
        if boss_summon_down_flag == 1:
            img_index = boss_summon.down_index // 10
            screen.blit(boss_summon.down_images[img_index], boss_summon.rect)
            boss_summon.down_index += 1
            if boss_summon.down_index == 59:
                boss_summon_down_flag = 0

        # 生成奖励
        if flag_dialog != 1 and flag_dialog != 2:
            if award_frequency == award_time and flag_betweenLevel == 0:
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
                min_time = 600 - int(player.score / 25)
                if min_time < 350:
                    min_time = 350
                max_time = 900 - int(player.score / 20)
                if max_time < 500:
                    max_time = 500
                award_time = random.randint(min_time, max_time)
            else:
                award_frequency += 1
            
        for award in awards:
            award.move()
                #是否获得奖励
            if pygame.sprite.collide_rect(player, award):
                if award.kind == 1:
                    player.NL_bullet_time = 400
                    get_bullet_sound.play()
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
                myGame = 0
                myScore = player.score
                return boss_flag
                
        # 绘制子弹和和奖励和敌机
        player.bullets.draw(screen)
        awards.draw(screen)
        enemies1.draw(screen)
            
        # 绘制得分
        # score_font = pygame.font.Font('freesansbold.ttf', 32)  # 字体大小的
        score_text = score_font.render(str(player.score), True, (128, 128, 128))   # RGB三个通道，表示颜色是灰色
        text_rect = score_text.get_rect()
        text_rect.topleft = [10, 5]
        screen.blit(score_text, text_rect)
        # 绘制boss血量
        if boss_flag == 1 and boss_down_flag == 0:
            # boss_life_font = pygame.font.Font('freesansbold.ttf', 22)
            strbosslife = ''
            for i in range(0, boss.life):
                strbosslife += '[]'
            boss_life_text = boss_life_font.render('Boss level5: ' + strbosslife, True, (128, 128, 128))
            boss_life_rect = boss_life_text.get_rect()
            boss_life_rect.topleft = [30, SCREEN_HEIGHT - 40]
            screen.blit(boss_life_text, boss_life_rect)
                
        # 绘制子弹数目和bomb数目
        # bullet_font = pygame.font.Font('freesansbold.ttf', 20)
        if player.NL_bullet_time > 0:
            bullet_text = bullet_font.render('Bullet: ', True, (128, 128, 128))
            position = SCREEN_WIDTH - 65
            for i in range(0, 5):
                screen.blit(bullet_img, ((position + i * 12), 10))
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
        # bomb_font = pygame.font.Font('freesansbold.ttf', 20)
        bomb_text = bomb_font.render('Bomb x ' + str(player.bomb), True, (128, 128, 128))
        bombText_rect = bomb_text.get_rect()
        bombText_rect.topleft = [SCREEN_WIDTH - 130, 35]
        screen.blit(bomb_text, bombText_rect)
        # screen.blit(timeout_img, (SCREEN_WIDTH - 100, 60))
        # 监听键盘事件
        key_pressed = pygame.key.get_pressed()
        # 若玩家被击中，则无效
        if not player.is_hit:
            if key_pressed[K_SPACE]:
                if flag_dialog == 0:
                    if player.shoot_frequency % 15 == 0 and (player.bullet > 0 or player.NL_bullet_time > 0):
                        bullet_sound.play()
                        player.shoot(bullet_img)
                        player.shoot_frequency = 0
                        player.bullet -= 1
                else:
                    if dialog_index % 10 == 0:
                        x += 1
                        dialog_index = 0
                
                    #使用炸弹
            if key_pressed[K_b]:
                if flag_dialog != 1:
                    if player.bomb_frequency % 15 == 0 and player.bomb > 0:
                        bomb_sound.play()
                        player.bomb -= 1
                        player.bomb_frequency = 0
                        if boss_flag == 1 and boss.flag_showup == 1:
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
                        if boss_summon_once_flag == 1:
                            for enemy_bullet in boss_summon.enemy_bullets:
                                boss_summon.enemy_bullets.remove(enemy_bullet)
                        if boss_summon_flag == 1 and boss_summon.flag_showup == 1:
                            boss_summon.life -= boss_summon.bomb_damage
                            
                else:
                    if flag_betweenLevel == 0:
                        x = 16
                    else:
                        x = 27
                    player.bomb_frequency = 1
					
            if key_pressed[K_w] or key_pressed[K_UP]:
                player.moveUp()
            if key_pressed[K_s] or key_pressed[K_DOWN]:
                player.moveDown()
            if key_pressed[K_a] or key_pressed[K_LEFT]:
                player.moveLeft()
            if key_pressed[K_d] or key_pressed[K_RIGHT]:
                player.moveRight()
                
         # 按t来暂停
            if timeout_frequency < 20:
                timeout_frequency += 1
            if key_pressed[K_t] and timeout_frequency == 20:
                flag_timeout = True
                timeout_frequency = 0
                while(1): 
                    clock.tick(60)
                    timeout_rect = timeout_text.get_rect()
                    timeout_rect.centerx = screen.get_rect().centerx
                    timeout_rect.centery = screen.get_rect().centery
                    screen.blit(timeout_text, timeout_rect)
                    pygame.display.update()
                    if timeout_frequency < 20:
                        timeout_frequency += 1
                    if not flag_timeout:
                        timeout_frequency = 0
                        break
                    key_pressed = pygame.key.get_pressed()
                    if key_pressed[K_t] and timeout_frequency == 20:
                        flag_timeout = False
                        timeout_frequency = 0
                    for timeout_event in pygame.event.get():
                        if timeout_event.type == pygame.QUIT:
                            pygame.quit()
                            exit()   
            
        if player.shoot_frequency < 15:  # 现在飞机射子弹的频率下来了
            player.shoot_frequency += 1
        if player.bomb_frequency < 15:
            player.bomb_frequency += 1
        
        if dialog_index < 10:
            dialog_index += 1
            #recharge the bullets
        if player.recharging < player.recharge_time and player.bullet < player.bullet_max:
            player.recharging += 1
            if player.recharging == player.recharge_time:
                player.bullet += 1
                player.recharging = 0
        player.NL_bullet_time -= 1
        if player.NL_bullet_time == 0:
            player.bullet = player.bullet_max
            get_bullet_sound.play()  # 效果失效时提醒一下
            
        # 更新屏幕
        pygame.display.update()
        myTime += 1
        
        if timeout_frequency < 20:
            timeout_frequency += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()    
 
# 结束时的画面 
def over():
    clock = pygame.time.Clock()
    myX = [-3, 3, -3, 3]
    myY = [3, 3, -3, -3]
    myIndex1 = myIndex2 = myIndex3 = 0
    flag1 = flag2 = flag3 = 0
    running = 1
    myYesCenterx = screen.get_rect().centerx 
    myYesCentery = screen.get_rect().centery + 170
    myNoCenterx = screen.get_rect().centerx
    myNoCentery = screen.get_rect().centery + 220
    myBackCenterx = screen.get_rect().centerx
    myBackCentery = screen.get_rect().centery + 300
    global myScore
    save_game() # 每次到这儿就保存一下进度
    
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
        backText = choicefont.render('Back to the main menu', True, (0, 0, 0))
        YesText_rect = YesText.get_rect()
        NoText_rect = NoText.get_rect()
        backText_rect = backText.get_rect()
        
        YesText_rect.centerx = myYesCenterx
        YesText_rect.centery = myYesCentery
        NoText_rect.centerx = myNoCenterx
        NoText_rect.centery = myNoCentery
        backText_rect.centerx = myBackCenterx
        backText_rect.centery = myBackCentery
        
        screen.blit(scoreText, scoreText_rect)
        if flag1 == 0:
            screen.blit(YesText, YesText_rect)
        if flag2 == 0:
            screen.blit(NoText, NoText_rect)
        if flag3 == 0:
            screen.blit(backText, backText_rect)
            
        showlist = list(pygame.mouse.get_pos())
        #对于yes的回答
        if  showlist[0] > 150 and showlist[0] < 650 and showlist[1] > 500 and showlist[1] < 540:
            myIndex1 += 1
            flag1 = 1
            flag2 = 0
            flag3 = 0
            if myIndex1 // 5 >= 1 and myIndex1 % 5 == 0:
                YesText_rect.centerx = myYesCenterx + myX[myIndex1 // 5 - 1]
                YesText_rect.centery = myYesCentery + myY[myIndex1 // 5 - 1]
            if myIndex1 > 23:
                myIndex1 = 0
            screen.blit(YesText, YesText_rect)    
            
            #对于no的回答
        elif  showlist[0] > 30 and showlist[0] < 770 and showlist[1] > 550 and showlist[1] < 590:
            myIndex2 += 1
            flag2 = 1
            flag1 = 0
            flag3 = 0
            if myIndex2 // 5 >= 1 and myIndex2 % 5 == 0:
                NoText_rect.centerx = myNoCenterx + myX[myIndex2 // 5 - 1]
                NoText_rect.centery = myNoCentery + myY[myIndex2 // 5 - 1]
            if myIndex2 > 23:
                myIndex2 = 0
            screen.blit(NoText, NoText_rect)    
 
        elif  showlist[0] > 240 and showlist[0] < 565 and showlist[1] > 635 and showlist[1] < 670:
            myIndex3 += 1
            flag3 = 1
            flag1 = 0
            flag2 = 0
            if myIndex3 // 5 >= 1 and myIndex3 % 5 == 0:
                backText_rect.centerx = myBackCenterx + myX[myIndex3 // 5 - 1]
                backText_rect.centery = myBackCentery + myY[myIndex3 // 5 - 1]
            if myIndex3 > 23:
                myIndex3 = 0
            screen.blit(backText, backText_rect)    
            
        else:
            flag1 = 0
            flag2 = 0
            flag3 = 0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                poslist = list(pygame.mouse.get_pos())
                # print pygame.mouse.get_pos()  # 用于测试选择项的两个端点的坐标的
                if poslist[0] > 150 and poslist[0] < 650 and poslist[1] > 500 and poslist[1] < 540:
                    return 'continue'
                if poslist[0] > 30 and poslist[0] < 770 and poslist[1] > 550 and poslist[1] < 590:
                    pygame.quit()
                    exit()
                if poslist[0] > 240 and poslist[0] < 565 and poslist[1] > 635 and poslist[1] < 670:
                    return 'back'
        pygame.display.update()
 
# 开始画面 
def opening():   
    running = 1
    clock = pygame.time.Clock()
    error = 4
    myX = [-error, error, -error, error]
    myY = [error, error, -error, -error]
    welcomeDirection = 1
    myWelcomeCenterx = screen.get_rect().centerx
    myBeginIndex = 0
    myBeginCenterx = screen.get_rect().centerx
    myBeginCentery = screen.get_rect().centery - 150
    myLoadIndex = 0
    myLoadCenterx = screen.get_rect().centerx
    myLoadCentery = screen.get_rect().centery - 50
    myChallengingIndex = 0
    myChallengingCenterx = screen.get_rect().centerx
    myChallengingCentery = screen.get_rect().centery + 50
    myRulesIndex = 0
    myRulesCenterx = screen.get_rect().centerx
    myRulesCentery = screen.get_rect().centery + 150
    myExitIndex = 0
    myExitCenterx = screen.get_rect().centerx
    myExitCentery = screen.get_rect().centery + 250    
    flag_begin = 0
    flag_load = 0
    flag_challenging = 0
    flag_rules = 0
    flag_exit = 0
    openingFont = pygame.font.Font('freesansbold.ttf', 50)
    introFont = pygame.font.Font('freesansbold.ttf', 12)
    welcomeText = openingFont.render("Welcome to this game!", True, (0, 0, 0))
    beginText = openingFont.render('New game', True, (0, 0, 0))
    loadText = openingFont.render('Load game', True, (0, 0, 0))
    challengingText = openingFont.render('Challenging mode', True, (0, 0, 0))
    rulesText = openingFont.render('The rules', True, (0, 0, 0))
    exitText = openingFont.render('Exit', True, (0, 0, 0))
    introText = introFont.render('Please check  https://github.com/type-coder-engineer  to find more interesting projects by me ^_^', True, (0, 50, 200))
    introText_rect = introText.get_rect()
    welcomeText_rect = welcomeText.get_rect()
    beginText_rect = beginText.get_rect()
    loadText_rect = loadText.get_rect()
    challengingText_rect = challengingText.get_rect()
    rulesText_rect = rulesText.get_rect()
    exitText_rect = exitText.get_rect()
        
    while running:
        clock.tick(60)
    
        screen.fill(0)
        screen.blit(background, (0, 0))
        
        if welcomeDirection == 1:
            myWelcomeCenterx += 3
        else:
            myWelcomeCenterx -= 3
            
        if myWelcomeCenterx < 300:
            welcomeDirection = 1
        if myWelcomeCenterx > 500:
            welcomeDirection = 0
            
        welcomeText_rect.centerx =  myWelcomeCenterx
        welcomeText_rect.centery = screen.get_rect().centery - 270
        beginText_rect.centerx =  screen.get_rect().centerx
        beginText_rect.centery = screen.get_rect().centery - 150
        loadText_rect.centerx =  screen.get_rect().centerx
        loadText_rect.centery = screen.get_rect().centery - 50   
        challengingText_rect.centerx =  screen.get_rect().centerx
        challengingText_rect.centery = screen.get_rect().centery + 50            
        rulesText_rect.centerx =  screen.get_rect().centerx
        rulesText_rect.centery = screen.get_rect().centery + 150
        exitText_rect.centerx =  screen.get_rect().centerx
        exitText_rect.centery = screen.get_rect().centery + 250
        introText_rect.centerx = screen.get_rect().centerx
        introText_rect.centery = screen.get_rect().centery + 315
        screen.blit(welcomeText, welcomeText_rect)
        screen.blit(introText, introText_rect)
        if flag_begin == 0:
            screen.blit(beginText, beginText_rect)
        if flag_load == 0:
            screen.blit(loadText, loadText_rect)
        if flag_challenging == 0:
            screen.blit(challengingText, challengingText_rect)            
        if flag_rules == 0:
            screen.blit(rulesText, rulesText_rect)
        if flag_exit == 0:
            screen.blit(exitText, exitText_rect)
            
        showlist = list(pygame.mouse.get_pos())
        if showlist[0] > 275 and showlist[0] < 525 and showlist[1] > 175 and showlist[1] < 225:
            myBeginIndex += 1
            flag_begin = 1
            if myBeginIndex // 7 >= 1 and myBeginIndex % 7 == 0:
                beginText_rect.centerx = myBeginCenterx + myX[myBeginIndex // 7 - 1]
                beginText_rect.centery = myBeginCentery + myY[myBeginIndex // 7 - 1]

            if myBeginIndex > 33:
                myBeginIndex = 1
            screen.blit(beginText, beginText_rect)
            flag_load = 0
            flag_challenging = 0
            flag_rules = 0
            flag_exit = 0
            
            # pygame.display.update()    
        elif showlist[0] > 265 and showlist[0] < 535 and showlist[1] > 275 and showlist[1] < 325:
            myLoadIndex += 1
            flag_load = 1
            if myLoadIndex // 7 >= 1 and myLoadIndex % 7 == 0:
                loadText_rect.centerx = myLoadCenterx + myX[myLoadIndex // 7 - 1]
                loadText_rect.centery = myLoadCentery + myY[myLoadIndex // 7 - 1]

            if myLoadIndex > 33:
                myLoadIndex = 1
            screen.blit(loadText, loadText_rect)   
            flag_begin = 0
            flag_rules = 0
            flag_challenging = 0
            flag_exit = 0

        elif showlist[0] > 180 and showlist[0] < 620 and showlist[1] > 375 and showlist[1] < 425:
            myChallengingIndex += 1
            flag_challenging = 1
            if myChallengingIndex // 7 >= 1 and myChallengingIndex % 7 == 0:
                challengingText_rect.centerx = myChallengingCenterx + myX[myChallengingIndex // 7 - 1]
                challengingText_rect.centery = myChallengingCentery + myY[myChallengingIndex // 7 - 1]

            if myChallengingIndex > 33:
                myChallengingIndex = 1
            screen.blit(challengingText, challengingText_rect)   
            flag_begin = 0
            flag_rules = 0
            flag_load = 0
            flag_exit = 0

        elif showlist[0] > 280 and showlist[0] < 515 and showlist[1] > 475 and showlist[1] < 525:
            myRulesIndex += 1
            flag_rules = 1
            if myRulesIndex // 7 >= 1 and myRulesIndex % 7 == 0:
                rulesText_rect.centerx = myRulesCenterx + myX[myRulesIndex // 7 - 1]
                rulesText_rect.centery = myRulesCentery + myY[myRulesIndex // 7 - 1]

            if myRulesIndex > 33:
                myRulesIndex = 1
            screen.blit(rulesText, rulesText_rect)   
            flag_begin = 0
            flag_challenging = 0
            flag_load = 0
            flag_exit = 0
            
        elif showlist[0] > 355 and showlist[0] < 450 and showlist[1] > 575 and showlist[1] < 625:
            myExitIndex += 1
            flag_exit = 1
            if myExitIndex // 7 >= 1 and myExitIndex % 7 == 0:
                exitText_rect.centerx = myExitCenterx + myX[myExitIndex // 7 - 1]
                exitText_rect.centery = myExitCentery + myY[myExitIndex // 7 - 1]

            if myExitIndex > 33:
                myExitIndex = 1
            screen.blit(exitText, exitText_rect)   
            flag_begin = 0
            flag_challenging = 0
            flag_load = 0
            flag_rules = 0
            
        else:
            flag_begin = 0
            flag_challenging = 0
            flag_load = 0
            flag_rules = 0
            flag_exit = 0
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                poslist = list(pygame.mouse.get_pos())
                # print pygame.mouse.get_pos()  # 用于测试选择项的两个端点的坐标的
                if poslist[0] > 275 and poslist[0] < 525 and poslist[1] > 175 and poslist[1] < 225:
                    return 'newgame'
                elif poslist[0] > 265 and poslist[0] < 535 and poslist[1] > 275 and poslist[1] < 325:
                    return 'loadgame'
                elif poslist[0] > 180 and poslist[0] < 620 and poslist[1] > 375 and poslist[1] < 425:
                    return 'challengingmode'
                elif poslist[0] > 280 and poslist[0] < 515 and poslist[1] > 475 and poslist[1] < 525:
                    return 'rules'
                elif poslist[0] > 355 and poslist[0] < 450 and poslist[1] > 575 and poslist[1] < 625:
                    pygame.quit()
                    exit()       
                    
        pygame.display.update()

# 规则界面
def rules():
    running = 1
    clock = pygame.time.Clock()
    error = 4
    myX = [-error, error, -error, error]
    myY = [error, error, -error, -error]
    myIndex = 0
    myCenterx = screen.get_rect().centerx
    myCentery = screen.get_rect().centery + 250  # back按钮原来的位置
    flag = 0
    
    while running:
        clock.tick(60)
    
        screen.fill(0)
        screen.blit(background, (0, 0))
        titleFont = pygame.font.Font('freesansbold.ttf', 30)
        introFont = pygame.font.Font('freesansbold.ttf', 14)
        titleText = titleFont.render('The rules of the game', True, (0, 0, 0))
        backText = titleFont.render('Back to the menu', True, (0, 0, 0))
        
        introText1 = introFont.render('You can use direction keys to move your plane, use space to shoot. There is a recharging time for the bullets.', True, (0, 0, 0))
        introText2 = introFont.render('Be careful not to get too close to any enemy, you will risk of being crashed by the airflow between the planes.', True, (0, 0, 0))
        introText3 = introFont.render('There are two kinds of award. If you get the bullet award, you can have unlimited bullets for a while. ', True, (0, 0, 0))
        introText4 = introFont.render('If you get the bomb award you can tap \'b\' to use it. You can only carry at most 3 bombs at one time. A bomb', True, (0, 0, 0))
        introText5 = introFont.render('can erase all the enemies and their bullets on the screen. It can also make a certain damage to every boss.', True, (0, 0, 0))       
        introText6 = introFont.render('For the boss You can see its life on the bottom left. Pay attention a boss will have some special attacks! ', True, (0, 0, 0))
        introText7 = introFont.render('And remember every boss has its own pattern, well that\'s for me to know and for you to find out~ LOL ', True, (0, 0, 0))
        introText8 = introFont.render('If you achieve a higher level after the level1, you will be able to reload the game to this level if you are dead.', True, (0, 0, 0)) 
        introText9 = introFont.render('And in the challenging mode, you can enjoy the classic mode of shooting planes game without the boss.', True, (0, 0, 0)) 
        introText10 = introFont.render('You can use key \'t\' to pause the game and take a break, and use \'t\' again to get back', True, (0, 0, 0))
        introText11 = introFont.render('Nothing else to say, I hope you have fun playing this game and I wish you good luck!', True, (0, 0, 0))
        
        introText1_rect = introText1.get_rect()
        introText2_rect = introText2.get_rect()
        introText3_rect = introText3.get_rect()
        introText4_rect = introText4.get_rect()
        introText5_rect = introText5.get_rect()
        introText6_rect = introText6.get_rect()
        introText7_rect = introText7.get_rect()
        introText8_rect = introText8.get_rect()
        introText9_rect = introText9.get_rect()
        introText10_rect = introText10.get_rect()
        introText11_rect = introText10.get_rect()
        titleText_rect = titleText.get_rect()
        backText_rect = backText.get_rect()
        
        titleText_rect.centerx =  screen.get_rect().centerx
        titleText_rect.centery = screen.get_rect().centery - 300
        backText_rect.centerx =  screen.get_rect().centerx
        backText_rect.centery = screen.get_rect().centery + 250
        
        introText1_rect.centerx = screen.get_rect().centerx
        introText1_rect.centery = screen.get_rect().centery - 240
        introText2_rect.centerx = screen.get_rect().centerx
        introText2_rect.centery = screen.get_rect().centery - 200
        introText3_rect.centerx = screen.get_rect().centerx
        introText3_rect.centery = screen.get_rect().centery - 160
        introText4_rect.centerx = screen.get_rect().centerx
        introText4_rect.centery = screen.get_rect().centery - 120
        introText5_rect.centerx = screen.get_rect().centerx
        introText5_rect.centery = screen.get_rect().centery - 80
        introText6_rect.centerx = screen.get_rect().centerx
        introText6_rect.centery = screen.get_rect().centery - 40
        introText7_rect.centerx = screen.get_rect().centerx
        introText7_rect.centery = screen.get_rect().centery 
        introText8_rect.centerx = screen.get_rect().centerx
        introText8_rect.centery = screen.get_rect().centery + 40        
        introText9_rect.centerx = screen.get_rect().centerx
        introText9_rect.centery = screen.get_rect().centery + 80  
        introText10_rect.centerx = screen.get_rect().centerx
        introText10_rect.centery = screen.get_rect().centery + 120           
        introText11_rect.centerx = screen.get_rect().centerx
        introText11_rect.centery = screen.get_rect().centery + 160             
        screen.blit(titleText, titleText_rect)
        screen.blit(introText1, introText1_rect)
        screen.blit(introText2, introText2_rect)
        screen.blit(introText3, introText3_rect)
        screen.blit(introText4, introText4_rect)
        screen.blit(introText5, introText5_rect)
        screen.blit(introText6, introText6_rect)
        screen.blit(introText7, introText7_rect)       
        screen.blit(introText8, introText8_rect)
        screen.blit(introText9, introText9_rect)       
        screen.blit(introText10, introText10_rect) 
        screen.blit(introText11, introText11_rect) 
        
        if flag == 0:
            screen.blit(backText, backText_rect)
        
        showlist = list(pygame.mouse.get_pos())
        if showlist[0] > 270 and showlist[0] < 530 and showlist[1] > 580 and showlist[1] < 620:
            myIndex += 1
            flag = 1
            if myIndex // 7 >= 1 and myIndex % 7 == 0:
                backText_rect.centerx = myCenterx + myX[myIndex // 7 - 1]
                backText_rect.centery = myCentery + myY[myIndex // 7 - 1]
                
            if myIndex > 33:
                myIndex = 0
            screen.blit(backText, backText_rect)

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
                if poslist[0] > 270 and poslist[0] < 530 and poslist[1] > 580 and poslist[1] < 620:
                    running = 0
        pygame.display.update()    

# 新游戏        
def newgame_main(): 
    player = Player(player_img, player_down_img, player_pos)
    clock = pygame.time.Clock()
    onelife = 1
    global myGame 
    
    again = 0 # 为了重玩的时候重新刷新player的参数，如果是直接进如下一关就不用刷新位置弹药信息了
    flag_saw_boss = 0
    flag_saw_boss = level1(clock, player, flag_saw_boss, again)
    while (myGame != 1):
        again = 1
        onelife = 0
        choice = over()
        if choice == 'back':
            return
        else:
            flag_saw_boss = level1(clock, player, flag_saw_boss, again)
            
    if myGame == 1:
        again = 0
        flag_saw_boss = 0
        flag_saw_boss = level2(clock, player, flag_saw_boss, again)
        while (myGame != 1):
            again = 1
            choice = over()
            if choice == 'back':
                return
            else:
                flag_saw_boss = level2(clock, player, flag_saw_boss, again)
                
    if myGame == 1:
        again = 0
        flag_saw_boss = 0
        flag_saw_boss = level3(clock, player, flag_saw_boss, again)
        while (myGame != 1):
            again = 1
            onelife = 0
            choice = over()
            if choice == 'back':
                return
            else:
                flag_saw_boss = level3(clock, player, flag_saw_boss, again)
                
    if myGame == 1:
        again = 0
        flag_saw_boss = 0
        flag_saw_boss = level4(clock, player, flag_saw_boss, again)
        while (myGame != 1):
            again = 1
            onelife = 0
            choice = over()
            if choice == 'back':
                return
            else:
                flag_saw_boss = level4(clock, player, flag_saw_boss, again)
                
    if myGame == 1:
        again = 0
        flag_saw_boss = 0
        flag_saw_boss = level5(clock, player, flag_saw_boss, again)
        while (myGame != 1):
            again = 1
            onelife = 0
            choice = over()
            if choice == 'back':
                return
            else:
                flag_saw_boss = level5(clock, player, flag_saw_boss, again)                 
        
        if onelife == 1:
            congraduation_onelife()
        elif myGame == 1:
            congraduation()
            
# 选择加载游戏界面                     
def loadGame():
    running = 1
    clock = pygame.time.Clock()
    error = 4
    myX = [-error, error, -error, error]
    myY = [error, error, -error, -error]
    mylevel2Index = 0
    mylevel2Centerx = screen.get_rect().centerx
    mylevel2Centery = screen.get_rect().centery - 150
    mylevel3Index = 0
    mylevel3Centerx = screen.get_rect().centerx
    mylevel3Centery = screen.get_rect().centery - 50
    mylevel4Index = 0
    mylevel4Centerx = screen.get_rect().centerx
    mylevel4Centery = screen.get_rect().centery + 50
    mylevel5Index = 0
    mylevel5Centerx = screen.get_rect().centerx
    mylevel5Centery = screen.get_rect().centery + 150
    mybackIndex = 0
    mybackCenterx = screen.get_rect().centerx
    mybackCentery = screen.get_rect().centery + 200  # back按钮原来的位置
    flag_level2 = 0
    flag_level3 = 0
    flag_level4 = 0
    flag_level5 = 0
    flag_back = 0
    global pass_level

    while running:
        clock.tick(60)
    
        screen.fill(0)
        screen.blit(background, (0, 0))
        openingFont = pygame.font.Font('freesansbold.ttf', 50)
        titleFont = pygame.font.Font('freesansbold.ttf', 30)
        
        backText = titleFont.render('Back to the menu', True, (0, 0, 0))
        if pass_level < 2:
            level2Text = openingFont.render('LEVEL2', True, (150, 150, 150))
        else:
            level2Text = openingFont.render('LEVEL2', True, (0, 0, 0))
            
        if pass_level < 3:
            level3Text = openingFont.render('LEVEL3', True, (150, 150, 150))
        else:
            level3Text = openingFont.render('LEVEL3', True, (0, 0, 0))
            
        if pass_level < 4:
            level4Text = openingFont.render('LEVEL4', True, (150, 150, 150))
        else:
            level4Text = openingFont.render('LEVEL4', True, (0, 0, 0))
            
        if pass_level < 5:
            level5Text = openingFont.render('LEVEL5', True, (150, 150, 150))
        else:
            level5Text = openingFont.render('LEVEL5', True, (0, 0, 0))

        level2Text_rect = level2Text.get_rect()
        level3Text_rect = level3Text.get_rect()
        level4Text_rect = level4Text.get_rect()
        level5Text_rect = level5Text.get_rect()
        backText_rect = backText.get_rect()

        level2Text_rect.centerx =  screen.get_rect().centerx
        level2Text_rect.centery = screen.get_rect().centery - 150
        level3Text_rect.centerx =  screen.get_rect().centerx
        level3Text_rect.centery = screen.get_rect().centery - 50   
        level4Text_rect.centerx =  screen.get_rect().centerx
        level4Text_rect.centery = screen.get_rect().centery + 50            
        level5Text_rect.centerx =  screen.get_rect().centerx
        level5Text_rect.centery = screen.get_rect().centery + 150
        backText_rect.centerx =  screen.get_rect().centerx
        backText_rect.centery = screen.get_rect().centery + 200
        
        if flag_level2 == 0:
            screen.blit(level2Text, level2Text_rect)
        if flag_level3 == 0:
            screen.blit(level3Text, level3Text_rect)
        if flag_level4 == 0:
            screen.blit(level4Text, level4Text_rect)            
        if flag_level5 == 0:
            screen.blit(level5Text, level5Text_rect)
        if flag_back == 0:
            screen.blit(backText, backText_rect)
            
        showlist = list(pygame.mouse.get_pos())

        if showlist[0] > 275 and showlist[0] < 525 and showlist[1] > 175 and showlist[1] < 225:
            if pass_level >= 2:
                mylevel2Index += 1
                flag_level2 = 1
                if mylevel2Index // 7 >= 1 and mylevel2Index % 7 == 0:
                    level2Text_rect.centerx = mylevel2Centerx + myX[mylevel2Index // 7 - 1]
                    level2Text_rect.centery = mylevel2Centery + myY[mylevel2Index // 7 - 1]
       
                if mylevel2Index > 33:
                    mylevel2Index = 1
                screen.blit(level2Text, level2Text_rect)
                flag_level3 = 0
                flag_level4 = 0
                flag_level5 = 0
            
        elif showlist[0] > 265 and showlist[0] < 535 and showlist[1] > 275 and showlist[1] < 325:
            if pass_level >= 3:   
                mylevel3Index += 1
                flag_level3 = 1
                if mylevel3Index // 7 >= 1 and mylevel3Index % 7 == 0:
                    level3Text_rect.centerx = mylevel3Centerx + myX[mylevel3Index // 7 - 1]
                    level3Text_rect.centery = mylevel3Centery + myY[mylevel3Index // 7 - 1]
        
                if mylevel3Index > 33:
                    mylevel3Index = 1
                screen.blit(level3Text, level3Text_rect)   
                flag_level2 = 0
                flag_level4 = 0
                flag_level5 = 0
                
        elif showlist[0] > 180 and showlist[0] < 620 and showlist[1] > 375 and showlist[1] < 425:
            if pass_level >= 4:
                mylevel4Index += 1
                flag_level4 = 1
                if mylevel4Index // 7 >= 1 and mylevel4Index % 7 == 0:
                    level4Text_rect.centerx = mylevel4Centerx + myX[mylevel4Index // 7 - 1]
                    level4Text_rect.centery = mylevel4Centery + myY[mylevel4Index // 7 - 1]
    
                if mylevel4Index > 33:
                    mylevel4Index = 1
                screen.blit(level4Text, level4Text_rect)   
                flag_level2 = 0
                flag_level3 = 0
                flag_level5 = 0
                
        elif showlist[0] > 280 and showlist[0] < 515 and showlist[1] > 475 and showlist[1] < 520:
            if pass_level >= 5:
                mylevel5Index += 1
                flag_level5 = 1
                if mylevel5Index // 7 >= 1 and mylevel5Index % 7 == 0:
                    level5Text_rect.centerx = mylevel5Centerx + myX[mylevel5Index // 7 - 1]
                    level5Text_rect.centery = mylevel5Centery + myY[mylevel5Index // 7 - 1]
    
                if mylevel5Index > 33:
                    mylevel5Index = 1
                screen.blit(level5Text, level5Text_rect)   
                flag_level2 = 0
                flag_level3 = 0
                flag_level4 = 0
                
        elif showlist[0] > 270 and showlist[0] < 530 and showlist[1] > 530 and showlist[1] < 570:
            mybackIndex += 1
            flag_back = 1
            if mybackIndex // 7 >= 1 and mybackIndex % 7 == 0:
                backText_rect.centerx = mybackCenterx + myX[mybackIndex // 7 - 1]
                backText_rect.centery = mybackCentery + myY[mybackIndex // 7 - 1]
                
            if mybackIndex > 33:
                mybackIndex = 0
            screen.blit(backText, backText_rect)
            
        else:
            flag_level2 = 0
            flag_level3 = 0
            flag_level4 = 0
            flag_level5 = 0
            flag_back = 0
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                poslist = list(pygame.mouse.get_pos())
                #print pygame.mouse.get_pos()  # 用于测试选择项的两个端点的坐标的
                if poslist[0] > 275 and poslist[0] < 525 and poslist[1] > 175 and poslist[1] < 225:
                    if pass_level >= 2:
                        return 2
                                    
                elif poslist[0] > 265 and poslist[0] < 535 and poslist[1] > 275 and poslist[1] < 325:
                    if pass_level >= 3:
                        return 3
                                    
                elif poslist[0] > 180 and poslist[0] < 620 and poslist[1] > 375 and poslist[1] < 425:
                    if pass_level >= 4:
                        return 4
                            
                elif poslist[0] > 280 and poslist[0] < 515 and poslist[1] > 475 and poslist[1] < 520:
                    if pass_level >= 5:
                        return 5

                elif poslist[0] > 270 and poslist[0] < 530 and poslist[1] > 530 and poslist[1] < 570:
                        return 0
                        
        pygame.display.update()

# 加载游戏的main
def load_main(level):
    player = Player(player_img, player_down_img, player_pos)
    clock = pygame.time.Clock()
    
    if level == 2:
        again = 0 # 为了重玩的时候重新刷新player的参数，如果是直接进如下一关就不用刷新位置弹药信息了
        flag_saw_boss = 0
        flag_saw_boss = level2(clock, player, flag_saw_boss, again)
        while (myGame != 1):
            again = 1
            onelife = 0
            choice = over()
            if choice == 'back':
                return
            else:
                flag_saw_boss = level2(clock, player, flag_saw_boss, again)
                    
        if myGame == 1:
            again = 0
            flag_saw_boss = 0
            flag_saw_boss = level3(clock, player, flag_saw_boss, again)
            while (myGame != 1):
                again = 1
                onelife = 0
                choice = over()
                if choice == 'back':
                    return
                else:
                    flag_saw_boss = level3(clock, player, flag_saw_boss, again)
                    
        if myGame == 1:
            again = 0
            flag_saw_boss = 0
            flag_saw_boss = level4(clock, player, flag_saw_boss, again)
            while (myGame != 1):
                again = 1
                onelife = 0
                choice = over()
                if choice == 'back':
                    return
                else:
                    flag_saw_boss = level4(clock, player, flag_saw_boss, again)
                    
        if myGame == 1:
            again = 0
            flag_saw_boss = 0
            flag_saw_boss = level5(clock, player, flag_saw_boss, again)
            while (myGame != 1):
                again = 1
                onelife = 0
                choice = over()
                if choice == 'back':
                    return
                else:
                    flag_saw_boss = level5(clock, player, flag_saw_boss, again)    
            
            congraduation()
         
    if level == 3:
        again = 0 # 为了重玩的时候重新刷新player的参数，如果是直接进如下一关就不用刷新位置弹药信息了
        flag_saw_boss = 0
        flag_saw_boss = level3(clock, player, flag_saw_boss, again)
        while (myGame != 1):
            again = 1
            onelife = 0
            choice = over()
            if choice == 'back':
                return
            else:
                flag_saw_boss = level3(clock, player, flag_saw_boss, again)
                    
        if myGame == 1:
            again = 0
            flag_saw_boss = 0
            flag_saw_boss = level4(clock, player, flag_saw_boss, again)
            while (myGame != 1):
                again = 1
                onelife = 0
                choice = over()
                if choice == 'back':
                    return
                else:
                    flag_saw_boss = level4(clock, player, flag_saw_boss, again)
                    
        if myGame == 1:
            again = 0
            flag_saw_boss = 0
            flag_saw_boss = level5(clock, player, flag_saw_boss, again)
            while (myGame != 1):
                again = 1
                onelife = 0
                choice = over()
                if choice == 'back':
                    return
                else:
                    flag_saw_boss = level5(clock, player, flag_saw_boss, again)    
            
            congraduation()
          
    if level == 4:
        again = 0 # 为了重玩的时候重新刷新player的参数，如果是直接进如下一关就不用刷新位置弹药信息了
        flag_saw_boss = 0
        flag_saw_boss = level4(clock, player, flag_saw_boss, again)
        while (myGame != 1):
            again = 1
            onelife = 0
            choice = over()
            if choice == 'back':
                return
            else:
                flag_saw_boss = level4(clock, player, flag_saw_boss, again)
                    
        if myGame == 1:
            again = 0
            flag_saw_boss = 0
            flag_saw_boss = level5(clock, player, flag_saw_boss, again)
            while (myGame != 1):
                again = 1
                onelife = 0
                choice = over()
                if choice == 'back':
                    return
                else:
                    flag_saw_boss = level5(clock, player, flag_saw_boss, again)    
            
            congraduation()
            
    if level == 5:
        again = 0 # 为了重玩的时候重新刷新player的参数，如果是直接进如下一关就不用刷新位置弹药信息了
        flag_saw_boss = 0
        flag_saw_boss = level5(clock, player, flag_saw_boss, again)
        while (myGame != 1):
            again = 1
            onelife = 0
            choice = over()
            if choice == 'back':
                return
            else:
                flag_saw_boss = level5(clock, player, flag_saw_boss, again)
                       
        congraduation()

# 一条命过关的祝贺画面            
def congraduation_onelife():
    running = 1
    clock = pygame.time.Clock()
    error = 4
    myX = [-error, error, -error, error]
    myY = [error, error, -error, -error]
    myIndex = 0
    myCenterx = screen.get_rect().centerx
    myCentery = screen.get_rect().centery + 200  # back按钮原来的位置
    flag = 0
    
    while running:
        clock.tick(60)
    
        screen.fill(0)
        screen.blit(background, (0, 0))
        titleFont = pygame.font.Font('freesansbold.ttf', 30)
        introFont = pygame.font.Font('freesansbold.ttf', 16)
        titleText = titleFont.render('Congratulations!', True, (0, 50, 100))
        backText = titleFont.render('Back to the menu', True, (0, 0, 0))
        introText1 = introFont.render('You have passed all the five levels without a death, that\'s fantastic!', True, (0, 50, 100))
        introText2 = introFont.render('For the reward, you can add me on Wechat by "zcy-scott" and we could be friends! Isn\'t that great? ^^', True, (0, 50, 100))
        introText3 = introFont.render('Now you can play all the five levels, you can also enjoy the classic game in the challenging mode', True, (0, 50, 100))
        introText4 = introFont.render('If you like this game, please check my Github homepage to find more interesting projets by me!', True, (0, 50, 100))       
        introText5 = introFont.render('And if you have any suggestions, you are welcome to contact me by E-mail: zcy.scott@outlook.com ^^', True, (0, 50, 100))
        
        introText1_rect = introText1.get_rect()
        introText2_rect = introText2.get_rect()
        introText3_rect = introText3.get_rect()
        introText4_rect = introText4.get_rect()
        introText5_rect = introText5.get_rect()
        
        titleText_rect = titleText.get_rect()
        backText_rect = backText.get_rect()
        
        titleText_rect.centerx =  screen.get_rect().centerx
        titleText_rect.centery = screen.get_rect().centery - 250
        backText_rect.centerx =  screen.get_rect().centerx
        backText_rect.centery = screen.get_rect().centery + 200
        
        introText1_rect.centerx = screen.get_rect().centerx
        introText1_rect.centery = screen.get_rect().centery - 150
        introText2_rect.centerx = screen.get_rect().centerx
        introText2_rect.centery = screen.get_rect().centery - 100
        introText3_rect.centerx = screen.get_rect().centerx
        introText3_rect.centery = screen.get_rect().centery - 50
        introText4_rect.centerx = screen.get_rect().centerx
        introText4_rect.centery = screen.get_rect().centery 
        introText5_rect.centerx = screen.get_rect().centerx
        introText5_rect.centery = screen.get_rect().centery + 50
        
        screen.blit(titleText, titleText_rect)
        screen.blit(introText1, introText1_rect)
        screen.blit(introText2, introText2_rect)
        screen.blit(introText3, introText3_rect)
        screen.blit(introText4, introText4_rect)
        screen.blit(introText5, introText5_rect)

        if flag == 0:
            screen.blit(backText, backText_rect)
        
        showlist = list(pygame.mouse.get_pos())
        if showlist[0] > 270 and showlist[0] < 530 and showlist[1] > 530 and showlist[1] < 570:
            myIndex += 1
            flag = 1
            if myIndex // 7 >= 1 and myIndex % 7 == 0:
                backText_rect.centerx = myCenterx + myX[myIndex // 7 - 1]
                backText_rect.centery = myCentery + myY[myIndex // 7 - 1]
                
            if myIndex > 33:
                myIndex = 0
            screen.blit(backText, backText_rect)

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
                if poslist[0] > 270 and poslist[0] < 530 and poslist[1] > 530 and poslist[1] < 570:
                    running = 0
        pygame.display.update()              

# load过关画面        
def congraduation():
    running = 1
    clock = pygame.time.Clock()
    error = 4
    myX = [-error, error, -error, error]
    myY = [error, error, -error, -error]
    myIndex = 0
    myCenterx = screen.get_rect().centerx
    myCentery = screen.get_rect().centery + 200  # back按钮原来的位置
    flag = 0
    
    while running:
        clock.tick(60)
    
        screen.fill(0)
        screen.blit(background, (0, 0))
        titleFont = pygame.font.Font('freesansbold.ttf', 30)
        introFont = pygame.font.Font('freesansbold.ttf', 16)
        titleText = titleFont.render('Congratulations!', True, (0, 50, 100))
        backText = titleFont.render('Back to the menu', True, (0, 0, 0))
        introText1 = introFont.render('You have passed the final level, that\'s great!', True, (0, 50, 100))
        introText2 = introFont.render('Now you can play all the five levels, you can also enjoy the classic game in the challenging mode', True, (0, 50, 100))
        introText3 = introFont.render('Or you can try to pass all the fifth levels with one life, if succeed you will get a mysterious reward ^^', True, (0, 50, 100))
        introText4 = introFont.render('If you like this game, please check my Github homepage to find more interesting projets by me!', True, (0, 50, 100))       
        introText5 = introFont.render('And if you have any suggestions, you are welcome to contact me by E-mail: zcy.scott@outlook.com ^^', True, (0, 50, 100))
        
        introText1_rect = introText1.get_rect()
        introText2_rect = introText2.get_rect()
        introText3_rect = introText3.get_rect()
        introText4_rect = introText4.get_rect()
        introText5_rect = introText5.get_rect()
        
        titleText_rect = titleText.get_rect()
        backText_rect = backText.get_rect()
        
        titleText_rect.centerx =  screen.get_rect().centerx
        titleText_rect.centery = screen.get_rect().centery - 250
        backText_rect.centerx =  screen.get_rect().centerx
        backText_rect.centery = screen.get_rect().centery + 200
        
        introText1_rect.centerx = screen.get_rect().centerx
        introText1_rect.centery = screen.get_rect().centery - 150
        introText2_rect.centerx = screen.get_rect().centerx
        introText2_rect.centery = screen.get_rect().centery - 100
        introText3_rect.centerx = screen.get_rect().centerx
        introText3_rect.centery = screen.get_rect().centery - 50
        introText4_rect.centerx = screen.get_rect().centerx
        introText4_rect.centery = screen.get_rect().centery 
        introText5_rect.centerx = screen.get_rect().centerx
        introText5_rect.centery = screen.get_rect().centery + 50
        
        screen.blit(titleText, titleText_rect)
        screen.blit(introText1, introText1_rect)
        screen.blit(introText2, introText2_rect)
        screen.blit(introText3, introText3_rect)
        screen.blit(introText4, introText4_rect)
        screen.blit(introText5, introText5_rect)

        if flag == 0:
            screen.blit(backText, backText_rect)
        
        showlist = list(pygame.mouse.get_pos())
        if showlist[0] > 270 and showlist[0] < 530 and showlist[1] > 530 and showlist[1] < 570:
            myIndex += 1
            flag = 1
            if myIndex // 7 >= 1 and myIndex % 7 == 0:
                backText_rect.centerx = myCenterx + myX[myIndex // 7 - 1]
                backText_rect.centery = myCentery + myY[myIndex // 7 - 1]
                
            if myIndex > 33:
                myIndex = 0
            screen.blit(backText, backText_rect)

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
                if poslist[0] > 270 and poslist[0] < 530 and poslist[1] > 530 and poslist[1] < 570:
                    running = 0
        pygame.display.update()        

# 保存游戏数据到game_data        
def save_game():
    global pass_level
    target = open('game_data', 'w')
    target.write(str(pass_level))
    target.close()
    return

# 从game_data 中读取数据
def load_game():
    global pass_level
    # path = 'resources'  # 有了这个path的改变exe就没法运行了。。。不得已就把data放在外面了
    # os.chdir(path)
    if not os.path.isfile('game_data'): #如果没有数据就从1开始
        pass_level = 1
        return
    else:
        target = open('game_data', 'r')
        pass_level = int(target.readline())
        target.close()
        return
        
if __name__ == '__main__': 
    global pass_level
    load_game()
    # pass_level = 5  # for test
    
    while(1):
        choice = opening()
        if choice == "rules":
            rules()
            
        elif choice == "newgame":
            newgame_main()

        elif choice == "loadgame":
            load_choice = loadGame()
            if load_choice != 0:
                load_main(load_choice)

        elif choice == "challengingmode":
            classicMode()
            over()
        