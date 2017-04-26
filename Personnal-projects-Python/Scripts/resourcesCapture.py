# -*- coding: utf-8 -*-

'''
用于抓取一张图片上的某一部分，输入的zone是左上角的坐标和右下角的坐标，注意是先宽后高
run: python resourceCapture.py pictureName
'''

import os, sys
from PIL import Image
import matplotlib.pyplot as plt

def capture(filename):
    img = Image.open(filename)
    print img.size
    while(1):
        region = raw_input('your zone?\n').split(',')
        if region[0] == 'stop' or region[0] == 'quit' or region[0] == 'exit':
            exit()
        if region[0] == 'save' or region[0] == 'cut':
            try:
                if len(region) == 1:
                    new.save('cut.png')
                else:
                    new.save(region[1])
                plt.show()
                continue
            except:
                print 'No captured image....'
                continue
            
        if len(region) != 4:
            print 'Wrong input...You should give 4 ints as the positions of two points'
            continue
                
        myregion = list()
        for one in region:
            myregion.append(int(one))
            
        myregion[2] = myregion[0] + myregion[2]
        myregion[3] = myregion[1] + myregion[3]
            
        cut = tuple(myregion)
        new = img.crop(cut)
        plt.subplot(2, 1, 1)
        plt.imshow(img)
        plt.subplot(2, 1, 2)
        plt.imshow(new)
        plt.show()

if __name__ == '__main__':
    capture(sys.argv[1])


        
        