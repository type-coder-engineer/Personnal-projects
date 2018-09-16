# coding: utf
from Tkinter import * 
import tkMessageBox 
from PIL import Image, ImageTk
import ttk
import time
import threading
import random
import time
import win32api,win32con 
# to make a .exe file, just tap 'pyinstaller sudoku_GUI.spec'

def shuffling(all):
    new_list = all[:]
    for index in xrange(1, len(all)):
        index_exc = random.randint(0, index)
        new_list[index], new_list[index_exc] = new_list[index_exc], new_list[index]
    return new_list
 
# 用于生成数独终盘的时候判断每个空格不能填入的数字
def limit_generate(map, row, col):
    list_limit = []
    
    #先将row和col中已经有的数字加入list
    for one in xrange(col):
        list_limit.append(map[row*9 + one])
    for one in xrange(row):
        list_limit.append(map[one*9 + col])
        
    # 再找出小的3*3的矩阵中出现的数字
    local_row = (row // 3) * 3
    local_col = (col // 3) * 3
    for i in xrange(local_row, row):
        list_limit.append(map[i*9 + local_col])
        list_limit.append(map[i*9 + local_col + 1])
        list_limit.append(map[i*9 + local_col + 2])
    for i in xrange(local_col, col):
        list_limit.append(map[9*row + i])
        
    return list(set(list_limit))
   
# 生成数独终盘   
def sudoku_final():
    stack_options = [] # 这是一个stack结构，lifo
    all = range(1, 10)
    map = [0 for index in xrange(81)]
    map[:9] = shuffling(all)
    index = 9
    
    while(index < 81):
        row = index // 9
        col = index % 9
        already = limit_generate(map, row, col)
        options = [one for one in all if one not in already]
        
        # 如果除去不能填的数字还可以选择那么就填入任意一个选择，然后把剩余的选择放入stack中
        if len(options) > 0:
            options = shuffling(options)
            map[index] = options.pop(0)
            stack_options.append(options)
            index += 1
        else:
        # 如果没有可以填的选择，那么将上一个数字换成另一个选择
            last_options = []
            while(len(last_options) == 0):
                last_options = stack_options.pop()
                index -= 1
            map[index] = last_options.pop(0)
            stack_options.append(last_options)
            index += 1
    return map

# 用于解决数独题目时判断每个空格不能填入的数字    
def limit_solve(map, row, col):
    list_limit = []
    
    #先将row和col中已经有的数字加入list, 这里是两边的数字
    for one in xrange(9):
        if map[row*9 + one] != 0:
            list_limit.append(map[row*9 + one])
    for one in xrange(9):
        if map[one*9 + col] != 0:
            list_limit.append(map[one*9 + col])
        
    # 再找出小的3*3的矩阵中出现的数字，这里是所有9个数字都要遍历
    local_row = (row // 3) * 3
    local_col = (col // 3) * 3
    for i in xrange(local_row, local_row + 3):
        for j in xrange(local_col, local_col + 3):
            if map[9*i + j] != 0:
                list_limit.append(map[9*i + j])
        
    return list(set(list_limit))
 
# 检查数独题目是否有问题
def puzzle_verify(puzzle):
    nb_blanks = 0
    for row in xrange(9):
        for col in xrange(9):
            if puzzle[row*9 + col] == 0:
                nb_blanks += 1
    if nb_blanks > 64:
        return False

    for row in xrange(9):
        list_col = []
        for col in xrange(9):
            if puzzle[row*9 + col] == 0:
                pass
            else:
                if puzzle[row*9 + col] in list_col or puzzle[row*9 + col] > 9 or puzzle[row*9 + col] < 0:
                    return False
                else:
                    list_col.append(puzzle[row*9 + col])
                    
    for col in xrange(9):
        list_row = []
        for row in xrange(9):
            if puzzle[row*9 + col] == 0:
                pass
            else:
                if puzzle[row*9 + col] in list_row or puzzle[row*9 + col] > 9 or puzzle[row*9 + col] < 0:
                    return False
                else:
                    list_row.append(puzzle[row*9 + col]) 
                    
    for pos in [(0, 0), (3, 0), (6, 0), (0, 3), (3, 3), (6, 3), (0, 6), (3, 6), (6, 6)]:  
        list_ele = []
        for i in xrange(3):
            for j in xrange(3):
                if puzzle[(pos[0] + i)*9 + pos[1] + j] == 0:
                    pass
                else:
                    if puzzle[(pos[0] + i)*9 + pos[1] + j] in list_ele:
                        return False
                    else:
                        list_ele.append(puzzle[(pos[0] + i)*9 + pos[1] + j])
    return True

# 得到数独的解    
def sudoku_solving(puzzle):
    map_solved = []
    pos_blank = []
    stack_options = []
    all = range(1, 10)
    for index in xrange(81):
        if puzzle[index] == 0:
            pos_blank.append(index)
    blank_nb = len(pos_blank)
    index = 0
    origin = puzzle[:]
    flag_over = False
    
    while(1):
        row = pos_blank[index] // 9
        col = pos_blank[index] % 9
        already = limit_solve(puzzle, row, col)
        options = [one for one in all if one not in already]
        
        # 如果除去不能填的数字还可以选择那么就填入任意一个选择，然后把剩余的选择放入stack中
        if len(options) > 0:
            puzzle[pos_blank[index]] = options.pop(0)
            stack_options.append(options)
            index += 1
            if index == blank_nb:
                map_solved.append(puzzle[:])
                index = 0
                first_option = []
                for one in stack_options:
                    if len(one) == 0:
                        index += 1
                    else:
                        first_option = one[:]
                        break
                if not first_option:
                    break
                puzzle[pos_blank[index] + 1:] = origin[pos_blank[index] + 1:]
                puzzle[pos_blank[index]] = first_option.pop(0)
                stack_options = [first_option]
                index += 1
                continue
            # print options
            # print_map(puzzle)
            # raw_input()
        else:
        # 如果没有可以填的选择，那么将上一个数字换成另一个选择
            last_options = []
            while(len(last_options) == 0):
                if not stack_options: # 说明已经用尽了可能了
                    flag_over = True
                    break
                last_options = stack_options.pop()
                index -= 1
                puzzle[pos_blank[index]] = 0 # 注意这里和生成数独终盘的时候不一样，如果这个要
                # 往前回溯的话必须要将已经填入的数字清零
            if flag_over:
                break
            puzzle[pos_blank[index]] = last_options.pop(0)
            stack_options.append(last_options)
            index += 1
    return map_solved

# 在数独终盘上随机挖去数字形成题目    
def dibble(final, level):
    map = final[:]
    list_blank = []
        
    for pos in [(0, 0), (3, 0), (6, 0), (0, 3), (3, 3), (6, 3), (0, 6), (3, 6), (6, 6)]:
        if level == 1:
            total = random.randint(2, 3)
        elif level == 2:
            total = random.randint(4, 5)
        elif level == 3:
            total = random.randint(6, 7)

        for index in xrange(total):
            i = random.randint(0, 2)
            j = random.randint(0, 2)
            while (pos[0] + i, pos[1] + j) in list_blank:
                i = random.randint(0, 2)
                j = random.randint(0, 2)
            list_blank.append((pos[0] + i, pos[1] + j))
            
    for one in list_blank:
        index = one[0]*9 + one[1]
        map[index] = 0
    return map

# 用于检查这个题目是否有多解，或者解这个题目是否用时超过1s，不合格的就返回False
def sudoku_verify(test):
    puzzle = test[:]
    map_solved = []
    pos_blank = []
    stack_options = []
    all = range(1, 10)
    for index in xrange(81):
        if puzzle[index] == 0:
            pos_blank.append(index)
    blank_nb = len(pos_blank)
    index = 0
    origin = puzzle[:]
    flag_over = False
    start = time.time()
    
    while(1):
        end = time.time()
        if (end - start) > 1:
            # print 'time out'
            return False
        if len(map_solved) > 1:
            # print 'not unique'
            return False
        row = pos_blank[index] // 9
        col = pos_blank[index] % 9
        already = limit_solve(puzzle, row, col)
        options = [one for one in all if one not in already]
        
        if len(options) > 0:
            puzzle[pos_blank[index]] = options.pop(0)
            stack_options.append(options)
            index += 1
            if index == blank_nb:
                map_solved.append(puzzle[:])
                index = 0
                first_option = []
                for one in stack_options:
                    if len(one) == 0:
                        index += 1
                    else:
                        first_option = one[:]
                        break
                if not first_option:
                    break
                puzzle[pos_blank[index] + 1:] = origin[pos_blank[index] + 1:]
                puzzle[pos_blank[index]] = first_option.pop(0)
                stack_options = [first_option]
                index += 1
                continue
        else:
            last_options = []
            while(len(last_options) == 0):
                if not stack_options: # 说明已经用尽了可能了
                    flag_over = True
                    break
                last_options = stack_options.pop()
                index -= 1
                puzzle[pos_blank[index]] = 0 
            if flag_over:
                break
            puzzle[pos_blank[index]] = last_options.pop(0)
            stack_options.append(last_options)
            index += 1
    if len(map_solved) == 1:
        return True
    else:
        return False

# 生成数独题目        
def sudoku_puzzle(final, level):
    map_final = final[:]
    puzzle = dibble(map_final, level)
    list_notGood = []
    while (not sudoku_verify(puzzle)):
        list_notGood.append(puzzle)
        while(puzzle in list_notGood):
            puzzle = dibble(map_final, level)
    return puzzle
    
class SudokuGUI:
    def __init__(self):
        self.window = Tk()
        self.window.minsize(width = WIDTH, height = HEIGHT)
        self.window.title("数独世界") 
        self.window.iconbitmap('sudokuIco.ico')
        self.frame = Frame(self.window, width = WIDTH, height = HEIGHT)
        self.background_image = ImageTk.PhotoImage(Image.open('bg3.png'))   
        self.background_imageLeft = ImageTk.PhotoImage(Image.open('left.png'))  
        self.background_imageRight = ImageTk.PhotoImage(Image.open('right.png'))           
        self.background_imageDown1 = ImageTk.PhotoImage(Image.open('down1.png'))                   
        self.background_imageDown2 = ImageTk.PhotoImage(Image.open('down2.png'))                   
        self.flag_language = 'ch'
       
        self.puzzleEasyReady = False
        self.puzzleMedianReady = False
        self.puzzleHardReady = False
        print '[init] - Begin to generate a new sudoku by a thread'
        th_puzzle = threading.Thread(target = self.generatePuzzle) # 一个线程用来生成这个puzzle,这样可以提前生成下一个数独题目，防止hard难度的数独花费时间过长
        th_puzzle.setDaemon(True)
        th_puzzle.start()  
        self.main()
        
    def main(self):
        self.frame.destroy()
        self.flag_count = False
        self.frame = Frame(self.window, width = WIDTH, height = HEIGHT)
        self.background_label = Label(self.frame, image = self.background_image)
        self.background_label.place(x = 0, y = 0, relwidth = 1, relheight = 1)
        if self.flag_language == 'ch':
            Label(self.frame, font = ("Purisa", 24, 'bold'), text = "欢迎来到数独世界！", fg = '#000000', bg = '#eeeebb').place(x = WIDTH / 2, y = 60, anchor = 'center')
            Label(self.frame, font = ("Purisa", 10), text = "作者: 张辰宇", fg = '#000000', bg = '#eeeebb').place(x = WIDTH / 2, y = 120, anchor = 'center')
            Label(self.frame, font = ("Purisa", 10), text = "欢迎来我的github主页逛逛: https://github.com/type-coder-engineer", fg = '#000000', bg = '#eeeebb').place(x = WIDTH / 2, y = 140, anchor = 'center')
            
            Label(self.frame, font = ("Purisa", 12), text = '数独难度：', fg = '#000000', bg = '#eeeebb').place(x = 120, y = 280, anchor = 'center')
            self.level = StringVar()
            self.level.set("median") # 默认初始值
            ttk.Combobox(self.frame, textvariable = self.level, values = ["easy", "median", "hard"]).place(x = WIDTH / 2, y = 280, anchor = 'center')
            Button(self.frame, font = ("Purisa", 15), text = '数独题目', width = 12, height = 1, command = self.sudokuPuzzleWait, fg = '#000000', bg = '#cccc99').place(x = WIDTH / 3, y = 220, anchor = 'center')
            Button(self.frame, font = ("Purisa", 15), text = '挑战模式', width = 12, height = 1, command = self.sudokuChallengeWait, fg = '#000000', bg = '#cccc99').place(x = WIDTH * 2 / 3, y = 220, anchor = 'center')
            Button(self.frame, font = ("Purisa", 15), text = '解数独', width = 12, height = 1, command = self.sudokuSolve, fg = '#000000', bg = '#cccc99').place(x = WIDTH / 2, y = 340, anchor = 'center')
            Button(self.frame, font = ("Purisa", 12), text = 'change language', width = 15, height = 1, command = self.changeLanguage, fg = '#000000', bg = '#cccc99').place(x = WIDTH / 2, y = 440, anchor = 'center')
        else:
            Label(self.frame, font = ("Purisa", 19, 'bold'), text = "Welcome to the SUDOKU WORLD!", fg = '#000000', bg = '#eeeebb').place(x = WIDTH / 2, y = 60, anchor = 'center')
            Label(self.frame, font = ("Purisa", 10), text = "Author: GUIGUI", fg = '#000000', bg = '#eeeebb').place(x = WIDTH / 2, y = 120, anchor = 'center')
            Label(self.frame, font = ("Purisa", 10), text = "Welcome to my github: https://github.com/type-coder-engineer", fg = '#000000', bg = '#eeeebb').place(x = WIDTH / 2, y = 140, anchor = 'center')
            
            Label(self.frame, font = ("Purisa", 10), text = 'difficulty level：', fg = '#000000', bg = '#eeeebb').place(x = 120, y = 280, anchor = 'center')
            self.level = StringVar()
            self.level.set("median") # 默认初始值
            ttk.Combobox(self.frame, textvariable = self.level, values = ["easy", "median", "hard"]).place(x = WIDTH / 2, y = 280, anchor = 'center')
            Button(self.frame, font = ("Purisa", 14), text = 'sudoku puzzle', width = 15, height = 1, command = self.sudokuPuzzleWait, fg = '#000000', bg = '#cccc99').place(x = WIDTH / 3, y = 220, anchor = 'center')
            Button(self.frame, font = ("Purisa", 14), text = 'challenge mode', width = 15, height = 1, command = self.sudokuChallengeWait, fg = '#000000', bg = '#cccc99').place(x = WIDTH * 2 / 3, y = 220, anchor = 'center')
            Button(self.frame, font = ("Purisa", 14), text = 'solve sudoku', width = 15, height = 1, command = self.sudokuSolve, fg = '#000000', bg = '#cccc99').place(x = WIDTH / 2, y = 340, anchor = 'center')
            Button(self.frame, font = ("Purisa", 12), text = '更换语言', width = 12, height = 1, command = self.changeLanguage, fg = '#000000', bg = '#cccc99').place(x = WIDTH / 2, y = 440, anchor = 'center')
        
        self.frame.pack()
        
    def changeLanguage(self):
        if self.flag_language == 'ch':
            self.flag_language = 'en'
        else:
            self.flag_language = 'ch'
        self.main()
    
    def sudokuPuzzleWait(self):
        if self.level.get() != 'easy' and self.level.get() != 'median' and self.level.get() != 'hard':
            if self.flag_language == 'ch':
                tkMessageBox.showwarning("检查难度", "难度必须是 easy, median 或者 hard 哦!")
            else:
                tkMessageBox.showwarning("check difficulty", "The difficulty must be easy, median or hard!")
            return
        self.frame.destroy()
        self.frame = Frame(self.window, width = WIDTH, height = HEIGHT)
        self.background_label = Label(self.frame, image = self.background_image)
        self.background_label.place(x = 0, y = 0, relwidth = 1, relheight = 1) 
        if self.flag_language == 'ch':
            Label(self.frame, font = ("Purisa", 22), text = "正在生成题目   ", fg = '#000000', bg = '#eeeebb').place(x = 150, y = 200, anchor = SW)
        else:
            Label(self.frame, font = ("Purisa", 20), text = "The puzzle is generating   ", fg = '#000000', bg = '#eeeebb').place(x = 60, y = 200, anchor = SW)
        self.frame.pack()
        th_animation = threading.Thread(target = self.signalPuzzleWait) # 另一个线程用来产生动画效果
        th_animation.setDaemon(True)
        th_animation.start()
        
    def sudokuChallengeWait(self):
        if self.level.get() != 'easy' and self.level.get() != 'median' and self.level.get() != 'hard':
            if self.flag_language == 'ch':
                tkMessageBox.showwarning("检查难度", "难度必须是 easy, median 或者 hard 哦!")
            else:
                tkMessageBox.showwarning("check difficulty", "The difficulty must be easy, median or hard!")
            return
        self.frame.destroy()
        self.frame = Frame(self.window, width = WIDTH, height = HEIGHT)
        self.background_label = Label(self.frame, image = self.background_image)
        self.background_label.place(x = 0, y = 0, relwidth = 1, relheight = 1) 
        if self.flag_language == 'ch':
            Label(self.frame, font = ("Purisa", 22), text = "正在生成题目   ", fg = '#000000', bg = '#eeeebb').place(x = 150, y = 200, anchor = SW)
        else:
            Label(self.frame, font = ("Purisa", 20), text = "The puzzle is generating   ", fg = '#000000', bg = '#eeeebb').place(x = 60, y = 200, anchor = SW)
        self.frame.pack()
        th_animation = threading.Thread(target = self.signalChallengeWait) # 另一个线程用来产生动画效果
        th_animation.setDaemon(True)
        th_animation.start()
        
    def animationWait(self, index):
        self.frame.destroy()
        self.frame = Frame(self.window, width = WIDTH, height = HEIGHT)
        self.background_label = Label(self.frame, image = self.background_image)
        self.background_label.place(x = 0, y = 0, relwidth = 1, relheight = 1) 
        if index % 4 == 0:
            if self.flag_language == 'ch':
                Label(self.frame, font = ("Purisa", 22), text = "正在生成题目...", fg = '#000000', bg = '#eeeebb').place(x = 150, y = 200, anchor = SW)
            else:
                Label(self.frame, font = ("Purisa", 20), text = "The puzzle is generating...", fg = '#000000', bg = '#eeeebb').place(x = 60, y = 200, anchor = SW)
        elif (index + 1) % 4 == 0:
            if self.flag_language == 'ch':
                Label(self.frame, font = ("Purisa", 22), text = "正在生成题目.. ", fg = '#000000', bg = '#eeeebb').place(x = 150, y = 200, anchor = SW)
            else:
                Label(self.frame, font = ("Purisa", 20), text = "The puzzle is generating.. ", fg = '#000000', bg = '#eeeebb').place(x = 60, y = 200, anchor = SW)
        elif (index + 2) % 4 == 0:
            if self.flag_language == 'ch':
                Label(self.frame, font = ("Purisa", 22), text = "正在生成题目.  ", fg = '#000000', bg = '#eeeebb').place(x = 150, y = 200, anchor = SW)
            else:
                Label(self.frame, font = ("Purisa", 20), text = "The puzzle is generating.  ", fg = '#000000', bg = '#eeeebb').place(x = 60, y = 200, anchor = SW)
        else:
            if self.flag_language == 'ch':
                Label(self.frame, font = ("Purisa", 22), text = "正在生成题目   ", fg = '#000000', bg = '#eeeebb').place(x = 150, y = 200, anchor = SW)
            else:
                Label(self.frame, font = ("Purisa", 20), text = "The puzzle is generating   ", fg = '#000000', bg = '#eeeebb').place(x = 60, y = 200, anchor = SW)
        self.frame.pack()
    
    def signalPuzzleWait(self):
        index = 2
        if self.level.get() == 'easy':
            while (not self.puzzleEasyReady): # puzzle还没有好的时候用一个循环来生成动画效果
                time.sleep(0.4)
                self.animationWait(index)
                index += 1
        elif self.level.get() == 'median':
            while (not self.puzzleMedianReady): 
                time.sleep(0.4)
                self.animationWait(index)
                index += 1
        elif self.level.get() == 'hard':
            while (not self.puzzleHardReady): 
                time.sleep(0.4)
                self.animationWait(index)
                index += 1
        time.sleep(0.2)
        self.sudokuPuzzleShow()
        
    def signalChallengeWait(self):
        index = 2
        self.flag_count = False
        if self.level.get() == 'easy':
            while (not self.puzzleEasyReady): # puzzle还没有好的时候用一个循环来生成动画效果
                time.sleep(0.4)
                self.animationWait(index)
                index += 1
        if self.level.get() == 'median':
            while (not self.puzzleMedianReady): 
                time.sleep(0.4)
                self.animationWait(index)
                index += 1
        if self.level.get() == 'hard':
            while (not self.puzzleHardReady): 
                time.sleep(0.4)
                self.animationWait(index)
                index += 1
        time.sleep(0.2)
        self.sudokuChallengeConfirm()
        
    def sudokuChallengeConfirm(self):
        self.frame.destroy()
        self.frame = Frame(self.window, width = WIDTH, height = HEIGHT)
        self.background_label = Label(self.frame, image = self.background_image)
        self.background_label.place(x = 0, y = 0, relwidth = 1, relheight = 1) 
        if self.flag_language == 'ch':
            Label(self.frame, font = ("Purisa", 22), text = "您选择了挑战模式", fg = '#000000', bg = '#eeeebb').place(x = WIDTH / 2, y = 130, anchor = 'center')
            Label(self.frame, font = ("Purisa", 22), text = "点击确认后就会开始计时", fg = '#000000', bg = '#eeeebb').place(x = WIDTH / 2, y = 180, anchor = 'center')
            Button(self.frame, font = ("Purisa", 15), text = '确认挑战', width = 12, height = 1, command = self.sudokuChallengeShow, fg = '#000000', bg = '#cccc99').place(x = WIDTH / 2, y = 280, anchor = 'center')
            Button(self.frame, font = ("Purisa", 15), text = '回到主菜单', width = 12, height = 1, command = self.main, fg = '#000000', bg = '#cccc99').place(x = WIDTH / 2, y = 370, anchor = 'center')    
        else:
            Label(self.frame, font = ("Purisa", 18), text = "You chose the challenging mode", fg = '#000000', bg = '#eeeebb').place(x = WIDTH / 2, y = 130, anchor = 'center')
            Label(self.frame, font = ("Purisa", 18), text = "Click 'Yes!' and start the counting down", fg = '#000000', bg = '#eeeebb').place(x = WIDTH / 2, y = 180, anchor = 'center')
            Button(self.frame, font = ("Purisa", 15), text = 'Yes!', width = 12, height = 1, command = self.sudokuChallengeShow, fg = '#000000', bg = '#cccc99').place(x = WIDTH / 2, y = 280, anchor = 'center')
            Button(self.frame, font = ("Purisa", 12), text = 'return to menu', width = 18, height = 1, command = self.main, fg = '#000000', bg = '#cccc99').place(x = WIDTH / 2, y = 370, anchor = 'center')    
        
        self.frame.pack()
        
    def generatePuzzle(self):
        lock.acquire()
        try:
            self.nextFinal = sudoku_final()
            self.puzzleEasy = sudoku_puzzle(self.nextFinal, 1)
            self.puzzleEasyReady = True
            print '[generatePuzzle] - easy sudoku is ready'
            self.puzzleMedian = sudoku_puzzle(self.nextFinal, 2)
            self.puzzleMedianReady = True
            print '[generatePuzzle] - median sudoku is ready'
            self.puzzleHard = sudoku_puzzle(self.nextFinal, 3) 
            self.puzzleHardReady = True
            print '[generatePuzzle] - hard sudoku is ready'
        finally:
            lock.release()
      
    def sudokuPuzzleShow(self):
        self.frame.destroy()
        self.frame = Canvas(self.window, width = 500, height = 550, bg = '#eeeebb') # 注意如果是place的话要先确定好frame的尺寸
        self.background_labelLeft = Label(self.frame, image = self.background_imageLeft)
        self.background_labelLeft.place(x = 0, y = 0) 
        self.background_labelRight = Label(self.frame, image = self.background_imageRight)
        self.background_labelRight.place(x = 465, y = 0) 
        self.background_labelDown = Label(self.frame, image = self.background_imageDown1)
        self.background_labelDown.place(x = 0, y = 420) 
        if self.level.get() == 'easy':
            self.puzzle = self.puzzleEasy[:]
        elif self.level.get() == 'median':
            self.puzzle = self.puzzleMedian[:]
        else:
            self.puzzle = self.puzzleHard[:]
            
        self.final = self.nextFinal[:]
        print '[sudokuPuzzleShow] - take the nextFinal sudoku'
        
        self.answer = []
        for i in range(9):
            for j in range(9):
                if self.puzzle[i*9 + j] == 0:
                    self.answer.append(self.final[i*9 + j])
        
        self.blanks = []
        for i in range(9):
            for j in range(9):
                if self.puzzle[i*9 + j] == 0:
                    self.blanks.append(StringVar())
       
        index = 0           
        for i in xrange(9):
            for j in xrange(9):
                if i < 3:
                    pos_x = i*45 + 75
                if j < 3:
                    pos_y = j*45 + 30
                if i >= 3 and i < 6:
                    pos_x = i*45 + 75
                if j >= 3 and j < 6:
                    pos_y = j*45 + 30
                if i >= 6:
                    pos_x = i*45 + 75
                if j >= 6:
                    pos_y = j*45 + 30
                if self.puzzle[i*9 + j] == 0:
                    Entry(self.frame, width = 3, justify = CENTER, textvariable = self.blanks[index]).place(x = pos_x, y = pos_y, anchor = 'center')
                    index += 1
                else:
                    Label(self.frame, width = 3, height = 2, text = str(self.puzzle[i*9 + j]), fg = '#000000', bg = '#eeeebb').place(x = pos_x, y = pos_y, anchor = 'center')
                    
        self.frame.create_rectangle(55, 10, 455, 410)
        self.frame.create_line(99, 10, 99, 410, dash = (4, 4))
        self.frame.create_line(142, 10, 142, 410, dash = (4, 4))
        self.frame.create_line(187, 10, 187, 410)          
        self.frame.create_line(232, 10, 232, 410, dash = (4, 4))
        self.frame.create_line(278, 10, 278, 410, dash = (4, 4))
        self.frame.create_line(323, 10, 323, 410)    
        self.frame.create_line(369, 10, 369, 410, dash = (4, 4))
        self.frame.create_line(413, 10, 413, 410, dash = (4, 4))
        
        self.frame.create_line(55, 51, 455, 51, dash = (4, 4)) 
        self.frame.create_line(55, 95, 455, 95, dash = (4, 4)) 
        self.frame.create_line(55, 142, 455, 142)    
        self.frame.create_line(55, 186, 455, 186, dash = (4, 4)) 
        self.frame.create_line(55, 230, 455, 230, dash = (4, 4)) 
        self.frame.create_line(55, 277, 455, 277)    
        self.frame.create_line(55, 320, 455, 320, dash = (4, 4)) 
        self.frame.create_line(55, 367, 455, 367, dash = (4, 4)) 
        if self.flag_language == 'ch':
            Button(self.frame, font = ("Purisa", 12), text = '提交', width = 12, height = 1, command = self.submit, fg = '#000000', bg = '#cccc99').place(x = 150, y = 480, anchor = 'center')
            Button(self.frame, font = ("Purisa", 12), text = '答案', width = 12, height = 1, command = self.getAnswer, fg = '#000000', bg = '#cccc99').place(x = 350, y = 480, anchor = 'center')
            Button(self.frame, font = ("Purisa", 12), text = '新数独', width = 12, height = 1, command = self.sudokuPuzzleWait, fg = '#000000', bg = '#cccc99').place(x = 150, y = 530, anchor = 'center')
            Button(self.frame, font = ("Purisa", 12), text = '回到主菜单', width = 12, height = 1, command = self.main, fg = '#000000', bg = '#cccc99').place(x = 350, y = 530, anchor = 'center')
        else:
            Button(self.frame, font = ("Purisa", 12), text = 'submit', width = 12, height = 1, command = self.submit, fg = '#000000', bg = '#cccc99').place(x = 150, y = 480, anchor = 'center')
            Button(self.frame, font = ("Purisa", 12), text = 'answer', width = 12, height = 1, command = self.getAnswer, fg = '#000000', bg = '#cccc99').place(x = 350, y = 480, anchor = 'center')
            Button(self.frame, font = ("Purisa", 12), text = 'new sudoku', width = 15, height = 1, command = self.sudokuPuzzleWait, fg = '#000000', bg = '#cccc99').place(x = 150, y = 530, anchor = 'center')
            Button(self.frame, font = ("Purisa", 12), text = 'return to menu', width = 18, height = 1, command = self.main, fg = '#000000', bg = '#cccc99').place(x = 350, y = 530, anchor = 'center')
        
        self.frame.pack()
        # print 'new'
        self.puzzleEasyReady = False
        self.puzzleMedianReady = False
        self.puzzleHardReady = False
        print '[sudokuPuzzleShow] - Begin to generate a new sudoku by a thread'
        th_puzzle = threading.Thread(target = self.generatePuzzle) # 一个线程用来生成这个puzzle，这样可以提前生成下一个数独题目，防止hard难度的数独花费时间过长
        th_puzzle.setDaemon(True)
        th_puzzle.start()
        
    def sudokuChallengeShow(self):
        self.start = time.time()
        self.count = 0
        self.flag_count = True
        self.flag_count_timeOut = False
        self.frame.destroy()
        self.frame = Canvas(self.window, width = 500, height = 550, bg = '#eeeebb') 
        self.background_labelLeft = Label(self.frame, image = self.background_imageLeft)
        self.background_labelLeft.place(x = 0, y = 0) 
        self.background_labelRight = Label(self.frame, image = self.background_imageRight)
        self.background_labelRight.place(x = 465, y = 0) 
        self.background_labelDown = Label(self.frame, image = self.background_imageDown2)
        self.background_labelDown.place(x = 0, y = 450) 
        if self.level.get() == 'easy':
            self.puzzle = self.puzzleEasy[:]
        elif self.level.get() == 'median':
            self.puzzle = self.puzzleMedian[:]
        else:
            self.puzzle = self.puzzleHard[:]
			
        self.final = self.nextFinal[:]
        print '[sudokuPuzzleShow] - take the nextFinal sudoku'
		
        self.answer = []
        for i in range(9):
            for j in range(9):
                if self.puzzle[i*9 + j] == 0:
                    self.answer.append(self.final[i*9 + j])
        
        self.blanks = []
        for i in range(9):
            for j in range(9):
                if self.puzzle[i*9 + j] == 0:
                    self.blanks.append(StringVar())
       
        index = 0           
        for i in xrange(9):
            for j in xrange(9):
                if i < 3:
                    pos_x = i*45 + 75
                if j < 3:
                    pos_y = j*45 + 30
                if i >= 3 and i < 6:
                    pos_x = i*45 + 75
                if j >= 3 and j < 6:
                    pos_y = j*45 + 30
                if i >= 6:
                    pos_x = i*45 + 75
                if j >= 6:
                    pos_y = j*45 + 30
                if self.puzzle[i*9 + j] == 0:
                    Entry(self.frame, width = 3, justify = CENTER, textvariable = self.blanks[index]).place(x = pos_x, y = pos_y, anchor = 'center')
                    index += 1
                else:
                    Label(self.frame, width = 3, height = 2, text = str(self.puzzle[i*9 + j]), fg = '#000000', bg = '#eeeebb').place(x = pos_x, y = pos_y, anchor = 'center')
                    
        self.frame.create_rectangle(55, 10, 455, 410)
        self.frame.create_line(99, 10, 99, 410, dash = (4, 4))
        self.frame.create_line(142, 10, 142, 410, dash = (4, 4))
        self.frame.create_line(187, 10, 187, 410)          
        self.frame.create_line(232, 10, 232, 410, dash = (4, 4))
        self.frame.create_line(278, 10, 278, 410, dash = (4, 4))
        self.frame.create_line(323, 10, 323, 410)    
        self.frame.create_line(369, 10, 369, 410, dash = (4, 4))
        self.frame.create_line(413, 10, 413, 410, dash = (4, 4))
        
        self.frame.create_line(55, 51, 455, 51, dash = (4, 4)) 
        self.frame.create_line(55, 95, 455, 95, dash = (4, 4)) 
        self.frame.create_line(55, 142, 455, 142)    
        self.frame.create_line(55, 186, 455, 186, dash = (4, 4)) 
        self.frame.create_line(55, 230, 455, 230, dash = (4, 4)) 
        self.frame.create_line(55, 277, 455, 277)    
        self.frame.create_line(55, 320, 455, 320, dash = (4, 4)) 
        self.frame.create_line(55, 367, 455, 367, dash = (4, 4)) 
        if self.flag_language == 'ch':
            Label(self.frame, font = ("Purisa", 12), text = '已用时： ', fg = '#000000', bg = '#eeeebb').place(x = WIDTH / 2 - 60, y = 430, anchor = 'center')
            self.label_count = Label(self.frame, font = ("Purisa", 14), text = str(self.count), fg = '#000000', bg = '#eeeebb')
            self.label_count.place(x = WIDTH / 2, y = 430, anchor = 'center')
            Label(self.frame, font = ("Purisa", 12), text = ' 秒', fg = '#000000', bg = '#eeeebb').place(x = WIDTH / 2 + 40, y = 430, anchor = 'center')
        else:
            Label(self.frame, font = ("Purisa", 10), text = 'You have used： ', fg = '#000000', bg = '#eeeebb').place(x = WIDTH / 2 - 80, y = 430, anchor = 'center')
            self.label_count = Label(self.frame, font = ("Purisa", 14), text = str(self.count), fg = '#000000', bg = '#eeeebb')
            self.label_count.place(x = WIDTH / 2, y = 430, anchor = 'center')
            Label(self.frame, font = ("Purisa", 10), text = ' seconds', fg = '#000000', bg = '#eeeebb').place(x = WIDTH / 2 + 60, y = 430, anchor = 'center')
            
        if self.flag_language == 'ch':
            Button(self.frame, font = ("Purisa", 12), text = '提交', width = 12, height = 1, command = self.submit, fg = '#000000', bg = '#cccc99').place(x = 150, y = 480, anchor = 'center')
            Button(self.frame, font = ("Purisa", 12), text = '答案', width = 12, height = 1, command = self.getAnswer, fg = '#000000', bg = '#cccc99').place(x = 350, y = 480, anchor = 'center')
            Button(self.frame, font = ("Purisa", 12), text = '新数独', width = 12, height = 1, command = self.sudokuChallengeWait, fg = '#000000', bg = '#cccc99').place(x = 150, y = 530, anchor = 'center')
            Button(self.frame, font = ("Purisa", 12), text = '回到主菜单', width = 12, height = 1, command = self.main, fg = '#000000', bg = '#cccc99').place(x = 350, y = 530, anchor = 'center')
        else:
            Button(self.frame, font = ("Purisa", 12), text = 'submit', width = 12, height = 1, command = self.submit, fg = '#000000', bg = '#cccc99').place(x = 150, y = 480, anchor = 'center')
            Button(self.frame, font = ("Purisa", 12), text = 'answer', width = 12, height = 1, command = self.getAnswer, fg = '#000000', bg = '#cccc99').place(x = 350, y = 480, anchor = 'center')
            Button(self.frame, font = ("Purisa", 12), text = 'new sudoku', width = 15, height = 1, command = self.sudokuChallengeWait, fg = '#000000', bg = '#cccc99').place(x = 150, y = 530, anchor = 'center')
            Button(self.frame, font = ("Purisa", 12), text = 'return to menu', width = 18, height = 1, command = self.main, fg = '#000000', bg = '#cccc99').place(x = 350, y = 530, anchor = 'center')
         
        self.frame.pack()
        
        self.puzzleEasyReady = False
        self.puzzleMedianReady = False
        self.puzzleHardReady = False
        print '[sudokuPuzzleShow] - Begin to generate a new sudoku by a thread'
        th_puzzle = threading.Thread(target = self.generatePuzzle) # 一个线程用来生成这个puzzle，这样可以提前生成下一个数独题目，防止hard难度的数独花费时间过长
        th_puzzle.setDaemon(True)
        th_puzzle.start()
        
        th_count = threading.Thread(target = self.countingSignal) # 一个线程用来实现计时
        th_count.setDaemon(True)
        th_count.start()
 
    def countingSignal(self):
        while(self.flag_count):
            if self.flag_count_timeOut:
                time.sleep(0.2)
            else:
                self.end = time.time()
                countNow = int(self.end - self.start) 
                if countNow > self.count:
                    self.count = countNow
                    self.countingLabel()
                
    def countingLabel(self):
        self.label_count.destroy()
        self.label_count = Label(self.frame, font = ("Purisa", 14), text = str(self.count), fg = '#000000', bg = '#eeeebb')
        self.label_count.place(x = WIDTH / 2, y = 430, anchor = 'center')
        
    def submit(self):
        values = [one.get() for one in self.blanks]
        response = []
        all = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        for one in values:
            if one in all:
                response.append(int(one))
        
        if len(self.answer) != len(response):
            if self.flag_language == 'ch':
                tkMessageBox.showwarning("检查答案", "还有漏填的空，或者空格中的数字超过9了...")
            else:
                tkMessageBox.showwarning("check answer", "You haven't filled all blanks or some number is bigger than 9...")    
            return
            
        if self.answer == response:
            if self.flag_language == 'ch':
                tkMessageBox.showinfo("检查答案","棒极了，答案完全正确！")
            else:
                tkMessageBox.showinfo("check answer","Great, the answer is correct!")
        else:
            if self.flag_language == 'ch':
                tkMessageBox.showwarning("检查答案", "答案有错误哦。。。")
            else:
                tkMessageBox.showwarning("check answer", "Sorry, the answer is not correct...")
        return  
 
    def submitChallenge(self):
        values = [one.get() for one in self.blanks]
        response = []
        all = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        for one in values:
            if one in all:
                response.append(int(one))
        
        if len(self.answer) != len(response):
            if self.flag_language == 'ch':
                tkMessageBox.showwarning("检查答案", "还有漏填的空，或者空格中的数字超过9了...")
            else:
                tkMessageBox.showwarning("check answer", "You haven't filled all blanks or some number is bigger than 9...")    
            return
            
        if self.answer == response:
            self.flag_count = False
            if self.flag_language == 'ch':
                text = "棒极了，答案完全正确！花费了 {} 秒完成 ".format(self.count)
                tkMessageBox.showinfo("检查答案", text)
            else:
                text = "Great, the answer is correct, you took {} seconds to complete!".format(self.count)
                tkMessageBox.showinfo("check answer", text)
        else:
            if self.flag_language == 'ch':
                tkMessageBox.showwarning("检查答案", "答案有错误哦。。。")
            else:
                tkMessageBox.showwarning("check answer", "Sorry, the answer is not correct...")
            return  
        
    def getAnswer(self):
        self.flag_count_timeOut = True
        if self.flag_language == 'ch':
            flag = tkMessageBox.askokcancel(message = "你真的想看答案吗?") 
        else:
            flag = tkMessageBox.askokcancel(message = "Do you really want to see the answer?") 
        if flag:
            pass
        else:
            self.flag_count_timeOut = False
            return
            
        newWindow = Tk()
        if self.flag_language == 'ch':
            newWindow.title("参考答案")
        else:
            newWindow.title('answer')
        newWindow.iconbitmap('sudokuIco.ico')
        newFrame = Canvas(newWindow, width = 500, height = 500, bg = '#eeeebb')
        self.flag_count = False
        
        for i in xrange(9):
            for j in xrange(9):
                if i < 3:
                    pos_x = i*45 + 75
                if j < 3:
                    pos_y = j*45 + 30
                if i >= 3 and i < 6:
                    pos_x = i*45 + 75
                if j >= 3 and j < 6:
                    pos_y = j*45 + 30
                if i >= 6:
                    pos_x = i*45 + 75
                if j >= 6:
                    pos_y = j*45 + 30
                Label(newFrame, width = 3, height = 2, text = str(self.final[i*9 + j]), fg = '#000000', bg = '#eeeebb').place(x = pos_x, y = pos_y, anchor = 'center')
                
        newFrame.create_rectangle(55, 10, 455, 410)
        newFrame.create_line(99, 10, 99, 410, dash = (4, 4))
        newFrame.create_line(142, 10, 142, 410, dash = (4, 4))
        newFrame.create_line(187, 10, 187, 410)          
        newFrame.create_line(232, 10, 232, 410, dash = (4, 4))
        newFrame.create_line(278, 10, 278, 410, dash = (4, 4))
        newFrame.create_line(323, 10, 323, 410)    
        newFrame.create_line(369, 10, 369, 410, dash = (4, 4))
        newFrame.create_line(413, 10, 413, 410, dash = (4, 4))
        newFrame.create_line(55, 51, 455, 51, dash = (4, 4)) 
        newFrame.create_line(55, 95, 455, 95, dash = (4, 4)) 
        newFrame.create_line(55, 142, 455, 142)    
        newFrame.create_line(55, 186, 455, 186, dash = (4, 4)) 
        newFrame.create_line(55, 230, 455, 230, dash = (4, 4)) 
        newFrame.create_line(55, 277, 455, 277)    
        newFrame.create_line(55, 320, 455, 320, dash = (4, 4)) 
        newFrame.create_line(55, 367, 455, 367, dash = (4, 4)) 
                
        Button(newFrame, font = ("Purisa", 12), text = "OK!", width = 12, height = 1, command = newWindow.destroy, fg = '#000000', bg = '#cccc99').place(x = WIDTH / 2, y = 450, anchor = 'center')
        newFrame.pack()
        newWindow.mainloop()
        
    def sudokuSolve(self):
        self.frame.destroy()  
        self.frame = Canvas(self.window, width = 500, height = 550, bg = '#eeeebb')
        self.background_labelLeft = Label(self.frame, image = self.background_imageLeft)
        self.background_labelLeft.place(x = 0, y = 0) 
        self.background_labelRight = Label(self.frame, image = self.background_imageRight)
        self.background_labelRight.place(x = 465, y = 0) 
        self.background_labelDown = Label(self.frame, image = self.background_imageDown1)
        self.background_labelDown.place(x = 0, y = 420) 
        self.blanks = []
        for index in xrange(81):
            self.blanks.append(StringVar())
        index = 0
        for i in xrange(9):
            for j in xrange(9):
                if i < 3:
                    pos_x = i*45 + 75
                if j < 3:
                    pos_y = j*45 + 30
                if i >= 3 and i < 6:
                    pos_x = i*45 + 75
                if j >= 3 and j < 6:
                    pos_y = j*45 + 30
                if i >= 6:
                    pos_x = i*45 + 75
                if j >= 6:
                    pos_y = j*45 + 30
                Entry(self.frame, width = 3, justify = CENTER, textvariable = self.blanks[index]).place(x = pos_x, y = pos_y, anchor = 'center')
                index += 1
                
        self.frame.create_rectangle(55, 10, 455, 410)
        self.frame.create_line(99, 10, 99, 410, dash = (4, 4))
        self.frame.create_line(142, 10, 142, 410, dash = (4, 4))
        self.frame.create_line(187, 10, 187, 410)          
        self.frame.create_line(232, 10, 232, 410, dash = (4, 4))
        self.frame.create_line(278, 10, 278, 410, dash = (4, 4))
        self.frame.create_line(323, 10, 323, 410)    
        self.frame.create_line(369, 10, 369, 410, dash = (4, 4))
        self.frame.create_line(413, 10, 413, 410, dash = (4, 4))
        self.frame.create_line(55, 51, 455, 51, dash = (4, 4)) 
        self.frame.create_line(55, 95, 455, 95, dash = (4, 4)) 
        self.frame.create_line(55, 142, 455, 142)    
        self.frame.create_line(55, 186, 455, 186, dash = (4, 4)) 
        self.frame.create_line(55, 230, 455, 230, dash = (4, 4)) 
        self.frame.create_line(55, 277, 455, 277)    
        self.frame.create_line(55, 320, 455, 320, dash = (4, 4)) 
        self.frame.create_line(55, 367, 455, 367, dash = (4, 4)) 
        if self.flag_language == 'ch':
            Button(self.frame, font = ("Purisa", 12), text = '自动求解!', width = 12, height = 1, command =self.solve, fg = '#000000', bg = '#cccc99').place(x = WIDTH / 2, y = 460, anchor = 'center')
            Button(self.frame, font = ("Purisa", 12), text = '求解新题目', width = 12, height = 1, command =self.sudokuSolve, fg = '#000000', bg = '#cccc99').place(x = WIDTH / 4, y = 510, anchor = 'center')
            Button(self.frame, font = ("Purisa", 12), text = '回到主菜单', width = 12, height = 1, command =self.main, fg = '#000000', bg = '#cccc99').place(x = WIDTH * 3 / 4, y = 510, anchor = 'center')
        else:
            Button(self.frame, font = ("Purisa", 12), text = 'slove it!', width = 12, height = 1, command =self.solve, fg = '#000000', bg = '#cccc99').place(x = WIDTH / 2, y = 460, anchor = 'center')
            Button(self.frame, font = ("Purisa", 12), text = 'slove new puzzle', width = 18, height = 1, command =self.sudokuSolve, fg = '#000000', bg = '#cccc99').place(x = WIDTH / 4, y = 510, anchor = 'center')
            Button(self.frame, font = ("Purisa", 12), text = 'return to menu', width = 18, height = 1, command =self.main, fg = '#000000', bg = '#cccc99').place(x = WIDTH * 3 / 4, y = 510, anchor = 'center')
        
        self.frame.pack()
        
    def solve(self):
        values = [one.get() for one in self.blanks]
        all = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        puzzle = []
        for one in values:
            if one in all:
                puzzle.append(int(one))
            elif one == '':
                puzzle.append(0)
            else:
                if self.flag_language == 'ch':
                    tkMessageBox.showwarning("检查题目", "题目中好像出现了奇怪的东西呢，只能填1到9的数字哦")
                else:
                    tkMessageBox.showwarning("check puzzle", "Something wrong with the puzzle, you can only enter the number from 1 to 9")
                return
        if puzzle_verify(puzzle):
            solved = sudoku_solving(puzzle)
        else:
            if self.flag_language == 'ch':
                tkMessageBox.showwarning("检查题目", "题目有错误哦，你可能做到了假数独。。。")
            else:
                tkMessageBox.showwarning("check puzzle", "Something wrong with the puzzle, it may be a fake puzzle...")
            return
            
        if len(solved) == 0:
            if self.flag_language == 'ch':
                tkMessageBox.showwarning("检查题目", "这个题目没有解，你可能做到了假数独。。。")
            else:
                tkMessageBox.showwarning("check puzzle", "Something wrong with the puzzle, it may be a fake puzzle...")
            return
        elif len(solved) > 1:
            if self.flag_language == 'ch':
                tkMessageBox.showwarning("检查题目", "这个题目有多个解，你可能做到了假数独。。。")
            else:
                tkMessageBox.showwarning("check puzzle", "This puzzle has plenty solutions, it may be a fake puzzle...")
            self.showAnswer(solved)
        else:
            self.showAnswer(solved)
    
    def showAnswer(self, solved):
        if (len(solved) == 1):
            newWindow = Tk()
            if self.flag_language == 'ch':
                newWindow.title("参考答案")
            else:
                newWindow.title('answer')
            newWindow.iconbitmap('sudokuIco.ico')
            newFrame = Canvas(newWindow, width = 1000, height = 500, bg = '#eeeebb')
            
            for i in xrange(9):
                for j in xrange(9):
                    if i < 3:
                        pos_x = i*45 + 75
                    if j < 3:
                        pos_y = j*45 + 30
                    if i >= 3 and i < 6:
                        pos_x = i*45 + 75
                    if j >= 3 and j < 6:
                        pos_y = j*45 + 30
                    if i >= 6:
                        pos_x = i*45 + 75
                    if j >= 6:
                        pos_y = j*45 + 30
                    Label(newFrame, width = 3, height = 2, text = str(solved[0][i*9 + j]), fg = '#000000', bg = '#eeeebb').place(x = pos_x, y = pos_y, anchor = 'center')
                    
            newFrame.create_rectangle(55, 10, 455, 410)
            newFrame.create_line(99, 10, 99, 410, dash = (4, 4))
            newFrame.create_line(142, 10, 142, 410, dash = (4, 4))
            newFrame.create_line(187, 10, 187, 410)          
            newFrame.create_line(232, 10, 232, 410, dash = (4, 4))
            newFrame.create_line(278, 10, 278, 410, dash = (4, 4))
            newFrame.create_line(323, 10, 323, 410)    
            newFrame.create_line(369, 10, 369, 410, dash = (4, 4))
            newFrame.create_line(413, 10, 413, 410, dash = (4, 4))
            newFrame.create_line(55, 51, 455, 51, dash = (4, 4)) 
            newFrame.create_line(55, 95, 455, 95, dash = (4, 4)) 
            newFrame.create_line(55, 142, 455, 142)    
            newFrame.create_line(55, 186, 455, 186, dash = (4, 4)) 
            newFrame.create_line(55, 230, 455, 230, dash = (4, 4)) 
            newFrame.create_line(55, 277, 455, 277)    
            newFrame.create_line(55, 320, 455, 320, dash = (4, 4)) 
            newFrame.create_line(55, 367, 455, 367, dash = (4, 4)) 
            
            Button(newFrame, font = ("Purisa", 12), text="OK!", width = 12, height = 1, command = newWindow.destroy, fg = '#000000', bg = '#cccc99').place(x = WIDTH / 2, y = 450, anchor = 'center')
            newFrame.pack()
            newWindow.mainloop()
        
        else:
            newWindow = Tk()
            if self.flag_language == 'ch':
                newWindow.title("部分参考答案")
            else:
                newWindow.title('some answers')
            newWindow.iconbitmap('sudokuIco.ico')
            newFrame = Canvas(newWindow, width = 1000, height = 500, bg = '#eeeebb')
                       
            for i in xrange(9):
                for j in xrange(9):
                    if i < 3:
                        pos_x = i*45 + 75
                    if j < 3:
                        pos_y = j*45 + 30
                    if i >= 3 and i < 6:
                        pos_x = i*45 + 75
                    if j >= 3 and j < 6:
                        pos_y = j*45 + 30
                    if i >= 6:
                        pos_x = i*45 + 75
                    if j >= 6:
                        pos_y = j*45 + 30
                    Label(newFrame, width = 3, height = 2, text = str(solved[0][i*9 + j]), fg = '#000000', bg = '#eeeebb').place(x = pos_x, y = pos_y, anchor = 'center')
            
            newFrame.create_rectangle(55, 10, 455, 410)
            newFrame.create_line(99, 10, 99, 410, dash = (4, 4))
            newFrame.create_line(142, 10,  142, 410, dash = (4, 4))
            newFrame.create_line(187, 10,  187, 410)          
            newFrame.create_line(232, 10,  232, 410, dash = (4, 4))
            newFrame.create_line(278, 10,  278, 410, dash = (4, 4))
            newFrame.create_line(323, 10,  323, 410)    
            newFrame.create_line(369, 10,  369, 410, dash = (4, 4))
            newFrame.create_line(413, 10,  413, 410, dash = (4, 4))
            newFrame.create_line(55,  51,  455, 51, dash = (4, 4)) 
            newFrame.create_line(55,  95,  455, 95, dash = (4, 4)) 
            newFrame.create_line(55,  142, 455, 142)    
            newFrame.create_line(55,  186, 455, 186, dash = (4, 4)) 
            newFrame.create_line(55,  230, 455, 230, dash = (4, 4)) 
            newFrame.create_line(55,  277, 455, 277)    
            newFrame.create_line(55,  320, 455, 320, dash = (4, 4)) 
            newFrame.create_line(55,  367, 455, 367, dash = (4, 4)) 
             
            for i in xrange(9):
                for j in xrange(9):
                    if i < 3:
                        pos_x = i*45 + 575
                    if j < 3:
                        pos_y = j*45 + 30
                    if i >= 3 and i < 6:
                        pos_x = i*45 + 575
                    if j >= 3 and j < 6:
                        pos_y = j*45 + 30
                    if i >= 6:
                        pos_x = i*45 + 575
                    if j >= 6:
                        pos_y = j*45 + 30
                    Label(newFrame, width = 3, height = 2, text = str(solved[1][i*9 + j]), fg = '#000000', bg = '#eeeebb').place(x = pos_x, y = pos_y, anchor = 'center')
                    
            newFrame.create_rectangle(555, 10, 955, 410)
            newFrame.create_line(599, 10,  599, 410, dash = (4, 4))
            newFrame.create_line(642, 10,  642, 410, dash = (4, 4))
            newFrame.create_line(687, 10,  687, 410)          
            newFrame.create_line(732, 10,  732, 410, dash = (4, 4))
            newFrame.create_line(778, 10,  778, 410, dash = (4, 4))
            newFrame.create_line(823, 10,  823, 410)    
            newFrame.create_line(869, 10,  869, 410, dash = (4, 4))
            newFrame.create_line(913, 10,  913, 410, dash = (4, 4))
            newFrame.create_line(555, 51,  955, 51, dash = (4, 4)) 
            newFrame.create_line(555, 95,  955, 95, dash = (4, 4)) 
            newFrame.create_line(555, 142, 955, 142)    
            newFrame.create_line(555, 186, 955, 186, dash = (4, 4)) 
            newFrame.create_line(555, 230, 955, 230, dash = (4, 4)) 
            newFrame.create_line(555, 277, 955, 277)    
            newFrame.create_line(555, 320, 955, 320, dash = (4, 4)) 
            newFrame.create_line(555, 367, 955, 367, dash = (4, 4)) 
            
            Button(newFrame, font = ("Purisa", 12), text = "OK!", width = 12, height = 1, command = newWindow.destroy, fg = '#000000', bg = '#cccc99').place(x = 500, y = 450, anchor = 'center')
            newFrame.pack()
            newWindow.mainloop()
        
        
lock = threading.Lock()
WIDTH = 500
HEIGHT = 550            
app = SudokuGUI()
app.window.mainloop()












