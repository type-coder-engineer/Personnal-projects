#coding: utf-8
from PyPDF2 import PdfFileMerger
import os, sys, time

def mergeTarget(targets, name):
    path = os.getcwd()
    allFile = os.listdir(path)
    mergeFile = PdfFileMerger()
    if '.pdf' not in name:
        pdfOutput = name + '.pdf'
    else:
        pdfOutput = name
    if pdfOutput in allFile:
        targets.append(pdfOutput)
        print 'Final target name "{}" already exists'.format(pdfOutput)
        pdfOutput = 'merged-' + time.strftime('%Y%m%d-%H%M%S') + '.pdf'
        print 'So the target is saved by the name "{}"'.format(pdfOutput)
            
    index = 0
    for file in targets:
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

def mergeAll(name):
    path = os.getcwd()
    allFile = os.listdir(path)
    mergeFile = PdfFileMerger()
    if '.pdf' not in name:
        pdfOutput = name + '.pdf'
    else:
        pdfOutput = name
    if pdfOutput in allFile:
        print 'Final target name "{}" already exists'.format(pdfOutput)
        answer = ''
        while(answer != 'yes' and answer != 'no'):
            answer = raw_input('Want to proceed and replace this target with the merged file? tap "yes" or "no"\n')
        if answer == 'no':
            pdfOutput = 'merged-' + time.strftime('%Y%m%d-%H%M%S') + '.pdf'
            print 'Ok the target is saved by the name "{}" then'.format(pdfOutput)
    
    index = 0
    for file in allFile:
        if '.py' not in file: # 防止重复merge
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
    if len(sys.argv) < 3:
        print 'Wrong input, the standard input is either "python PDFMergeHelper.py pdfname... targetName" or "python PDFMergeHelper.py all targetName"' 
        exit()
    if sys.argv[1] == 'all':
        mergeAll(sys.argv[2])
    else:
        mergeTarget(sys.argv[1:-1], sys.argv[-1])
        
        
        