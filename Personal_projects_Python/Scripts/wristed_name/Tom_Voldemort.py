# -*- coding: utf-8 -*-
'''
当时看完西部世界发现里面两个人的名字是同样字母重新排列的，所以写了这么一个脚本来比较两个
名字的相似度，名字来源于哈利波特中的汤姆里德尔
还有两个txt文件中是常见的姓和名，用于寻找一个打乱顺序的名字
'''

from progressbar import *
import os

# 将输入的字符串变成一个各个字母出现数字的dic
def pretreatment(name):
    name = name.lower()
    target = ''
    for one in name.split(' '):
        target += one
    target_dic = {}
    for one in target:
        if one in target_dic:
            target_dic[one] += 1
        else:
            target_dic[one] = 1
    # print target_dic
    return target_dic

# 比较dic，得出相似度
def compare(name1, name2):
    base = max(sum(name1.values()), sum(name2.values()))
    # print base
    bias = 0
    total_diff = 0
    for one in name1.keys():
        if one in name2.keys():
            bias += abs(name1[one] - name2[one])
        else:
            total_diff += name1[one]
    for one in name2.keys():
        if one in name1.keys():
            pass
        else:
            total_diff += name2[one]
    bias += float(total_diff) / 2 # 注意这里需要/2，不然不同的地方就算了两次
    # print bias
    return int((1 - float(bias)/base)*100)  # 注意这里必须要将bias或base其中一个变成float，不然算出来的不是一个小数

# 用于输入两个名字并计算相似度    
def find_resemblance():
    name1 = raw_input('The first name?\n')
    name1 = pretreatment(name1)
    name2 = raw_input('The second name?\n')
    name2 = pretreatment(name2)
    res = compare(name1, name2)
    print 'The resemblance of these two names is ', res, '%' 

# 用于把txt文件中男性名字提取出来
def extract_first_name_m():
    list_first_name_m = []
    for line in open('first_name.txt', 'r'):
        words = line.split('\t')
        if words[0] == 'women\n':            
            return list_first_name_m
        else:    
            if words[0] == '\n':
                continue
            else:
                list_first_name_m.append(words[0])

# 用于把txt文件中女性名字提取出来
def extract_first_name_f():                     
    list_first_name_f = []
    flag_start = 0
    for line in open('first_name.txt', 'r'):
        words = line.split('\t')
        if words[0] == 'women\n' and flag_start == 0:            
            flag_start = 1
            continue   
        if flag_start == 0:
            continue
        else:
            if words[0] == '\n':
                continue
            else:
                list_first_name_f.append(words[0])
    return list_first_name_f
    
# 用于把txt文件中姓提取出来    
def extract_second_name():
    list_second_name = []
    for line in open('second_name.txt', 'r'):
        words = line.split('\t')    
        if words[0] == '\n':
            continue
        else:
            list_second_name.append(words[0])
    return list_second_name
 
#用于找到和输入名字和给定相似度匹配的常见名字 
def find_name():
    potential_f = []
    given_name = raw_input('The name?\n')
    given_resemblence = int(raw_input('The resemblance you want?\n'))
    while given_resemblence > 100 or given_resemblence < 0:
        print 'The resemblance should be between 0 and 100...'
        given_resemblence = int(raw_input('The resemblance you want?\n'))
        
    potential_m = search_name_m( given_name, given_resemblence)
    potential_f = search_name_f( given_name, given_resemblence) 
    
    delete_too_favor(given_name, potential_m)
    delete_too_favor(given_name, potential_f)
    
    print '\n'
    if len(potential_m) == 0:
        print 'Sorry, no possible male names...'
    else:
        print 'Possible male names are:'
        for one in potential_m:
            print one

    print '\n'            
    if len(potential_f) == 0:
        print 'Sorry, no possible female names...'
    else:
        print 'Possible female names are:'
        for one in potential_f:
            print one
    
# 找到可能的男性姓名
def search_name_m( given_name, given_resemblence):
    i = 0
    potential_m = []
    list_first_m = extract_first_name_m()
    list_second = extract_second_name()
    print '\n'
    print 'Searching for the potential male names, please wait....'
    
    pbar_m = ProgressBar().start()    
    for first in list_first_m:
        for second in list_second:
            i += 1
            pbar_m.update(int(i / float(600000) * 100))
            res = compare(pretreatment(given_name), pretreatment(first+second))
            if res >= given_resemblence:
                name = first + " " + second 
                potential_m.append(name)
    pbar_m.finish()    
    return potential_m

# 找到可能的女性姓名
def search_name_f( given_name, given_resemblence):
    i = 0
    potential_f = []
    list_first_f = extract_first_name_f()
    list_second = extract_second_name()
    print '\n'
    print 'Searching for the potential female names, please wait....'
    
    pbar_f = ProgressBar().start()    
    for first in list_first_f:
        for second in list_second:
            i += 1
            pbar_f.update(int(i / float(600000) * 100))
            res = compare(pretreatment(given_name), pretreatment(first+second))
            if res >= given_resemblence:
                name = first + " " + second 
                potential_f.append(name)
    pbar_f.finish()
    return potential_f

# 用于剔除过于相似的结果 
def delete_too_favor(name, list):
    name = name.upper()
    names = name.split(' ')
    name = ''
    for one in names:
        name += one
    list_remove = [] # 注意这里要建立一个list储存要删去的元素，不能直接在循环里删除list中的元素
    for i in range(0, len(name) - 2):
        for one in list:
            if name[i:i+3] in one:
                if one not in list_remove:  # 要确认每个元素是唯一的
                    list_remove.append(one)
            else:
                pass
    for one in list_remove:
        list.remove(one)
    return
    
if __name__ == '__main__':
    choice = ''
    while('resem' not in choice and 'name' not in choice):
        choice = raw_input('You want to find the resemblance of two names or find the resemblant names? Tap ''resemblance'' or ''name'' to choose\n')
    if 'resemblance' in choice: 
        find_resemblance()
    else:
        find_name()
    
    
    
    