#!/usr/bin/python
#-*- coding:UTF-8 -*-
'''
用于修改一个目录下全部图片的尺寸
a script to put all the pictures in a dossier in the same size
'''

import os, sys
from PIL import Image
import shutil
from progressbar import *

def resize(width, height):
    myList = os.listdir(myPath)
    total = len(myList)
    pbar = ProgressBar().start()
    i = 0
    for one in myList:
        image = Image.open(one)
        new_image = image.resize((width, height), Image.ANTIALIAS)
        new_image.save(one)
        i += 1
        pbar.update(int(i / float(total) * 100))
    pbar.finish()
        
if __name__ == "__main__":
    if len(sys.argv) < 4:
        print 'Not enough inputs...'
        exit()
    path = os.getcwd()
    myPath = os.path.join(path, sys.argv[1])
    os.chdir(myPath)
    resize(int(sys.argv[2]), int(sys.argv[3]))    
    print 'All work done!'




