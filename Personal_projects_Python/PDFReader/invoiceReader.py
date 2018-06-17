# -*- coding: utf-8 -*-   

from pdfReader import *
from easyExcel import *

def treatInvoice(path):
    if (os.path.isfile('expense.xlsx')):
        os.remove('expense.xlsx')
    expenseFile = easyExcel()
    row = 1
    print 'Initialize the Excel file, begin to parse the files'
    for root, dirs, files in os.walk(path):
        for file in files:
            fileType = getLastAddress(root)
            if ('.pdf' in file):
                filePath = os.path.join(root, file)
                allPages = parsePDF(filePath)
                if (fileType == 'hotel'):
                    column = 4
                elif (fileType == 'taxi'):
                    column = 6
                else:
                    column = 8
                for page in allPages:
                    expenseFile.setCell(row, 1, page[0], 'Feuil1')
                    expenseFile.setCell(row, column, page[1], 'Feuil1')
                    expenseFile.setCell(row, 12, page[1], 'Feuil1')
                    row += 1
            # else:
                # print file + ' in ' + fileType + ' is not a pdf'
    expenseFile.save('expense.xlsx') 
    expenseFile.close()

if __name__ == '__main__':
    path = os.getcwd()
    treatInvoice(path)
    print 'All done, enjoy!'