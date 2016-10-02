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
        transparency = int(transparency)
        rate = int(255 * transparency / 100)
        newname = filename[:-4] + '_' + str(transparency) + '%' + filename[-4:]
        shutil.copy(filename, newname)
        target = Image.open(newname)
        data = target.getdata()
        newdata = []
        for i in data:
            newdata.append((i[0], i[1], i[2], rate))
        
        target.putdata(newdata)
        target.save(newname)
        print 'All done!'
    
if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])