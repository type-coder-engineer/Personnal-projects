# -*-coding: utf-8 -*-
import random
import os
import matplotlib.pyplot as plt

def getModel(type):
    data = []
    for i in range(1000):
        data.append(0)
        
    # 平稳上涨    
    if type == 1: 
        data[0] = 2000
        data[100] = 2500
        data[200] = 2700
        data[300] = 3400
        data[400] = 3300
        data[500] = 4000
        data[699] = 4100
        data[700] = 4000
        data[800] = 4600
        data[900] = 4700
        data[999] = 5000
      
    # 波动上涨      
    elif type == 2:
        data[0] = 2000
        data[100] = 1600
        data[200] = 2100
        data[300] = 2900
        data[400] = 2600
        data[500] = 3300
        data[699] = 3400
        data[700] = 3000
        data[800] = 4000
        data[900] = 3600
        data[999] = 4400
        
    # 倒U形
    elif type == 3:
        data[0] = 2000
        data[100] = 2400
        data[200] = 2800
        data[300] = 3000
        data[400] = 3600
        data[500] = 4200
        data[699] = 4400
        data[700] = 4300
        data[800] = 3400
        data[900] = 3300
        data[999] = 3500
        
    # 正U形
    elif type == 4:
        data[0] = 3000
        data[100] = 2800
        data[200] = 2600
        data[300] = 2700
        data[400] = 2200
        data[500] = 2100
        data[699] = 2100
        data[700] = 2600
        data[800] = 2500
        data[900] = 2900
        data[999] = 3100
     
    # S形上涨
    elif type == 5:
        data[0] = 2000
        data[100] = 2400
        data[200] = 2600
        data[300] = 2700
        data[400] = 2400
        data[500] = 2200
        data[699] = 2100
        data[700] = 2600
        data[800] = 2700
        data[900] = 3000
        data[999] = 3100
       
    # S形下跌
    elif type == 6:
        data[0] = 2000
        data[100] = 2500
        data[200] = 3100
        data[300] = 2900
        data[400] = 2400
        data[500] = 1800
        data[699] = 1500
        data[700] = 1400
        data[800] = 1500
        data[900] = 1900
        data[999] = 1800

    return data

def getLine(data):
    referencePoint = []
    for i in range(len(data)):
        if data[i] != 0:
            referencePoint.append(i)
    if (len(referencePoint) < 2):
        print '[getLine] - Something wrong with this data, no reference point'
        
    # print '[getLine] - Begin to generate the curve based on the first reference points'
    for i in range(len(referencePoint) - 1):
        firstDate = referencePoint[i]
        firstValue = data[referencePoint[i]]
        secondDate = referencePoint[i + 1]
        secondValue = data[referencePoint[i + 1]]
        k = (secondValue - firstValue)*1.0 / (secondDate - firstDate)
        for j in range(firstDate + 1, secondDate):
            data[j] = (j - firstDate)*k + firstValue
            
    for i in range(0, 1000, 20):
        changePoint = i + random.randint(1, 20)
        if changePoint < len(data):
            positive = random.randint(0, 1)
            value = random.randint(50, 200)
            if positive:
                data[changePoint] += value
            else:
                data[changePoint] -= value
            referencePoint.append(changePoint)
    referencePoint.sort()
    # print referencePoint
    
    # print '[getLine] - Begin to generate the curve based on the second reference points'
    for i in range(len(referencePoint) - 1):
        firstDate = referencePoint[i]
        firstValue = data[referencePoint[i]]
        secondDate = referencePoint[i + 1]
        secondValue = data[referencePoint[i + 1]]
        if (secondDate != firstDate):
            k = (secondValue - firstValue)*1.0 / (secondDate - firstDate)
        else:
            continue
        for j in range(firstDate + 1, secondDate):
            data[j] = (j - firstDate)*k + firstValue

    # print '[getLine] - All data is updated'
    return data
    
def addVibration(data):
    for i in range(0, 1000):
        positive = random.randint(0, 1)
        value = random.randint(1, 20)
        if positive:
            data[i] += value
        else:
            data[i] -= value
    # print '[addVibration] - Finish adding the grand vibration'
    return data
    
def getData(model):
    data = getModel(model)
    data = getLine(data)
    data = addVibration(data)
    return data

def getShare(data, interval):
    number = 1000/interval
    each = 10000.0/number
    share = 0
    
    for i in range(number):
        share += each / data[i*interval]
    # print 'With the interval: ', interval, '. We will get ', share, ' in total'
    return share
    
def getGain(interval, model):
    data = getData(model)    
    share = getShare(data, interval)
    gain = data[-1]*share
    rate = gain/10000.0
    # print 'The gain rate is: ', rate
    return rate
    
def saveAndCompare():    
    for model in range(1, 7):
        print 'Begin to compare the data type ', model, ' with different interval\n'
        interval = 2
        for i in range(1, 8):
            interval *= 2
            gainList = []
            for j in range(1000):
                gain = getGain(interval, model)
                gainList.append(gain)
            gainList.sort()
            average = 0
            for number in gainList:
                average += number
            average /= len(gainList)
            print 'When interval is: ', interval, ', min gain is: ', gainList[0], ', max gain is: ', gainList[-1], ', and average value is: ', average, '\n'
        print '****************************************\n'
        
    print 'Finish comparing all the data'
    
def saveData(data):
    if not os.path.isfile('data.txt'):
        target = open('data.txt','w')
    else:
        os.remove('data.txt')
        target = open('data.txt','w')
               
    for i in range(len(data)):
        target.write(str(data[i]))
        target.write('\n')
        
def showData():
    data = getData(6)
    x = range(len(data))
    y = data
    plt.plot(x, y)
    plt.title('data')
    plt.xlabel('time')
    plt.ylabel('value')
    plt.show()

if __name__ == "__main__":
    showData()
    # getGain(15)
    # saveAndCompare()


