# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 16:36:03 2013

@author: Leo
"""

import pygame

SCREEN_WIDTH = 680
SCREEN_HEIGHT = 600

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
        
class Enemy_bullet(pygame.sprite.Sprite):
    def __init__(self, bullet_img, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.rect = self.image.get_rect()  # 子弹的方块
        self.rect.midbottom = init_pos
        self.speed = 3

    def move(self):
        self.rect.top += self.speed  # 子弹的位置不断的往前
# the class player
class Player(pygame.sprite.Sprite):
    def __init__(self, resources, player_rect, init_pos):
        pygame.sprite.Sprite.__init__(self)  # 一个基本的用于可见的游戏物体的类
        self.image = []                                 # 用来存储玩家对象精灵图片的列表
        for i in range(len(player_rect)):
            self.image.append(resources.subsurface(player_rect[i]).convert_alpha()) 
			# image中储存的是plane img的字图片，player_rect是用来取面积的矩形
			
        self.rect = player_rect[0]                      # 初始化图片所在的矩形
        self.rect.topleft = init_pos                    # 初始化矩形的左上角坐标
        self.speed = 8                                  # 初始化玩家速度，这里是一个确定的值
        self.bullets = pygame.sprite.Group()            # 玩家飞机所发射的子弹的集合
        self.img_index = 0                              # 玩家精灵图片索引
        self.is_hit = False                             # 玩家是否被击中

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

class Enemy(pygame.sprite.Sprite):
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
        
class Boss(pygame.sprite.Sprite):
    def __init__(self, resources, boss_rect, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.images = []                              # 用来存储玩家对象精灵图片的列表
#        self.rect = self.image.get_rect()
        self.rect = boss_rect
       # self.image = resources.subsurface(boss_rect[0])
        # for i in range(len(boss_rect)):
            # self.images.append(resources.subsurface(boss_rect[i]).convert_alpha()) 
        self.rect.topleft = init_pos
        self.speed = 3
        self.life = 20
        self.bullet_number = 5
        self.recharge = 200
        self.shoot_frequency = 15
        self.down_index = 0
        self.enemy_bullets = pygame.sprite.Group()
        
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
            
    def shoot(self, bullet_enemy_img): # 注意这里tuple不能接受下标修改，也不能直接和int相加减
        pos1 = list(self.rect.midbottom)
        pos1[0] = pos1[0] - 15
        enemy_bullet = Enemy_bullet(bullet_enemy_img, tuple(pos1))
        self.enemy_bullets.add(enemy_bullet)
        pos2 = list(self.rect.midbottom)
        pos2[0] = pos2[0] + 15
        enemy_bullet = Enemy_bullet(bullet_enemy_img, tuple(pos2))
        self.enemy_bullets.add(enemy_bullet)
   
    # def missile(self, target.x, target.y): 
        # missile = Missile(missile_image, self.rect.midtop)
        
        
        
        
        
        
        
        