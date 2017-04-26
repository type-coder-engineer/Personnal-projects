#!/usr/bin/python
#-*- coding:UTF-8 -*-
'''
一个用来给批量图片命名同时将尺寸调节一致的脚本
run: python rename.py dirName
'''
import os, sys
from PIL import Image
import shutil

def reNameAll():
    if os.path.exists(myPath + '\\resize'):
        shutil.rmtree(myPath + '\\resize')  #删除一个非空目录
    myList = os.listdir(myPath)

    myList.sort(key=lambda x:int(x[:-4]))  #以数字大小为规则排序，因为名字里有.png 所以有一个lambda函数规定比较的是.png 前面的东西

    i = 1
    for one in myList:
        if os.path.splitext(one)[1] in optionalForme: #用点将文件名字分开，这样可以看是否是.png 或 .jpg 文件
            if one != str(i) + '.png':
                os.rename(one, str(i) + '.png')
            i += 1
            
def resizeImage(mypath):
    if not os.path.exists(myPath + '\\resize'):
        os.mkdir(mypath + '\\resize')
    myResizePath = mypath + '\\resize'

    myList = os.listdir(myPath)
    for one in myList:
        if os.path.splitext(one)[1] in optionalForme and os.path.isfile(one):
            shutil.copy(one, 'resize')
    
    os.chdir(myResizePath)
    myListNow = os.listdir(myResizePath)

    for one in myListNow:
        if os.path.splitext(one)[1] in optionalForme:
            image = Image.open(one)
            new_image = image.resize((150,180), Image.ANTIALIAS) # pokemon就不用修剪了，因为原来图片就很好，把体积压缩一下就OK
            # region = (0,0,300,270) # 注意这个区域是从左上角那个店作为(0,0)来设定的
            # resizeImage = new_image.crop(region)
            # resizeImage.resize((100,100), Image.ANTIALIAS)
            # resizeImage.save(one)# 一直有一个bug，发现是因为第一resize作为目录没有后缀名，所以没法
            # # 被if os.path.splitext(one)[1] in optionalForme 过滤掉，第二，有一个.DS_Store作为mac储存信息的文件，要先删掉。
            # # 所以要在修改尺寸的时候也加上if os.path.splitext(one)[1] in optionalForme
            os.remove(one)
            new_image.save('1_' + one)

if __name__ == "__main__":
    path = os.getcwd()
    if len(sys.argv) < 2:
        print 'Not enough inputs, standard input should be: python rename.py dirName'
    myPath = os.path.join(path, sys.argv[1])
    os.chdir(myPath)   
    optionalForme = ('.png', '.jpg')
    
    reNameAll()
    print "Renaming done!"
    
    resizeImage(myPath)
    print "All the work done!"