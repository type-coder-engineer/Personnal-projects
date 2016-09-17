# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 16:36:03 2013

@author: Leo
@optimised by ZHANG Chenyu
"""

import pygame
#import wx, win32api   #本来想尝试做一个框架的，不过pygame已经自带框架了，可以留着写别的程序用
# class myFrame(wx.Frame):
    # def __init__(self, parent=None):
        # wx.Frame.__init__(self, parent, wx.ID_ANY)
    
        #set window icon
        # exeName = win32api.GetModuleFileName(win32api.GetModuleHandle(None))
        # icon = wx.Icon('Plane.ico', wx.BITMAP_TYPE_ICO)   
        # self.SetIcon(icon)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700

TYPE_SMALL = 1
TYPE_MIDDLE = 2
TYPE_BIG = 3
        
# the class bullet
class Bullet(pygame.sprite.Sprite):
    def __init__(self, bullet_img, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.rect = self.image.get_rect()  # 子弹的方块
        self.rect.midbottom = init_pos
        self.speed = 12

    def move(self):
        self.rect.top -= self.speed  # 子弹的位置不断的往前
        
 # enmey bullets
class Enemy_bullet(pygame.sprite.Sprite):
    def __init__(self, bullet_img, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.rect = self.image.get_rect()  # 子弹的方块
        self.rect.midbottom = init_pos
        self.speed = 6

    def move(self):
        self.rect.top += self.speed  # 子弹的位置不断的往前
        
# the class player
class Player(pygame.sprite.Sprite):
    def __init__(self, player_img, player_down_imgs, init_pos):
        pygame.sprite.Sprite.__init__(self)  # 一个基本的用于可见的游戏物体的类
        self.image = player_img                                 # 用来存储玩家对象精灵图片的列表
        self.rect = player_img[0].get_rect()                   # 初始化图片所在的矩形
        self.rect.topleft = init_pos                    # 初始化矩形的左上角坐标
        self.down_imgs = player_down_imgs
        self.is_hit = False                             # 玩家是否被击中
        self.speed = 8                                  # 初始化玩家速度，这里是一个确定的值
        self.bullets = pygame.sprite.Group()            # 玩家飞机所发射的子弹的集合
        self.index = 0                           # 玩家精灵图片索引
        self.down_index = 0
        self.NL_bullet_time = 0
        self.bullet_max = 5
        self.bomb_max = 3
        self.bullet = 5
        self.bomb = 0
        self.score = 0
        self.recharge_time = 60
        self.shoot_frequency = 15
        self.bomb_frequency = 15
        self.recharging = 0
        
    def shoot(self, bullet_img):
        bullet = Bullet(bullet_img, self.rect.midtop)
        self.bullets.add(bullet) # 没有这句不能显示出子弹, 因为绘制子弹用的是子弹的精灵组

    def moveUp(self):  #移动的时候如果要超出屏幕就不能动了
        if self.rect.top <= 0:
            self.rect.top = 0
        else:
            self.rect.top -= self.speed 

    def moveDown(self):
        if self.rect.top >= SCREEN_HEIGHT - self.rect.height:
            self.rect.top = SCREEN_HEIGHT - self.rect.height
        else:
            self.rect.top += self.speed

    def moveLeft(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        else:
            self.rect.left -= self.speed

    def moveRight(self):
        if self.rect.left >= SCREEN_WIDTH - self.rect.width:
            self.rect.left = SCREEN_WIDTH - self.rect.width
        else:
            self.rect.left += self.speed

class Enemy1(pygame.sprite.Sprite):
    def __init__(self, enemy_img, enemy_down_imgs, init_pos):
       pygame.sprite.Sprite.__init__(self)
       self.image = enemy_img
       self.rect = self.image.get_rect()
       self.rect.topleft = init_pos
       self.down_imgs = enemy_down_imgs
       self.speed = 3
       self.down_index = 0

    def move(self):
        self.rect.top += self.speed
        
class Enemy2(pygame.sprite.Sprite):
    def __init__(self, enemy_img, enemy_down_imgs, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.images = enemy_img
        self.rect = self.images[0].get_rect()
        self.rect.topleft = init_pos
        self.down_imgs = enemy_down_imgs
        self.speed = 3
        self.img_index = 0
        self.down_index = 0
        self.enemy_bullets = pygame.sprite.Group()
        self.recharge_time = 40
        self.shoot_frequency = self.recharge_time
        
    def move(self, target):
        if target > 3: # 这里用+-3 而不是0， 因为速度是3，如果是以0来判断的话跟踪的时候就会左右抖动
            if self.rect.right >= SCREEN_WIDTH:
                pass
            else:
                self.rect.right += self.speed                
        elif target < -3:
            if self.rect.left  <= 0:
                pass
            else:
                self.rect.left -= self.speed                          
        else:
            pass
        self.rect.top += self.speed
        
    def shoot(self, bullet_enemy_img):
        pos = list(self.rect.midbottom)
        pos[1] = pos[1] + 20
        enemy_bullet = Enemy_bullet(bullet_enemy_img, tuple(pos))
        self.enemy_bullets.add(enemy_bullet)
        
class Boss(pygame.sprite.Sprite):
    def __init__(self, boss_img, boss_down_img, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.images = []           # 用来存储玩家对象精灵图片的列表
        self.images = boss_img
        self.down_images = boss_down_img
        self.rect = self.images[0].get_rect()
        self.rect.bottomleft = init_pos
    
    def show(self):
        self.rect.bottom += self.speed - 1
        if self.rect.bottom >= 250:
            self.flag_showup = 1
            
    def normal_shoot(self, bullet_enemy_img): # 注意这里tuple不能接受下标修改，也不能直接和int相加减
        pos1 = list(self.rect.midbottom)
        pos1[0] = pos1[0] - 15
        enemy_bullet = Enemy_bullet(bullet_enemy_img, tuple(pos1))
        self.enemy_bullets.add(enemy_bullet)
        pos2 = list(self.rect.midbottom)
        pos2[0] = pos2[0] + 15
        enemy_bullet = Enemy_bullet(bullet_enemy_img, tuple(pos2))
        self.enemy_bullets.add(enemy_bullet)

class Boss_level1(Boss):
    def __init__(self, boss_img, boss_down_img, init_pos):
        Boss.__init__(self, boss_img, boss_down_img, init_pos)
        self.speed = 3
        self.life = 20
        self.bullet_max = 5
        self.bullet = self.bullet_max
        self.recharge = 200
        self.shoot_frequency = 15
        self.bomb_damage = 8
        self.index = 0
        self.down_index = 0
        self.enemy_bullets = pygame.sprite.Group()
        self.flag_showup = 0
        self.flag_sound = 0
        
    def move(self, target):
        if target > 3: # 这里用+-3 而不是0， 因为速度是3，如果是以0来判断的话跟踪的时候就会左右抖动
            if self.rect.right >= SCREEN_WIDTH:
                pass
            else:
                self.rect.right += self.speed                
        elif target < -3:
            if self.rect.left  <= 0:
                pass
            else:
                self.rect.left -= self.speed                          
        else:
            pass

class Boss_level2(Boss):
    def __init__(self, boss_img, boss_down_img, init_pos):
        Boss.__init__(self, boss_img, boss_down_img, init_pos)
        self.speed = 3
        self.life = 20
        self.bullet_max = 5
        self.bullet = self.bullet_max
        self.recharge = 200
        self.shoot_frequency = 15
        self.bomb_damage = 8
        self.index = 0
        self.down_index = 0
        self.enemy_bullets = pygame.sprite.Group()
        self.flag_showup = 0
        self.flag_sound = 0
        self.direction = 0

    def move(self):
        if self.direction == 0:
            if self.rect.left <= 0:
                self.direction = 1
            else:
                self.rect.left -= self.speed
        else:
            if self.rect.right >= SCREEN_WIDTH:
                self.direction = 0
            else:
                self.rect.right += self.speed
    
class Boss_level3(Boss_level1):
    def __init__(self, boss_img, boss_down_img, init_pos):
        Boss_level1.__init__(self, boss_img, boss_down_img, init_pos)
        self.bullet_max = 8
        self.bullet = self.bullet_max
        self.recharge_time = 60
        self.recharging = self.recharge_time
        self.bomb_damage = 6
        self.speed = 4
        self.enemy1_recharge = 400
        self.enemy1 = self.enemy1_recharge
        self.teleportation_recharge = 300
        self.teleportation = self.teleportation_recharge
        self.mode = 1 #两种模式，攻击模式是1，防守模式是0，以子弹数目为准
        self.ishit_flag = 0

    def teleportation_defence(self, position):
        if position < SCREEN_WIDTH / 2:
            self.rect.topleft = [SCREEN_WIDTH - 180, 0]
        else:
            self.rect.topleft = [5, 0]
            
    def teleportation_attack(self, position):
        selflist = list(self.rect.topleft)
        selflist[0] = position + 20
        self.rect.topleft = list(selflist) 
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.left < 0:
           self.rect.left = 0 
           
    def move(self, target, mode):
        if mode == 1:
            if target > 4: 
                if self.rect.right >= SCREEN_WIDTH:
                    pass
                else:
                    self.rect.right += self.speed                
            elif target < -4:
                if self.rect.left  <= 0:
                    pass
                else:
                    self.rect.left -= self.speed                          
            else:
                pass
        else:
            if target > 4: 
                if self.rect.left  <= 0:
                    pass
                else:
                    self.rect.left -= self.speed                     
            elif target < -4:
                if self.rect.right >= SCREEN_WIDTH:
                    pass
                else:
                    self.rect.right += self.speed                     
            else:
                pass
        
    # def normal_shoot(self, bullet_enemy_img):
        # pos1 = list(self.rect.midbottom)
        # pos1[0] = pos1[0] - 15
        # enemy_bullet = Enemy_bullet(bullet_enemy_img, tuple(pos1))
        # self.enemy_bullets.add(enemy_bullet)
        # pos2 = list(self.rect.midbottom)
        # pos2[0] = pos2[0] + 15
        # enemy_bullet = Enemy_bullet(bullet_enemy_img, tuple(pos2))
        # self.enemy_bullets.add(enemy_bullet)        
class Award(pygame.sprite.Sprite):
    def __init__(self, award_img, effective_rect, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = award_img
        self.rect = self.image.get_rect() # 注意像boss，enemy和award这种需要重复生成的用get_rect
        #来获得rect，如果用给的rect初始化会发生奇怪的事情。。。
        self.rect.bottomleft = init_pos
        self.speed = 3
        self.kind = 0
        
    def move(self):
        self.rect.top += self.speed
        
        
        
        
        
        
        
 