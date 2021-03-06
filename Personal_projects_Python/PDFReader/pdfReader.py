# -*- coding: utf-8 -*-   
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import *
from pdfminer.converter import PDFPageAggregator
import os
import re
    
def testMode(filename):
    fp = open(filename, 'rb')
    #来创建一个pdf文档分析器
    parser = PDFParser(fp)  
    #创建一个PDF文档对象存储文档结构
    document = PDFDocument(parser)
    # 检查文件是否允许文本提取
    if not document.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:
        # 创建一个PDF资源管理器对象来存储共赏资源
        rsrcmgr = PDFResourceManager()
        # 设定参数进行分析
        laparams = LAParams()
        # 创建一个PDF设备对象
        # device=PDFDevice(rsrcmgr)
        device = PDFPageAggregator(rsrcmgr, laparams = laparams)
        # 创建一个PDF解释器对象
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        # 处理每一页
        for page in PDFPage.create_pages(document):
            interpreter.process_page(page)
            # 接受该页面的LTPage对象
            layout = device.get_result()
            for x in layout:
                # if(isinstance(x, LTTextLine)):
                    # print 'bingo'
                    # data = x.get_text().encode('utf-8')
                    # with open('testRecord.txt', 'a') as f:
                        # f.write(data + '\n')
                print x
                if(isinstance(x, LTTextBoxHorizontal)):
                    print 'ok'
                    data = x.get_text().encode('utf-8')
                    with open('testRecord.txt', 'a') as f:
                        f.write(data + '\n')
                

                
def parsePDF(filename):
    fp = open(filename, 'rb')
    #来创建一个pdf文档分析器
    parser = PDFParser(fp)  
    #创建一个PDF文档对象存储文档结构
    document = PDFDocument(parser)
    # 检查文件是否允许文本提取
    if not document.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:
        # 创建一个PDF资源管理器对象来存储共赏资源
        rsrcmgr=PDFResourceManager()
        # 设定参数进行分析
        laparams=LAParams()
        # 创建一个PDF设备对象
        # device=PDFDevice(rsrcmgr)
        device=PDFPageAggregator(rsrcmgr,laparams=laparams)
        # 创建一个PDF解释器对象
        interpreter=PDFPageInterpreter(rsrcmgr,device)
        # 处理每一页
        result = []
        for page in PDFPage.create_pages(document):
            pageResult = parsePage(page, interpreter, device, filename)
            result.append(pageResult)
        return result
           
def parsePage(page, interpreter, device, filename):           
    date = ''
    valueMax = 0
    interpreter.process_page(page)
    # 接受该页面的LTPage对象
    layout = device.get_result()
    for x in layout:
        # if(isinstance(x,LTTextBoxHorizontal) and ('￥' in x.get_text().encode('utf-8'))):
        if (isinstance(x, LTTextBoxHorizontal)):
            info = x.get_text().encode('utf-8')

            value = valueMatchPattern(info)
            if (value > valueMax):
                valueMax = value
                continue
                
            elif (date != 'confuse'):
                dateTemp = dateMatchPattern(info, filename)
                if dateTemp and date:
                    print 'We find more than one date in this file ', filename
                    date = 'confuse'
                elif not date:
                    date = dateTemp
                   
    if not valueMax or not date or date == 'confuse':
        print 'In file ' + getLastAddress(filename) 
        if not valueMax:
            print 'No price found!'
        if not date:
            print 'No date found!' 
        if date == 'confuse':
            print 'Have found more than one date'
        print '*****************************\n'
        
    return [date, valueMax]    

def getValue(info):
    number = '0123456789.'
    onlyNumber = info
    for one in onlyNumber:
        if one not in number:
            onlyNumber = onlyNumber.replace(one, '')
    value = float(onlyNumber)
    return value
    
def valueMatchPattern(info):
    value = 0
    if '￥' in info or '¥' in info:
        value = getValue(info)
    else:
        valueInfo = re.findall('\d+\.\d\d$', info)
        if (len(valueInfo) == 1):
            value = float(valueInfo[0])
    return value
        
def dateMatchPattern(info, filename):
    if ('年' in info and '月' in info and '日' in info):
        return getDate(info, 1, filename)
    else:
        numberMatch = re.findall('\d+', info)  # seperate the number from the space or special char
        if len(numberMatch) >= 3:
            info = '/'.join(one for one in numberMatch)
            return getDate(info, 2, filename) 
        else:
            return ''
        
def getDate(info, pattern, filename):
    date = ''
    if (pattern == 1):
        allInfo = info.split('\n')
        fullDate = ''
        for one in allInfo:
            if ('年' in one and '月' in one and '日' in one):
                fullDate = one
                
            if fullDate:
                if (len(fullDate) == 17):
                    date = fullDate[0:4] + '/' + fullDate[7:9] + '/' + fullDate[12:14]
                else:
                    date = fullDate
                    print 'In file ' + getLastAddress(filename) + ' the date format is unusual, can not converter'
                    print '*****************************\n'
                    # some lesson
                    # print date.index('年')
                    # print date.index('月')
                    # print date.index('日')
                    # date.replace('年', '/')
                    # date.replace('月', '/')
                    # date.replace('日', '')
                    # 没法直接这么替换，utf-8中中文和数字占用的字节数不一样，
                    # 也没法遍历然后替换不然会有3个'/', 直接数字节替换比较方便
                    
    elif (pattern == 2):
        match = re.findall('20\d\d/\d\d/\d\d', info)
        if not match:
            date = ''
        elif len(match) == 1:
            date = match[0]
        else:
            date = 'confuse'
            
    return date
        
def getLastAddress(path):
    allInfo = path.split('\\')
    return allInfo[-1]
    
if __name__ =="__main__": 
    # parsePDF('taxi1.pdf')
    testMode('6.5_6.10.pdf')
    
    print 'All done, enjoy!'
    
    
    
    
    
    
    
    
    
    
    
    