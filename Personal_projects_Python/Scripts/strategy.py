# -*-coding: utf-8 -*-
import random
import os

def getModel(type):
    data = []
    for i in range(1000):
        data.append(0)
        
    if type == 1:
        data[0] = 2000
        data[999] = 5000
        
    elif type == 2:
        data[0] = 2000
        data[300] = 6000
        data[600] = 4000
        data[999] = 5000

    return data

def getLine(data):
    referencePoint = []
    for i in range(len(data)):
        if data[i] != 0:
            referencePoint.append(i)
    if (len(referencePoint) < 2):
        print '[getLine] - Something wrong with this data, no reference point'
        
    print '[getLine] - Begin to generate the curve based on the first reference points'
    for i in range(len(referencePoint) - 1):
        firstDate = referencePoint[i]
        firstValue = data[referencePoint[i]]
        secondDate = referencePoint[i + 1]
        secondValue = data[referencePoint[i + 1]]
        k = (secondValue - firstValue)*1.0 / (secondDate - firstDate)
        for j in range(firstDate + 1, secondDate):
            data[j] = (j - firstDate)*k + firstValue
            
    for i in range(0, 1000, 20):
        changePoint = i + random.randint(0, 20)
        if changePoint < len(data):
            positive = random.randint(0, 1)
            value = random.randint(50, 300)
            if positive:
                data[changePoint] += value
            else:
                data[changePoint] -= value
            referencePoint.append(changePoint)
    referencePoint.sort()
    print referencePoint
    
    print '[getLine] - Begin to generate the curve based on the second reference points'
    for i in range(len(referencePoint) - 1):
        firstDate = referencePoint[i]
        firstValue = data[referencePoint[i]]
        secondDate = referencePoint[i + 1]
        secondValue = data[referencePoint[i + 1]]
        k = (secondValue - firstValue)*1.0 / (secondDate - firstDate)
        for j in range(firstDate + 1, secondDate):
            data[j] = (j - firstDate)*k + firstValue

    print '[getLine] - All data is updated'
    return data
    
def addVibration(data):
    for i in range(0, 1000):
        positive = random.randint(0, 1)
        value = random.randint(1, 10)
        if positive:
            data[i] += value
        else:
            data[i] -= value
    print '[addVibration] - Finish adding the grand vibration'
    return data
    
def getData():
    data = getModel(1)
    data = getLine(data)
    data = addVibration(data)
    return data

def getShare(data, interval):
    number = 1000/interval
    each = 10000.0/number
    share = 0
    
    for i in range(number):
        share += each / data[i*interval]
    print 'With the interval: ', interval, '. We will get ', share, ' in total'
    return share
    
def getGain():
    interval = 15
    data = getData();
    saveData(data)
    
    share = getShare(data, interval)
    gain = data[-1]*share
    rate = gain/10000.0
    
    print 'The gain rate is: ', rate

def saveData(data):
    if not os.path.isfile('data.txt'):
        target = open('data.txt','w')
    else:
        os.remove('data.txt')
        target = open('data.txt','w')
               
    for i in range(len(data)):
        target.write(str(data[i]))
        target.write('\n')

if __name__ == "__main__":
    getGain()



