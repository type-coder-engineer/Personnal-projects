# -*- coding: utf-8 -*-   

from pdfReader import *
from easyExcel import *
import datetime

def treatInvoice(path):
    expensePath = getLastAddress(path)
    filename = expensePath + '.xlsx'
    if (os.path.isfile(filename)):
        os.remove(filename)
    expenseFile = easyExcel()
    print 'Initialize the Excel file, begin to write the header\n'
    row = writeHeader(expenseFile, expensePath)
    if not row:
        print 'Not able to write in the excel file, please check the language, only available with English and French for now'
        return
    else:
        beginRow = row
    print 'Begin to parse the invoices files\n'
    lastClass = ''
    dictClass = {}
    noKeyCount = 0
    columnLetter = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    
    for root, dirs, files in os.walk(path):
        for file in files:
            fileType = getLastAddress(root)
            if not lastClass:
                lastClass = fileType
                if (fileType != expensePath):
                    print 'Now we are parsing the ' + fileType + ' invoices'
                
            if (lastClass != fileType):
                column = getColumn(lastClass)             
                
                allKeys = dictClass.keys()
                allKeys.sort()  # 这里需要赋值一下然后sort()
                for one in allKeys:
                    info = dictClass[one]
                    writeToCell(expenseFile, row, 1, info[0])
                    writeToCell(expenseFile, row, column, info[1])
                    equalBlanks = '=' + columnLetter[column - 1] + str(row)
                    writeToCell(expenseFile, row, 11, equalBlanks)
                    row += 1

                lastClass = fileType
                dictClass = {}
                noKeyCount = 0
                print 'Now we are parsing the ' + fileType + ' invoices\n'
                
            if ('.pdf' in file):
                filePath = os.path.join(root, file)
                allPages = parsePDF(filePath)
                for page in allPages:
                    result = getDateKey(page[0], noKeyCount, dictClass)
                    noKeyCount = result[1]
                    dictClass[result[0]] = page
            else:
                if (fileType != expensePath):
                    print file + ' in ' + fileType + ' is not a pdf file'
                    print '*****************************\n'
                
    if dictClass:
        column = getColumn(lastClass)
                    
        allKeys = dictClass.keys()
        allKeys.sort()
        for one in allKeys:
            info = dictClass[one]
            writeToCell(expenseFile, row, 1, info[0])
            writeToCell(expenseFile, row, column, info[1])
            equalBlanks = '=' + columnLetter[column - 1] + str(row)
            writeToCell(expenseFile, row, 11, equalBlanks)
            row += 1

    print 'Begin to resume all the sub total\n'            
    writeEnder(expenseFile, beginRow, row)

    expenseFile.save(filename)
    expenseFile.close()
    
def getDateKey(date, noKeyCount, dictClass):
    if (len(date) == 10):
        fullDate = date.split('/')
        key = int(fullDate[1])*31 + int(fullDate[2])
        while(key in dictClass.keys()):
            key += 0.01
    else:
        key = -noKeyCount
        noKeyCount = noKeyCount + 1
    return [key, noKeyCount]

def writeToCell(file, row, column, info):
    for i in range(2):
        try:
            file.setCell(row, column, info, 'Feuil1')
            return 1
        except:
            print ''
        
        try:
            file.setCell(row, column, info, 'Sheet1')
            return 1
        except:
            print ''
    return 0
       
def writeHeader(file, expensePath):
    row = 1
    res = writeToCell(file, row, 5, 'Altios China')
    if not res:
        return 0
    row += 1
    writeToCell(file, row, 5, expensePath)
    row += 2
    writeToCell(file, row, 1, 'Form No')
    currentYear = datetime.datetime.now().strftime('%Y')
    formNb = 'BAL' + currentYear[-2:] + '0' + expensePath[-2:]
    writeToCell(file, row, 2, formNb)

    writeToCell(file, row, 4, 'Date')
    currentDate = datetime.datetime.now().strftime('%Y-%m-%d')
    writeToCell(file, row, 5, currentDate)
    row += 2
    
    writeToCell(file, row, 1, 'Date')
    writeToCell(file, row, 2, 'City')
    writeToCell(file, row, 3, 'Client')
    writeToCell(file, row, 4, 'Hotel')
    writeToCell(file, row, 5, 'Taxi')
    writeToCell(file, row, 6, 'Plane')
    writeToCell(file, row, 7, 'Train')
    writeToCell(file, row, 8, 'Telephone')
    writeToCell(file, row, 9, 'Restaurant')
    writeToCell(file, row, 10, 'Others')
    writeToCell(file, row, 11, 'Total in RMB')
    row += 2
    return row
    
def writeEnder(file, beginRow, row):
    columnLetter = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    endRow = row - 1
    row += 1
    
    writeToCell(file, row, 1, 'Sub total')
    for column in range(4, 12):
        subTotal = '=SOMME(' + columnLetter[column - 1] + str(beginRow) + ':'  + columnLetter[column - 1] + str(endRow) + ')'
        writeToCell(file, row, column, subTotal)
        
    equalBlanks = '=' + columnLetter[10] + str(row)
    row += 2
    
    writeToCell(file, row, 10, 'Total due')
    writeToCell(file, row, 11, equalBlanks)

def getColumn(itemClass):
    if (itemClass == 'hotel'):
        column = 4
    elif (itemClass == 'taxi'):
        column = 5
    elif (itemClass == 'plane'):
        column = 6
    elif (itemClass == 'train'):
        column = 7
    elif (itemClass == 'telephone'):
        column = 8
    elif (itemClass == 'restaurant'):
        column = 9
    else:
        column = 10
    return column

if __name__ == '__main__':
    path = os.path.join(os.getcwd())
    treatInvoice(path)
    raw_input('All done, enjoy! Press any key to continue')
    
    
    
    
    
    