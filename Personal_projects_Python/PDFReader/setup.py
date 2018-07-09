#! /usr/bin/env python  
# -*- coding: utf-8 -*-  
# 用法: 和所有需要的py文件放在同一个目录下，然后console里面打 python setup.py py2exe 即可

from distutils.core import setup  
import py2exe  
options = {"py2exe":{"compressed": 1, #压缩  
                     "optimize": 2,  
                     "bundle_files": 1, #所有文件打包成一个exe文件  
                     "dll_excludes": ["numpy-atlas.dll"] # console里面说找不到这个dll，所以就直接加上去
                     }}  
setup(
    console=["invoiceHelper.py"], #这个setup中不用加上另外两个py文件
    options=options,  
    zipfile=None)   