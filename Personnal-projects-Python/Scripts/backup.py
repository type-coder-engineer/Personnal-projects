#!/usr/bin/python
# -*- coding: utf-8 -*-
# 每次可以保存一个文件，如果有同名文件就取代，一开始会新建一个backup目录
#在终端中run: backup.py filename 即可

import sys, os
import shutil

def backup(file):
    if os.path.isdir(mydes):
        cleanup(file)
    else:
        os.mkdir(os.path.join(mypath, mydes))
    os.chdir(mypath)
    shutil.copy(file, mydes)
    
def cleanup(file):
    filenames = os.listdir(mydes)
    os.chdir(os.path.join(mypath, mydes))
    for name in filenames:
        try:
            if name == file:
                os.remove(name)
            else:
                pass
        except:
            print 'Unknown mistakes during the cleanup...'
            
def info():
    filenames = os.listdir(mydes)
    os.chdir(os.path.join(mypath, mydes))
    print "Now you have: ",
    for name in filenames:
        print name + "  ",
    print "as the backup document(s)"
    
if __name__ == '__main__':
    mypath = os.getcwd()
    mydes = 'backup'
    backup(sys.argv[1])
    print 'All done!'
    info()