# -*-coding: utf-8 -*-
'''
使用迭代和黄金分割来画蒙德里安的画
Using recursion and the Golden ratio to draw Mondrian type picture
'''
from PIL import Image
import numpy as nu
from progressbar import *
import os
import random

# 这个function用来画线，有一个三维矩阵代表的图片data作为形参，然后有两个点作为画线的坐标，最后一个参数表示了线的宽度    
def fun_line(point1,point2,width,data): 
    pixel_selected = [] #a list where we stock the pixel selected for drawing the line
    newdata = [] #a list where we stock the new data for the pixels
      
    if point1[0] == point2[0]: # 首先是两个点的纵坐标相同
        if point1[1] < point2[1]:
            for w in range(int(point1[0] - width/2), int(point2[0] + width/2)): # 注意range中是int不是float，所以所有的都加上int强制转换
                for l in range(int(point1[1] - width/2), int((point2[1] + width/2))):                      
                    pixel_selected.append(search_pixel(w,l))
                                        
        elif point1[1] > point2[1]:
            for w in range(int(point1[0] - width/2), int(point2[0] + width/2)):
                for l in range(int(point2[1] - width/2), int(point1[1] + width/2)):
                    pixel_selected.append(search_pixel(w,l))
                    
        else:
            print 'Please make sure two points are different!'
            return
                                                       
    elif point1[1] == point2[1]: # 其次是两个点的横坐标相同
        if point1[0] < point2[0]:
            for l in range(int(point1[1] - width/2), int(point2[1] + width/2)):
                for w in range(int(point1[0] - width/2), int(point2[0] + width/2)):
                    pixel_selected.append(search_pixel(w,l))
                        
        elif point1[0] > point2[0]:
            for l in range(int(point1[1] - width/2), int(point2[1] + width/2)):
                for w in range(int(point2[0] - width/2), int(point1[0] + width/2)):
                    pixel_selected.append(search_pixel(w,l))
                        
        else:
            print 'Please make sure two points are different!'
            return
                    
    else:
        print 'Please make sure two points are either horizontal or vertical'
        return
    
    for num in range(0, len(data)):
        if num in pixel_selected:
            newdata.append((0,0,0))
        else:
            newdata.append(data[num])
    del pixel_selected
    return newdata
        
# 这个function用于给选定的矩形上色，两个坐标是对角线的两个点的坐标，color是一个用于表示颜色的tuple
def fun_paint(point1,point2,color,data): 
    if color[0] not in range(0,256) or color[1] not in range(0,256) or color[2] not in range(0,256):
        print 'The color you choose can\'t be presented'
        return 
    if point1[0] == point2[0] or point1[1] == point2[1]:
        print 'Something wrong with the diagonal points'
        return
        
    pixel_selected = []
    newdata = []
    
    for w in range(int(issmaller(point1[0],point2[0])), int(isbigger(point1[0], point2[0]) + 1)):
        for l in range(int(issmaller(point1[1],point2[1])), int(isbigger(point1[1], point2[1]) + 1)):
            if data[search_pixel(w,l)] != (0,0,0):
                pixel_selected.append(search_pixel(w,l))
            
    for num in range(0, len(data)):
        if num in pixel_selected:
            newdata.append(color)
        else:
            newdata.append(data[num])
    del pixel_selected
    return newdata

# 用迭代画图
# 一开始在形参中我用了*myList，但是发现这样有个问题，list自动变成tuple了，所以干脆就直接用myList然后最后return 到main()
def drawing(point1, point2, point3, point4, myList, end):
    point_list = point_order(point1, point2, point3, point4)
    # 用于调试和debug的
    # print myList
    # print len(myList)
    # print '\n'
    # print point1
    # print point2
    # print point3
    # print point4
    # print square(point_list)
    # print point_list
    # print '\n'
    # print '..............'
    if square(point_list) < end: 
        return 
        
    if det_form(point_list) == 'squ':
        if (len(myList) // 4) % 2 == 0: # 用于确定分割靠左靠右，本来以为要用一个变量记数的，后来发现只要用len(myList)就可以了
            myList.append((perfect(point_list[0][0], point_list[1][0], 1), point_list[0][1]))    
            myList.append((perfect(point_list[3][0], point_list[2][0], 1), point_list[3][1]))  
            drawing(myList[-1], myList[-2], point_list[1], point_list[2], myList, end)
        else:
            myList.append((perfect(point_list[0][0], point_list[1][0], 2), point_list[0][1]))    
            myList.append((perfect(point_list[3][0], point_list[2][0], 2), point_list[3][1]))    
            drawing(myList[-1], myList[-2], point_list[0], point_list[3], myList, end)
                     
    elif det_form(point_list) == 'rec_h':
        if (len(myList) // 4) % 2 == 0:
            myList.append((point_list[0][0], perfect(point_list[0][1], point_list[3][1], 2)))
            myList.append((point_list[1][0], perfect(point_list[1][1], point_list[2][1], 2)))
            drawing(myList[-1], myList[-2], point_list[0], point_list[1], myList, end)
        else:
            myList.append((point_list[0][0], perfect(point_list[0][1], point_list[3][1], 1)))
            myList.append((point_list[1][0], perfect(point_list[1][1], point_list[2][1], 1)))
            drawing(myList[-1], myList[-2], point_list[2], point_list[3], myList, end)
    
    else:
        if (len(myList) // 4 ) % 2 == 1: # 用于确定分割靠左靠右，本来以为要用一个变量记数的，后来发现只要用len(myList)就可以了
            myList.append((perfect(point_list[0][0], point_list[1][0], 1), point_list[0][1]))    
            myList.append((perfect(point_list[3][0], point_list[2][0], 1), point_list[3][1]))  
            drawing(myList[-1], myList[-2], point_list[1], point_list[2], myList, end)
        else:
            myList.append((perfect(point_list[0][0], point_list[1][0], 2), point_list[0][1]))    
            myList.append((perfect(point_list[3][0], point_list[2][0], 2), point_list[3][1]))    
            drawing(myList[-1], myList[-2], point_list[0], point_list[3], myList, end)
    
    return myList

# 得到可能涂色的方块对角线上的两点，这里用drawing的function把过程又走了一遍，然后用一个新的list来得到坐标
def painting(point1, point2, point3, point4, myList, end, paintingList):
    point_list = point_order(point1, point2, point3, point4)
    if square(point_list) < end: 
        return 
        
    if det_form(point_list) == 'squ':
        if (len(myList) // 4) % 2 == 0: # 用于确定分割靠左靠右，本来以为要用一个变量记数的，后来发现只要用len(myList)就可以了
            myList.append((perfect(point_list[0][0], point_list[1][0], 1), point_list[0][1]))    
            myList.append((perfect(point_list[3][0], point_list[2][0], 1), point_list[3][1])) 
            if len(myList) > 11: # 头几个大的方块还要继续分割，所以就不算在这个list中了
                paintingList.append(myList[-2])
                paintingList.append(point_list[3]) 
            painting(myList[-1], myList[-2], point_list[1], point_list[2], myList, end, paintingList)
        else:
            myList.append((perfect(point_list[0][0], point_list[1][0], 2), point_list[0][1]))    
            myList.append((perfect(point_list[3][0], point_list[2][0], 2), point_list[3][1]))  
            if len(myList) > 11:  
                paintingList.append(myList[-2])
                paintingList.append(point_list[2])  
            painting(myList[-1], myList[-2], point_list[0], point_list[3], myList, end, paintingList)
                     
    elif det_form(point_list) == 'rec_h':
        if (len(myList) // 4) % 2 == 0:
            myList.append((point_list[0][0], perfect(point_list[0][1], point_list[3][1], 2)))
            myList.append((point_list[1][0], perfect(point_list[1][1], point_list[2][1], 2)))
            if len(myList) > 11: 
                paintingList.append(myList[-2]) 
                paintingList.append(point_list[2])
            painting(myList[-1], myList[-2], point_list[0], point_list[1], myList, end, paintingList)
        else:
            myList.append((point_list[0][0], perfect(point_list[0][1], point_list[3][1], 1)))
            myList.append((point_list[1][0], perfect(point_list[1][1], point_list[2][1], 1)))
            if len(myList) > 11: 
                paintingList.append(myList[-2])
                paintingList.append(point_list[1])
            painting(myList[-1], myList[-2], point_list[2], point_list[3], myList, end, paintingList)
    
    else:
        if (len(myList) // 4) % 2 == 1: # 用于确定分割靠左靠右，本来以为要用一个变量记数的，后来发现只要用len(myList)就可以了
            myList.append((perfect(point_list[0][0], point_list[1][0], 1), point_list[0][1]))    
            myList.append((perfect(point_list[3][0], point_list[2][0], 1), point_list[3][1])) 
            if len(myList) > 11: 
                paintingList.append(myList[-2])
                paintingList.append(point_list[3])  
            painting(myList[-1], myList[-2], point_list[1], point_list[2], myList, end, paintingList)
        else:
            myList.append((perfect(point_list[0][0], point_list[1][0], 2), point_list[0][1]))    
            myList.append((perfect(point_list[3][0], point_list[2][0], 2), point_list[3][1]))
            if len(myList) > 11: 
                paintingList.append(myList[-2])
                paintingList.append(point_list[2])    
            painting(myList[-1], myList[-2], point_list[0], point_list[3], myList, end, paintingList)
    
    return paintingList
        
# 将4个点按逆时针排序
# 注意mydic = {sum1:point1, sum2:point2, sum3:point3, sum4:point4}有一个bug，因为如果是正方形的情况，有两个sum是一样的，但是dic中的key必须是不同的。
def point_order(point1, point2, point3, point4):
    mylist = []
    sum1 = point1[0] + point1[1]
    sum2 = point2[0] + point2[1]
    sum3 = point3[0] + point3[1]
    sum4 = point4[0] + point4[1]
    pointlist = []
    pointlist.append(point1)
    pointlist.append(point2)
    pointlist.append(point3)
    pointlist.append(point4) # 因为有正方形，所以加上一个list来确定第二和第四个点    
    mydic = {sum1:point1, sum2:point2, sum3:point3, sum4:point4}

    # x和y之和最小的是左上，最大的是右下
    mylist.append(mydic[min(mydic.keys())])
    pointlist.remove(mydic[min(mydic.keys())])
    del mydic[min(mydic.keys())]

    mylist.append(mydic[max(mydic.keys())])
    pointlist.remove(mydic[max(mydic.keys())])
    del mydic 
      
    for one in pointlist:
        if one[1] == mylist[0][1]:
            mylist.insert(1, one)
        else:
            mylist.append(one)
    del pointlist
    
    return mylist
        
# 区分是矩形还是正方形
def det_form(point_list):
    width = abs(point_list[1][0] - point_list[0][0])
    length = abs(point_list[2][1] - point_list[1][1])
    
    if abs(length - width) < 2: # 不用==因为float计算到后来有可能会有截断偏差
        return 'squ'
    else:
        if width > length:
            return 'rec_v'
        else:
            return 'rec_h'
         
# 计算黄金分割点的位置    
def perfect(point1, point2, position):
    coeff = (3 - 5**0.5)/2 # 1-0.618
    if position == 1:
        return (coeff*abs(point2 - point1) + point1)
    elif position == 2:
        return (point2 - coeff*abs(point2 - point1))
    else:
        print 'Wrong with the position...'
        return

# 计算这个矩形的面积        
def square(point_list):
    width = abs(point_list[0][0] - point_list[1][0])  
    length = abs(point_list[1][1] - point_list[2][1])
    
    return (width*length)

# 根据横坐标和纵坐标查找这个像素点在data中的位置        
def search_pixel(w,l):
    return (w*LENGTH + l) # 全部大写直接就是全局变量，注意这里直接是WIDTH，不用减1
        
def isbigger(a,b):
    if a > b:
        return a
    else:
        return b
        
def issmaller(a,b):
    if a > b:
        return b
    else:
        return a
        
def main():
    myList = []
    myList.append((100, 100))
    myList.append(((300*5**0.5 - 200), 100))
    myList.append(((300*5**0.5 - 200), 700))
    myList.append((100, 700)) # 一开始的四个点围成边框
    paintingList = []
    
    if os.path.isfile('result.png'):
        target = Image.open('result.png')
        print 'Found the picture without painting'
        newdata = target.getdata()
    else:
    # 新建图片文件
        target = Image.new('RGB', (LENGTH, WIDTH), 0xffffff)
        newdata = target.getdata()
        
        myList = drawing(myList[0], myList[1], myList[2], myList[3], myList, 500)
        myList = drawing(myList[4], myList[0], myList[1], myList[5], myList, 2000) #在第一个分割出的矩形中再次分割
        myList = drawing(myList[5], myList[6], myList[7], myList[2], myList, 2000) #在第二个分割出的矩形中再次分割
        myList = drawing(myList[8], myList[9], myList[3], myList[7], myList, 2000) #在第三个分割出的矩形中再次分割
        print 'All the positions determined, begin drawing...'
        pbar = ProgressBar().start()
        count = 0
        # 根据坐标画线
        newdata = fun_line(myList[0], myList[1], 8, newdata)
        newdata = fun_line(myList[1], myList[2], 8, newdata)
        newdata = fun_line(myList[2], myList[3], 8, newdata)
        newdata = fun_line(myList[3], myList[0], 8, newdata)
        count += 4
        pbar.update(int(count / float(len(myList)) * 100))
        
        # 用于画中间线条的循环，注意是每隔两个点循环一次
        for nu in range(4, len(myList), 2):
            newdata = fun_line(myList[nu], myList[nu+1], 4, newdata)
            count += 2
            pbar.update(int(count / float(len(myList)) * 100))
        pbar.finish()
        print '\n'
        
    myList = []
    myList.append((100, 100))
    myList.append(((300*5**0.5 - 200), 100))
    myList.append(((300*5**0.5 - 200), 700))
    myList.append((100, 700)) # 一开始的四个点围成边框
    # 获得每个方块对角线两点的坐标
    paintingList = painting(myList[0], myList[1], myList[2], myList[3], myList, 500, paintingList)
    paintingList = painting(myList[4], myList[0], myList[1], myList[5], myList, 2000, paintingList)
    paintingList = painting(myList[5], myList[6], myList[7], myList[2], myList, 2000, paintingList)
    paintingList = painting(myList[8], myList[9], myList[3], myList[7], myList, 2000, paintingList)
    print 'All the color is ready, begin painting...'
    pbar = ProgressBar().start()
    count = 0
    flag = 0 # 用于确保相邻的图片不是同一个颜色
    countWhite = 0 # 防止白色过多连续4个白色后要有一个别的颜色
    
    for nu in range(0, len(paintingList), 2):
        count += 2 # 一开始把这个进度条放在了下面，发现有问题，后来发现是因为白色话就直接continue了
        pbar.update(int(count / float(len(paintingList)) * 100))
    
        choice = random.randint(0,20)
        if choice < 6 or flag == 1:
                # print 'white'
            if countWhite < 3:
                flag = 0
                countWhite += 1
                continue
            else:
                newdata = fun_paint(paintingList[nu], paintingList[nu+1], (50,50,200), newdata)
                flag = 1
                countWhite = 0
        else:
            if choice == 10 or choice == 9 or choice > 18:
                newdata = fun_paint(paintingList[nu], paintingList[nu+1], (0,0,255), newdata)
                # print 'blue'
                flag = 1
            elif 10 < choice < 15:
                newdata = fun_paint(paintingList[nu], paintingList[nu+1], (255,0,0), newdata)
                # print 'red'
                flag = 1
            elif choice > 5 and choice < 9:
                newdata = fun_paint(paintingList[nu], paintingList[nu+1], (255,0,0), newdata)
                # print 'green'
                flag = 1
            else:
                newdata = fun_paint(paintingList[nu], paintingList[nu+1], (240,240,0), newdata)
                # print 'yellow'
                flag = 1
                
    pbar.finish()
    print '\n'
     # 将新的像素点data赋给target再保存
    target.putdata(newdata)
    target.save('result_painting.png')
     
    print 'All done!'
    
if __name__ == '__main__':
    LENGTH = 800 
    WIDTH = 600
    main()
    
    
    
        
    
    
    
    
    
    
    
    
    

