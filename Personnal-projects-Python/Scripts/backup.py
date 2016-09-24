#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os
import shutil

def backup(file1, file2):
    if os.path.isdir(mydes):
        cleanup()
    else:
        os.mkdir(os.path.join(mypath, mydes))
    os.chdir(mypath)
    shutil.copy(file1, mydes)
    shutil.copy(file2, mydes)
    
def cleanup():
    filenames = os.listdir(mydes)
    os.chdir(os.path.join(mypath, mydes))
    for name in filenames:
        try:
            os.remove(name)
        except:
            print 'Unknown mistakes...'

if __name__ == '__main__':
    mypath = os.getcwd()
    mydes = 'backup'
    backup(sys.argv[1], sys.argv[2])
    print 'All done!'