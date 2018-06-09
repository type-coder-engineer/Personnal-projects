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
import os, sys

# fp = open('taxi1.pdf', 'rb')
# if (os.path.exists('testPDF.txt')):
    # os.remove('testPDF.txt')
    
def parsePDF(filename, recordFile):
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
        for page in PDFPage.create_pages(document):
            flagDate  = 0;
            flagValue = 0;
            valueMax  = 0;
            interpreter.process_page(page)
            # 接受该页面的LTPage对象
            layout = device.get_result()
            for x in layout:
                # if(isinstance(x,LTTextBoxHorizontal) and ('￥' in x.get_text().encode('utf-8'))):
                if(isinstance(x,LTTextBoxHorizontal)):
                    info = x.get_text().encode('utf-8')
                    if ('￥' in info):
                        flagValue = 1;
                        number = '0123456789.'
                        onlyNumber = info
                        for one in onlyNumber:
                            if one not in number:
                                onlyNumber = onlyNumber.replace(one, '')
                        value = float(onlyNumber)
                        if (value > valueMax):
                            valueMax = value
                        continue
                    elif ('年' in info and '月' in info and '日' in info):
                        flagDate = 1
                        number = '0123456789'
                        allInfo = info.split('\n')
                        date = ''
                        for one in allInfo:
                            if ('年' in one and '月' in one and '日' in one):
                                date = one
                                break
                        if (not date):
                            print 'Problem in this file'
                        else:
                            if (len(date) == 17):
                                date = date[0:4] + '/' + date[7:9] + '/' + date[12:14]
                            else:
                                print 'This date format is unusual, do not converter'
                            # print date.index('年')
                            # print date.index('月')
                            # print date.index('日')
                            # date.replace('年', '/')
                            # date.replace('月', '/')
                            # date.replace('日', '')
                            # 没法直接这么替换，utf-8中中文和数字占用的字节数不一样，
                            # 也没法遍历然后替换不然会有3个'/', 直接数字节替换比较方便

                        with open(recordFile, 'a') as f:
                            f.write(date + '\n')
            
            if (flagDate and flagValue):
                with open(recordFile, 'a') as f:
                    f.write('price: ' + str(valueMax) + '\n\n')
                # print 'Successful!\n'
            else:
                print 'Can not treat file ' + getType(filename)
                if (not flagDate):
                    print 'No date found!'  
                if (not flagValue):
                    print 'No price found!'
                print '*****************************\n'
                
def getType(path):
    allInfo = path.split('\\')
    return allInfo[-1]
    
def treatFile(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            fileType = getType(root)
            recordFile = fileType + '.txt'
            if ('.pdf' in file):
                # print file
                filePath = os.path.join(root, file)
                parsePDF(filePath, recordFile)
    
if __name__ == '__main__':
    if (sys.argv == 3):
        path = os.getcwd()
    else:
        path = os.getcwd()
    treatFile(path)
    print 'All done, enjoy!'
    
    
    
    
    
    
    
    
    
    
    
    
    