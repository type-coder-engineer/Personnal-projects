# -*- coding: utf-8 -*-

import sys
import os
from PIL import Image
import shutil

def main(filename, transparency):
    if not os.path.isfile(filename):
        print 'No such picture file...'
        return
    elif int(transparency) > 100:
        print 'The rate of transparency should be less than 100'
        print transparency
        return
    else:
        if filename[-3:] != 'png':
            im = Image.open(filename)
            targetName = filename[:-4] + '.' + 'png'
            im.convert('RGBA').save(targetName)
            os.remove(filename)
        else:
            im = Image.open(filename)
            if im.mode != 'RGBA':
                im.convert('RGBA').save(filename)
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
    main(sys.argv[1], sys.argv[2])