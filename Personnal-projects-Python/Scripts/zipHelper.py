#coding=utf-8

'''
用于压缩的脚本，可以选择具体目标压缩，run: python zipHelper.py target1 target2... zipName
也可以将当前所有其他文件压缩。 run: python zipHelper.py all
'''

import zipfile
import sys, os

def compress_all(filename, path):
    print 'Begin to zip all the files...'
    print 'We have the following files now:'
    f_zip = zipfile.ZipFile(filename, 'w')
    for file in os.listdir(path):
        if os.path.isfile(file) and file != 'zipHelper.py' and '.zip' not in file:
            print file
            f_zip.write(file)
    f_zip.close()

def compress_target(filename, target):
    if len(target) <= 0:
        print 'Wrong with the input...'
        return
    else:
        f_zip = zipfile.ZipFile(filename, 'w')
        print 'The following files have been zipped:'
        for file in target:
            print file
            f_zip.write(file)
        f_zip.close()
        return
        
if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'Not enough inputs, the standard input should be python zipHelper.py target1 target2... zipName'
    else:
        path = os.getcwd()  #要进行压缩的文档目录
        # filename = sys.argv[-1] + '.zip'  #压缩后的文件名
        filename = sys.argv[-1] + '.zip' 
        if len(sys.argv) == 3 and sys.argv[1] == 'all':
            compress_all(filename, path)
        else:
            compress_target(filename, sys.argv[1 : -1])
        print 'All done!'