#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
a script to compare the pictures in two different dossiers and find the pictures only in one dossier and put them in another dossier resulat
'''
import os, sys
from PIL import Image
from progressbar import *
import shutil

def det(list1, list2): # 注意除非是直接copy coller的，不然就算是同一个pixel还是会有微量的差别，所以有这个
# function det来过滤掉小的差别
    sum1 = list1[0] + list1[1] + list1[2]
    sum2 = list2[0] + list2[1] + list2[2] 
    if (abs(sum1 - sum2) > 80):
        return True
    else:
        return False
        
def compare(error): 
    os.chdir(path1)
    list1 = os.listdir(path1)
    total = len(list1)
    pbar = ProgressBar().start()
    number = 0
    for one1 in list1:
        os.chdir(path1)
        image = Image.open(one1)
        data1 = image.getdata()
        
        os.chdir(path2)
        list2 = os.listdir(path2)
        
        for one2 in list2:
            image2 = Image.open(one2)
            data2 = image2.getdata()
            pointDiff = 0
            flagFind = 1
            for i in range(0,16800):
                if det(data1[i], data2[i]):
                    pointDiff += 1
                if (pointDiff > error):
                    flagFind = 0
                    break
            if (flagFind == 1):
                break
                
        if (flagFind == 0):
            listDiff.append(one1)
            
        number += 1 
        pbar.update(int(number / float(total) * 100))
    
    pbar.finish()
    
if __name__ == "__main__":
    path = os.getcwd()
    path1 = path + '\\group1'
    path2 = path + '\\group2'
    listDiff = list()
    error = 600
    compare(error)
    while len(listDiff) > 5:
        print 'Found extra pictures, changing the error and redo the calcul...'
        del listDiff[:] # 这个是清空list的方法，没有list.clear()这个方法。。。
        error += 200
        compare(error)

    if os.path.exists(path + '\\Result'):
        shutil.rmtree(path + '\\Result')  #删除一个非空目录
    os.mkdir(path + '\\Result')
    
    os.chdir(path1)
    for one in listDiff:
        shutil.copy(one, path + '\\Result')
   
    print "All done!"
        
        
     
