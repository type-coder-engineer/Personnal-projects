# coding:utf-8
# 用于背单词的小程序，可以将单词本中不认识的单词整理到一个resume.txt的文件中去

import sys, os

# 读取单词文件
def read_file(filename):
    word_dic = {}
    if not os.path.isfile(filename):
        print 'Sorry this file doesn\'t exist...'
        return
    file_to_read = open(filename,'r')
    lines = file_to_read.readlines()
    for line in lines:
        # print line
        words = line.split(' ')
        word = words[0]
        # print word
        explanation = ' '.join(words[1:])
        # print explanation
        word_dic[word] = explanation
        # raw_input()
    file_to_read.close()
    return word_dic

# 将不懂的单词保存到文件中
def save_file(words_to_save):
    if len(words_to_save) == 0:
        return
        
    words_exist = []
    if not os.path.isfile('resume.txt'):
        target = open('resume.txt','w')
    else:
        target = open('resume.txt','r')
        lines = target.readlines() 
        for line in lines:
            words = line.split(' ') # 这里不是空格而要用\t,因为下面52行里面你自己加的就是\t，要保持一致,同理如果下面你用的是' '那么这里也是' '
            words_exist.append(words[0])
        target.close()
                
        target = open('resume.txt','a')
        target.write('\n')
        
    # print words_exist 
       
    for word in words_to_save.keys():
        if word in words_exist:
            continue
        else:
            target.write(word)
            target.write(' ')
            target.write(words_to_save[word])
            target.write('\n')
            
    target.close()
       
# 测试单词
def test_words(word_dic):
    # print word_dic
    # raw_input()
    total = len(word_dic)
    progress = 0
    words_to_save = {}
    
    for one in word_dic.keys(): 
        progress += 1           
        choice = ''
        while choice != 'n' and choice != 'y':
            clear()
            print '%d / %d' %(progress, total)
            choice = raw_input(one + '\n')
            
        if choice == 'n':
            clear()
            print '%d / %d' %(progress, total)
            print one
            print '\n'
            raw_input(word_dic[one].strip('\n') + '\n')
            words_to_save[one] = word_dic[one].strip('\n')
        else:
            choice = ''
            while choice != 'n' and choice != 'y':
                clear()
                print '%d / %d' %(progress, total)
                print one
                print '\n'
                choice = raw_input(word_dic[one].strip('\n') + '\n')
            if choice == 'n':
                words_to_save[one] = word_dic[one].strip('\n')
            else:    
                pass 
    return words_to_save
            
def clear():
    if os.name == 'posix':
        os.system('clear')
    else:
        os.system('cls')
        
if __name__ == '__main__':
    word_dic = read_file(sys.argv[1])
    words_to_save = test_words(word_dic)
    save_file(words_to_save)
    clear()
    print 'All done!'