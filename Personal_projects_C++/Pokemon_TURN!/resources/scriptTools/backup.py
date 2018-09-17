# -*- coding: utf-8 -*-
# 一开始如果没有backup目录会新建一个backup目录
# 每次可以备份多个个文件，或者使用python backup.py all type 来备份所有该
# 类型的文件，已有的文件会被覆盖
#在终端中run: python backup.py filename 即可

import sys, os
import shutil

def backup(files):
    if os.path.isdir(myDes):
        cleanupOriginal(files)
    else:
        os.mkdir(os.path.join(myPath, myDes))
    os.chdir(myPath)
    for file in files:
        try:
            shutil.copy(file, myDes)
        except:
            print 'Error with the file " {} " during the copy'.format(file)
    print 'All done!'
    info()
    
def cleanupOriginal(targetFiles):
    fileNames = os.listdir(myDes)
    os.chdir(os.path.join(myPath, myDes))
    for name in fileNames:
        try:
            if name in targetFiles:
                os.remove(name)
            else:
                pass
        except:
            print 'Error with the file " {} "during the cleanup'.format(name)

def backupAll(targets):
    allFiles = os.listdir(myPath)
    targetFiles = []
    for file in allFiles:
        index = file.find('.')
        if index != -1 and index <= len(file) - 2:
            if file[index + 1:] in targets:
                targetFiles.append(file)
            else:
                pass
        else:
            pass
    backup(targetFiles)
            
def info():
    filenames = os.listdir(myDes)
    os.chdir(os.path.join(myPath, myDes))
    print "Now you have: ",
    for name in filenames:
        print name + "  ",
    print "as the backup document(s)"
    
if __name__ == '__main__':
    myPath = os.getcwd()
    myDes = 'backup'
    if len(sys.argv) < 2:
        print 'Wrong input...'
    else:
        if sys.argv[1] != 'all':
            backup(sys.argv[1:])
        else:
            if len(sys.argv) == 2:
                print 'Not enough inputs...'
            else:
                backupAll(sys.argv[2:])    
    
    
    