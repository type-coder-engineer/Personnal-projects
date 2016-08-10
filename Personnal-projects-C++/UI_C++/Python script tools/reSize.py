#!/usr/bin/python
#-*- coding:UTF-8 -*-

import os
from PIL import Image
import shutil
from progressbar import *

def reSize():
    myList = os.listdir(myPath)
    total = len(myList)
    pbar = ProgressBar().start()
    i = 0
    for one in myList:
        image = Image.open(one)
        new_image = image.resize((100,110), Image.ANTIALIAS)
        new_image.save(one)
        i += 1
        pbar.update(int(i / float(total) * 100))
    pbar.finish()
        
if __name__ == "__main__":
    currentPath = os.getcwd()
    myPath = currentPath + '\\lianliankan_ui\\image'
    os.chdir(myPath)
    reSize()    
    print 'All work done!'




