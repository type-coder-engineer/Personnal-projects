#coding: utf-8
from PyPDF2 import PdfFileMerger
import os, sys

def mergeAll(name):
    path = os.getcwd()
    allFile = os.listdir(path)
    mergeFile = PdfFileMerger()
    if '.pdf' not in name:
        pdfOutput = name + '.pdf'
    else:
        pdfOutput = name
        
    index = 0
    for file in allFile:
        if '.py' not in file and file != pdfOutput: # 防止重复merge
            try:
                target = open(file, 'rb')
                mergeFile.append(target)
                index += 1
            except:
                print 'Wrong with the file "{}"'.format(file)
    target.close()
    output = open(pdfOutput, 'wb')
    mergeFile.write(output)
    mergeFile.close()
    print 'You have merged {} PDF files'.format(index)
    print 'All done!'
    
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Wrong input, the standard input is python PDFMergeHelper.py targetName'
        exit()
    mergeAll(sys.argv[1])