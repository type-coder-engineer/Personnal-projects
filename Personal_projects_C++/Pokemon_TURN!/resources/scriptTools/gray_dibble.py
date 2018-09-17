#coding: utf
from PIL import Image
import shutil, os
from progressbar import *

def dibble(myPath):
    myList = os.listdir(myPath)
    total = len(myList)
    pbar = ProgressBar().start()
    i = 0
    for file in myList:
        if file[-2:] == 'py':
            continue
        target = Image.open(file)
        data = target.getdata()
        newData = []
        for one in data:
            if one[3] >= 200:
                newData.append((90,90,90,255))
            else:
                newData.append((255,255,255,255))
        target.putdata(newData)
        filename = ('gray_' + file)
        target.save(filename)
        i += 1
        pbar.update(int(i / float(total) * 100))
    pbar.finish()
    
if __name__ == '__main__':
    myPath = os.getcwd()
    dibble(myPath)