# -*- coding: utf-8-*- 
import win32com.client as win32
import os
 
class easyExcel: 
    """A utility to make iteasier to get at Excel.  Remembering 
    to save the data is your problem, asis  error handling. 
    Operates on one workbook at atime.""" 
    
    def __init__(self, filename = None): 
        self.App = win32.gencache.EnsureDispatch('Excel.Application')
        # self.App.Visible = True  # debug mode
        self.path = os.getcwd()
        if filename: 
            if os.path.isfile(filename):
                self.filename = filename 
                filepath = os.join.path(os.getcwd(), filename)
                self.xlBook = self.App.Workbooks.Open(filepath) 
            else:
                print 'This file does not exist'
                self.App.Application.Quit()
        else: 
            self.xlBook = self.App.Workbooks.Add() 
            self.filename = ''  
            
    def save(self, newfilename = None): 
        if newfilename: 
            self.filename = newfilename 
            filePath = os.path.join(self.path, self.filename)
            self.xlBook.SaveAs(filePath) 
        else: 
            self.xlBook.Save()   
            
    def close(self): 
        # self.xlBook.Close(SaveChanges = 0) 
        self.xlBook.Close() 
        self.App.Application.Quit()

    def getCell(self, row, col, sheet = None): 
        """Get value of one cell""" 
        if sheet:
            try:
                mySheet = self.xlBook.Worksheets(sheet)
            except:
                print 'No this ' + sheet + ' in this file'
                return ''
        else:
            try:
                mySheet = self.xlBook.Worksheets("Sheet1")
            except:
                print 'No sheet1 in this file, please give one'
                
        return mySheet.Cells(row, col).Value 
        
    def setCell(self, row, col, value, sheet = None): 
        """set value of one cell"""
        if sheet:
            try:
                mySheet = self.xlBook.Worksheets(sheet)
            except:
                print 'No this ' + sheet + ' in this file'
        else:
            try:
                mySheet = self.xlBook.Worksheets("Sheet1")
            except:
                print 'No sheet1 in this file, please give one'
                
        mySheet.Cells(row, col).Value = value 
        
    def getRange(self, row1, col1, row2, col2, sheet = None): 
        """return a 2d array (i.e. ((xx, xx), (xx, xx)))"""
        if sheet:
            try:
                mySheet = self.xlBook.Worksheets(sheet)
            except:
                print 'No this ' + sheet + ' in this file'
                return ''
        else:
            try:
                mySheet = self.xlBook.Worksheets("Sheet1")
            except:
                print 'No sheet1 in this file, please give one'
                return ''
                
        return mySheet.Range(mySheet.Cells(row1, col1), mySheet.Cells(row2, col2)).Value 
        
        
if __name__ =="__main__": 
    test = easyExcel()
    test.setCell(1, 1, 1, 'Feuil1')
    test.setCell(2, 1, 'ok', 'Feuil1')
    test.save('test.xlsx') 
    test.close()
    print 'All done, enjoy!'
    