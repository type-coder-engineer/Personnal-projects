#coding: utf
import os

# 找到所有磁盘
def findDrives():
    driveList = []
    for drive in range(ord('A'), ord('N')):
        if os.path.exists(chr(drive) + ':'):
            driveList.append(chr(drive)+":\\")
    return driveList

# 在磁盘中找目标文件
def iterateFiles(directory):
    if not os.path.isdir(directory):
        return []
    formList = ['doc', 'txt', 'xls', 'xlsx', 'ppt', 'pdf', 'jpg', 'png']
    result = []
    for root, dirs, files in os.walk(directory, topdown = True):
        for file in files:
            for one in formList:
                if one in file.split('.')[-1]:
                    result.append(os.path.join(root, file))
                    break
    return result

# 返回所有目标文件的路径
def findFiles():
    allDrives = findDrives()
    allTargets = []
    for drive in allDrives:
        allTargets += iterateFiles(drive)
    return allTargets
    
def findFilesFromHere():
    path = os.getcwd()
    allTargets = iterateFiles(path)
    return allTargets
    
# if __name__ == '__main__':
    # print findFilesFromHere()
    