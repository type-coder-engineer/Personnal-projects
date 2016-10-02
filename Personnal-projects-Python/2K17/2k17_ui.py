# -*- coding: utf-8 -*-

import random, time, os
from sys import exit
import pygame
from pygame.locals import *

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

if os.name == 'posix':
    flags = FULLSCREEN | DOUBLEBUF
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags)

else:
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption('2K17')

background = pygame.image.load('2K17_20%.png').convert_alpha() # 要用convert_alpha如果你的图片的
# alpha通道不是255，然后你的背景颜色要设为白色，不然图片半透明后就变黑了

# allTeams = ['热火', '雷霆', '马刺', '勇士', '步行者', '篮网', '开拓者', '小牛', '凯尔特人', '森林狼', '灰熊', '奇才', '鹈鹕', '掘金', '76人', '太阳', '活塞', '猛龙',\
# '魔术', '老鹰', '爵士', '雄鹿', '骑士', '黄蜂', '公牛', '尼克斯', '快船', '火箭', '国王', '湖人']
allTeams =['1', '2', '3', '4', '5']

def opening():
    running = 1
    clock = pygame.time.Clock()
    error = 4
    myX = [-error, error, -error, error]
    myY = [error, error, -error, -error]
    myChooseIndex = 0
    myChooseCenterx = screen.get_rect().centerx
    myChooseCentery = screen.get_rect().centery + 170
    myExitIndex = 0
    myExitCenterx = screen.get_rect().centerx
    myExitCentery = screen.get_rect().centery + 250  # back按钮原来的位置
    flag1 = flag2 = 0
    flag_show = 0
    titleFont = pygame.font.Font('freesansbold.ttf', 30)
    choiceFont = pygame.font.Font('freesansbold.ttf', 35)
    teamFont = pygame.font.Font('freesansbold.ttf', 45)
    startText = choiceFont.render('Choose your team!', True, (0, 0, 0))
    exitText = titleFont.render('Exit', True, (0, 0, 0))
    startRect = startText.get_rect()
    exitRect = exitText.get_rect()
    
    while running:
        clock.tick(60)
    
        screen.fill((255,255,255))
        screen.blit(background, (0, 0))
        
        startRect.centerx = myChooseCenterx
        startRect.centery = myChooseCentery
        exitRect.centerx = myExitCenterx
        exitRect.centery = myExitCentery
        
        if flag1 == 0:
            screen.blit(startText, startRect)
        if flag2 == 0:
            screen.blit(exitText, exitRect)
        
        showlist = list(pygame.mouse.get_pos())
        if showlist[0] > 235 and showlist[0] < 565 and showlist[1] > 440 and showlist[1] < 480:
            myChooseIndex += 1
            flag1 = 1
            flag2 = 0
            if myChooseIndex // 7 >= 1 and myChooseIndex % 7 == 0:
                startRect.centerx = myChooseCenterx + myX[myChooseIndex // 7 - 1]
                startRect.centery = myChooseCentery + myY[myChooseIndex // 7 - 1]
                
            if myChooseIndex > 33:
                myChooseIndex = 0
            screen.blit(startText, startRect)
            
        elif showlist[0] > 370 and showlist[0] < 430 and showlist[1] > 535 and showlist[1] < 570:
            myExitIndex += 1
            flag2 = 1
            flag1 = 0
            if myExitIndex // 7 >= 1 and myExitIndex % 7 == 0:
                exitRect.centerx = myExitCenterx + myX[myExitIndex // 7 - 1]
                exitRect.centery = myExitCentery + myY[myExitIndex // 7 - 1]
                
            if myExitIndex > 33:
                myExitIndex = 0
            screen.blit(exitText, exitRect)
            
        else:
            flag1 = flag2 = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # pass
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                poslist = list(pygame.mouse.get_pos())
                # print pygame.mouse.get_pos()  # 用于测试选择项的两个端点的坐标的
                if poslist[0] > 370 and poslist[0] < 430 and poslist[1] > 535 and poslist[1] < 570:
                    pygame.quit()
                    exit()
                if poslist[0] > 235 and poslist[0] < 565 and poslist[1] > 440 and poslist[1] < 480:
                    return 'choose'
                    
        pygame.display.update()  
 
def limit(x): #
    if x > 4:
        return (x - 5)
    elif x < 0:
        return 4
    else:
        return x
        
def show(chosenTeams):
    running = 1
    clock = pygame.time.Clock()
    error = 4
    myX = [-error, error, -error, error]
    myY = [error, error, -error, -error]
    myChooseIndex = 0
    myChooseCenterx = screen.get_rect().centerx
    myChooseCentery = screen.get_rect().centery + 170
    myExitIndex = 0
    myExitCenterx = screen.get_rect().centerx
    myExitCentery = screen.get_rect().centery + 250  # back按钮原来的位置
    flag1 = flag2 = 0
    titleFont = pygame.font.Font('freesansbold.ttf', 30)
    choiceFont = pygame.font.Font('freesansbold.ttf', 35)
    teamFont1 = pygame.font.Font('freesansbold.ttf', 60)
    teamFont2 = pygame.font.Font('freesansbold.ttf', 35)
    teamFont3 = pygame.font.Font('freesansbold.ttf', 10)
    startText = choiceFont.render('Choose your team!', True, (0, 0, 0))
    exitText = titleFont.render('Exit', True, (0, 0, 0))
    startRect = startText.get_rect()
    exitRect = exitText.get_rect()
    startRect.centerx = screen.get_rect().centerx
    startRect.centery = screen.get_rect().centery + 170
    exitRect.centerx = screen.get_rect().centerx
    exitRect.centery = screen.get_rect().centery + 250
    
    order = range(0, 5)  # 通过乱序使得每次队伍的名字都不同
    random.shuffle(order)
    mylist = []
    for one in order:
        mylist.append(allTeams[one])
    
    print mylist
    myIndex1 = 0
    myIndex2 = 1
    myIndex3 = 2
    myTime = 0
    myIndex = 0
    
    myLeftCenterx = screen.get_rect().centerx - 150
    myMiddleCenterx = screen.get_rect().centerx + 50
    myRightCenterx = screen.get_rect().centerx + 250
    my1Centery = screen.get_rect().centery - 230
    my2Centery = screen.get_rect().centery - 170
    my3Centery = screen.get_rect().centery - 110
    my4Centery = screen.get_rect().centery - 50
    my5Centery = screen.get_rect().centery + 10
    flag_ok1 = 0
    flag_ok2 = 0
    flag_ok3 = 0
    team1ok = allTeams[chosenTeams[0]]
    team2ok = allTeams[chosenTeams[1]]
    team3ok = allTeams[chosenTeams[2]]
    
    titleText = titleFont.render('Your team: ', True, (0, 0, 0))    
    titleText_rect = titleText.get_rect()   
    titleText_rect.centerx = screen.get_rect().centerx - 300
    titleText_rect.centery = screen.get_rect().centery - 80
    
    while running:
        clock.tick(60)
    
        screen.fill((255,255,255))
        screen.blit(background, (0, 0))

        team1 = teamFont3.render(mylist[limit(myIndex1)], True, (0, 0, 0))
        team2 = teamFont2.render(mylist[limit(myIndex1 + 1)], True, (0, 0, 0))
        team3 = teamFont1.render(mylist[limit(myIndex1 + 2)], True, (0, 0, 0))
        team4 = teamFont2.render(mylist[limit(myIndex1 + 3)], True, (0, 0, 0))
        team5 = teamFont3.render(mylist[limit(myIndex1 + 4)], True, (0, 0, 0))
        team6 = teamFont3.render(mylist[limit(myIndex2)], True, (0, 0, 0))
        team7 = teamFont2.render(mylist[limit(myIndex2 + 1)], True, (0, 0, 0))
        team8 = teamFont1.render(mylist[limit(myIndex2 + 2)], True, (0, 0, 0))
        team9 = teamFont2.render(mylist[limit(myIndex2 + 3)], True, (0, 0, 0))
        team10 = teamFont3.render(mylist[limit(myIndex2 + 4)], True, (0, 0, 0))
        team11 = teamFont3.render(mylist[limit(myIndex3)], True, (0, 0, 0))
        team12 = teamFont2.render(mylist[limit(myIndex3 + 1)], True, (0, 0, 0))
        team13 = teamFont1.render(mylist[limit(myIndex3 + 2)], True, (0, 0, 0))
        team14 = teamFont2.render(mylist[limit(myIndex3 + 3)], True, (0, 0, 0))
        team15 = teamFont3.render(mylist[limit(myIndex3 + 4)], True, (0, 0, 0))
        # print  mylist[limit(myIndex1)]
        # print  mylist[limit(myIndex1 + 1)]
        # print  mylist[limit(myIndex1 + 2)]
        # print  mylist[limit(myIndex1 + 3)]
        # print  mylist[limit(myIndex1 + 4)]
        # print '%%%%%%%%%%%%%%%%%'
        
        team1_rect = team1.get_rect()
        team2_rect = team2.get_rect()
        team3_rect = team3.get_rect()
        team4_rect = team4.get_rect()
        team5_rect = team5.get_rect()
        team6_rect = team6.get_rect()
        team7_rect = team7.get_rect()
        team8_rect = team8.get_rect()
        team9_rect = team9.get_rect()
        team10_rect = team10.get_rect()
        team11_rect = team11.get_rect()
        team12_rect = team12.get_rect()
        team13_rect = team13.get_rect()
        team14_rect = team14.get_rect()
        team15_rect = team15.get_rect()
        
        team1_rect.centerx = myLeftCenterx
        team2_rect.centerx = myLeftCenterx
        team3_rect.centerx = myLeftCenterx
        team4_rect.centerx = myLeftCenterx
        team5_rect.centerx = myLeftCenterx
        team6_rect.centerx = myMiddleCenterx
        team7_rect.centerx = myMiddleCenterx
        team8_rect.centerx = myMiddleCenterx
        team9_rect.centerx = myMiddleCenterx
        team10_rect.centerx = myMiddleCenterx     
        team11_rect.centerx = myRightCenterx
        team12_rect.centerx = myRightCenterx
        team13_rect.centerx = myRightCenterx
        team14_rect.centerx = myRightCenterx
        team15_rect.centerx = myRightCenterx
        
        if flag_ok1:
            team1_rect.centery = my1Centery + 30
            team2_rect.centery = my2Centery + 30
            team3_rect.centery = my3Centery + 30
            team4_rect.centery = my4Centery + 30
            team5_rect.centery = my5Centery + 30
                                                                     
        if flag_ok2:                                          
            team6_rect.centery = my1Centery + 30
            team7_rect.centery = my2Centery + 30
            team8_rect.centery = my3Centery + 30
            team9_rect.centery = my4Centery + 30
            team10_rect.centery = my5Centery + 30
                                                                      
        if flag_ok3:                                            
            team11_rect.centery = my1Centery + 30
            team12_rect.centery = my2Centery + 30
            team13_rect.centery = my3Centery + 30
            team14_rect.centery = my4Centery + 30
            team15_rect.centery = my5Centery + 30      
        
        if myTime < 120:
            if myIndex == 6:
                myIndex1 = limit(myIndex1 - 1)
                myIndex2 = limit(myIndex2 - 1)
                myIndex3 = limit(myIndex3 - 1)         
           
            team1_rect.centery = my1Centery + 10 * myIndex
            team2_rect.centery = my2Centery + 10 * myIndex
            team3_rect.centery = my3Centery + 10 * myIndex
            team4_rect.centery = my4Centery + 10 * myIndex
            team5_rect.centery = my5Centery + 10 * myIndex
            team6_rect.centery = my1Centery + 10 * myIndex
            team7_rect.centery = my2Centery + 10 * myIndex
            team8_rect.centery = my3Centery + 10 * myIndex
            team9_rect.centery = my4Centery + 10 * myIndex
            team10_rect.centery = my5Centery + 10 * myIndex
            team11_rect.centery = my1Centery + 10 * myIndex
            team12_rect.centery = my2Centery + 10 * myIndex
            team13_rect.centery = my3Centery + 10 * myIndex
            team14_rect.centery = my4Centery + 10 * myIndex
            team15_rect.centery = my5Centery + 10 * myIndex     
                                                                                 
        if myTime >= 120:  
            if myIndex == 30:    # 没事不要随便用% == 0， 因为0也可以是余数为0的，所以可能就变了两次。。。
                if flag_ok1 == 0:
                    myIndex1 = limit(myIndex1 - 1)
                if flag_ok2 == 0:
                    myIndex2 = limit(myIndex2 - 1)
                if flag_ok3 == 0:
                    myIndex3 = limit(myIndex3 - 1) 
            
            if flag_ok1 == 0:  
                team1_rect.centery = my1Centery + 2 * myIndex
                team2_rect.centery = my2Centery + 2 * myIndex
                team3_rect.centery = my3Centery + 2 * myIndex
                team4_rect.centery = my4Centery + 2 * myIndex
                team5_rect.centery = my5Centery + 2 * myIndex
            if flag_ok2 == 0:                                                           
                team6_rect.centery = my1Centery + 2 * myIndex
                team7_rect.centery = my2Centery + 2 * myIndex
                team8_rect.centery = my3Centery + 2 * myIndex
                team9_rect.centery = my4Centery + 2 * myIndex
                team10_rect.centery = my5Centery + 2 * myIndex
            if flag_ok3 == 0:                                                      
                team11_rect.centery = my1Centery + 2 * myIndex
                team12_rect.centery = my2Centery + 2 * myIndex
                team13_rect.centery = my3Centery + 2 * myIndex
                team14_rect.centery = my4Centery + 2 * myIndex
                team15_rect.centery = my5Centery + 2 * myIndex
                    
        if myTime > 360:
            if mylist[limit(myIndex1 + 2)] == team1ok:
                flag_ok1 = 1
            if mylist[limit(myIndex2 + 2)] == team2ok:
                flag_ok2 = 1
            if mylist[limit(myIndex3 + 2)] == team3ok:
                flag_ok3 = 1
                
        myTime += 1
        myIndex += 1
        if myTime < 120:
            if myIndex > 6:
                myIndex = 0
        else:
            if myIndex > 30:
                myIndex = 0
                
        screen.blit(team1, team1_rect)
        screen.blit(team2, team2_rect)
        screen.blit(team3, team3_rect)
        screen.blit(team4, team4_rect)
        screen.blit(team5, team5_rect)
        screen.blit(team6, team6_rect)
        screen.blit(team7, team7_rect)
        screen.blit(team8, team8_rect)
        screen.blit(team9, team9_rect)
        screen.blit(team10, team10_rect)
        screen.blit(team11, team11_rect)
        screen.blit(team12, team12_rect)
        screen.blit(team13, team13_rect)
        screen.blit(team14, team14_rect)
        screen.blit(team15, team15_rect)
              
        screen.blit(titleText, titleText_rect)
        
        if flag1 == 0:
            screen.blit(startText, startRect)
        if flag2 == 0:
            screen.blit(exitText, exitRect)
        
        if flag_ok1 and flag_ok2 and flag_ok3:
            showlist = list(pygame.mouse.get_pos())
            if showlist[0] > 235 and showlist[0] < 565 and showlist[1] > 440 and showlist[1] < 480:
                myChooseIndex += 1
                flag1 = 1
                flag2 = 0
                if myChooseIndex // 7 >= 1 and myChooseIndex % 7 == 0:
                    startRect.centerx = myChooseCenterx + myX[myChooseIndex // 7 - 1]
                    startRect.centery = myChooseCentery + myY[myChooseIndex // 7 - 1]
                    
                if myChooseIndex > 33:
                    myChooseIndex = 0
                screen.blit(startText, startRect)
                
            elif showlist[0] > 370 and showlist[0] < 430 and showlist[1] > 535 and showlist[1] < 570:
                myExitIndex += 1
                flag2 = 1
                flag1 = 0
                if myExitIndex // 7 >= 1 and myExitIndex % 7 == 0:
                    exitRect.centerx = myExitCenterx + myX[myExitIndex // 7 - 1]
                    exitRect.centery = myExitCentery + myY[myExitIndex // 7 - 1]
                    
                if myExitIndex > 33:
                    myExitIndex = 0
                screen.blit(exitText, exitRect)
                
            else:
                flag1 = flag2 = 0
    
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # pass
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    poslist = list(pygame.mouse.get_pos())
                    # print pygame.mouse.get_pos()  # 用于测试选择项的两个端点的坐标的
                    if poslist[0] > 370 and poslist[0] < 430 and poslist[1] > 535 and poslist[1] < 570:
                        pygame.quit()
                        exit()
                    if poslist[0] > 235 and poslist[0] < 565 and poslist[1] > 440 and poslist[1] < 480:
                        return 
                    
        pygame.display.update()      
        

def randomTeam(allTeams):
    team1 = random.randint(0, len(allTeams) - 1)
    team2 = random.randint(0, len(allTeams) - 1)
    team3 = random.randint(0, len(allTeams) - 1)
    
    while(team2 == team1):
        team2 = random.randint(0, len(allTeams) - 1)
        
    while(team3 == team2 or team3 == team1):
        team3 = random.randint(0, len(allTeams) - 1)
    
    nameList = [team1, team2, team3]
    return nameList
 
# def main():
    # opening()
    # show()
        
if __name__ == '__main__':
    choice = ''
    last = []
    opening()
    while(1):
        noRepeat = 0
        while(noRepeat != 1):
            namelist = randomTeam(allTeams)
            if len(last) != 0:
                noRepeat = 1
                for x in range(0,3):
                    if namelist[x] in last:
                       noRepeat = 0

            else:
                noRepeat = 1
                
        show(namelist)        
        last = namelist
        
        
        
        
        
        