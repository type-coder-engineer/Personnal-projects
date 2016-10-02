# -*- coding: utf-8 -*-

import random

allTeams = ['热火', '雷霆', '马刺', '勇士', '步行者', '篮网', '开拓者', '小牛', '凯尔特人', '森林狼', '灰熊', '奇才', '鹈鹕', '掘金', '76人', '太阳', '活塞', '猛龙',\
'魔术', '老鹰', '爵士', '雄鹿', '骑士', '黄蜂', '公牛', '尼克斯', '快船', '火箭', '国王', '湖人']

    
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
        
if __name__ == '__main__':
    choice = ''
    last = []
    while(choice != 'exit'): 
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
                
        for x in range(0, 3):
            print allTeams[namelist[x]],
            print "          ",
        print '\n'
        print '**********************************************'
        choice = raw_input()
        last = namelist