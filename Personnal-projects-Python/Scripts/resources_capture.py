# -*- coding: utf-8 -*-

import os
from PIL import Image
import matplotlib.pyplot as plt

img = Image.open('shoot.png')
while(1):
    region = raw_input('your zone?\n').split(',')
    if region[0] == "stop":
        exit()
    if region[0] == "last":
        try:
            plt.imshow(new)
            plt.show()
            continue
        except:
            plt.imshow(img)
            plt.show()
            continue
        
    if len(region) != 4:
        print 'wrong input'
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

#region = raw_input('your zone?\n').split(',')