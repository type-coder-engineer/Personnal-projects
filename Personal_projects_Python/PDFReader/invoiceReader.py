# -*- coding: utf-8 -*-   

from pdfReader import *
from easyExcel import *

def treatInvoice(path):
    if (os.path.isfile('expense.xlsx')):
        os.remove('expense.xlsx')
    expenseFile = easyExcel()
    row = 1
    print 'Initialize the Excel file, begin to parse the files\n'
    lastClass = ''
    dictClass = {}
    noKeyCount = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            fileType = getLastAddress(root)
            if not lastClass:
                lastClass = fileType
                print 'Now we are parsing the ' + fileType + ' invoices\n'
                
            if (lastClass != fileType):
                if (lastClass == 'hotel'):
                    column = 4
                elif (lastClass == 'taxi'):
                    column = 6
                else:
                    column = 8                
                
                allKeys = dictClass.keys()
                allKeys.sort()  # 这里需要赋值一下然后sort()
                for one in allKeys:
                    info = dictClass[one]
                    expenseFile.setCell(row, 1, info[0], 'Feuil1')
                    expenseFile.setCell(row, column, info[1], 'Feuil1')
                    expenseFile.setCell(row, 12, info[1], 'Feuil1')
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
                    
            # else:
                # print file + ' in ' + fileType + ' is not a pdf'
    if dictClass:
        if (lastClass == 'hotel'):
            column = 4
        elif (lastClass == 'taxi'):
            column = 6
        else:
            column = 8  
                    
        allKeys = dictClass.keys()
        allKeys.sort()
        for one in allKeys:
            info = dictClass[one]
            expenseFile.setCell(row, 1, info[0], 'Feuil1')
            expenseFile.setCell(row, column, info[1], 'Feuil1')
            expenseFile.setCell(row, 12, info[1], 'Feuil1')
            row += 1
            
    expenseFile.save('expense.xlsx') 
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

if __name__ == '__main__':
    path = os.path.join(os.getcwd(), 'expense claim 009')
    treatInvoice(path)
    print 'All done, enjoy!'
    
    
    
    
    
    