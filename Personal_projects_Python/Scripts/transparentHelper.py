# -*- coding: utf-8 -*-

'''
用于调整一张图片的透明度的，如果不是png格式会先转化成png的RGBA格式然后调整透明度
run: python transparentHelper.py pictureName transparency
'''
import sys
import os
from PIL import Image
import shutil

def main(filename, transparency):
    if not os.path.isfile(filename):
        print 'No such picture file...'
        return
    elif int(transparency) > 100 or int(transparency) < 0:
        print 'Wrong input, the rate of transparency should be between 0 and 100'
        return
    else:
        if filename[-3:] != 'png':
            try:
                im = Image.open(filename)
                targetName = filename[:-4] + '.' + 'png'
                im.convert('RGBA').save(targetName)
                os.remove(filename)
            except:
                print 'Error occured when changing the mode RGBA for the file " {} "'.format(filename)
                return
        else:
            im = Image.open(filename)
            if im.mode != 'RGBA':
                try:
                    im.convert('RGBA').save(filename)
                except:
                    print 'Error occured when changing the mode RGBA for the file " {} "'.format(filename)
                    return
            im.close()
            targetName = filename
        transparency = int(transparency)
        rate = int(255 * transparency / 100)
        newName = targetName[:-4] + '_' + str(transparency) + '%' + targetName[-4:]
        shutil.copy(targetName, newName)
        target = Image.open(newName)
        data = target.getdata()
        newData = []
        for i in data:
            newData.append((i[0], i[1], i[2], rate))
        
        target.putdata(newData)
        target.save(newName)
        print 'All done!'
    
if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'Not enough inputs, standard input should be: python transparentHelper.py pictureName transparency'
        exit()
    main(sys.argv[1], sys.argv[2])    
    