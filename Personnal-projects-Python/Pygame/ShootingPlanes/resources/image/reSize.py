#!/usr/bin/python
#-*- coding:UTF-8 -*-

import os, sys
from PIL import Image
from progressbar import *

def reSizeAll():
    myList = os.listdir(myPath)
    total = len(myList)
    pbar = ProgressBar().start()
    i = 0
    for one in myList:
        image = Image.open(one)
        new_image = image.resize((myList[0], myList[1]), Image.ANTIALIAS)
        new_image.save(one)
        i += 1
        pbar.update(int(i / float(total) * 100))
    pbar.finish()
  
def reSize(file):
    image = Image.open(file)
    new_image = image.resize((myList[0], myList[1]), Image.ANTIALIAS)
    if sys.argv[2] != None:
        new_image.save(sys.argv[2])
    else:
        new_image.save(file)
    
if __name__ == "__main__":
    myPath = os.getcwd()
    dimensions = raw_input('What dimensions would you like?\n').split(',')
    myList = []
    for one in dimensions:
        myList.append(int(one))
        
    if sys.argv[1] == 'all':
        reSizeAll()    
    else:
        reSize(sys.argv[1])
    print 'All done!'




