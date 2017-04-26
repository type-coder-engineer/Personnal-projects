# coding: utf
from Tkinter import * 
import tkMessageBox 
import ttk
from sudoku_class import *
import time
import threading

class SudokuGUI:
    def __init__(self):
        self.window = Tk()
        self.window.minsize(width = WIDTH, height = HEIGHT)
        self.window.title("数独世界") 
        self.frame = Frame(self.window, width = WIDTH, height = HEIGHT)
        Label(self.frame, font = ("Purisa", 22), text = "欢迎来到数独世界！").place(x = WIDTH / 2, y = 60, anchor = 'center')
        Label(self.frame, font = ("Purisa", 10), text = "作者: 张辰宇").place(x = WIDTH / 2, y = 110, anchor = 'center')
        Label(self.frame, font = ("Purisa", 10), text = "欢迎来我的github主页逛逛: https://github.com/type-coder-engineer").place(x = WIDTH / 2, y = 130, anchor = 'center')
        
        Label(self.frame, font = ("Purisa", 12), text = '数独难度：').place(x = 120, y = 280, anchor = 'center')
        self.level = StringVar()
        self.level.set("median") # 默认初始值
        ttk.Combobox(self.frame, textvariable = self.level, values = ["easy", "median", "hard"]).place(x = WIDTH / 2, y = 280, anchor = 'center')
        Button(self.frame, font = ("Purisa", 15), text = '数独题目', width = 12, height = 2, command = self.sudokuPuzzleWait).place(x = WIDTH / 3, y = 220, anchor = 'center')
        Button(self.frame, font = ("Purisa", 15), text = '挑战模式', width = 12, height = 2, command = self.sudokuChallengeWait).place(x = WIDTH * 2 / 3, y = 220, anchor = 'center')
        Button(self.frame, font = ("Purisa", 15), text = '解数独', width = 12, height = 2, command = self.sudokuSolve).place(x = WIDTH / 2, y = 370, anchor = 'center')
        self.frame.pack()
        
        self.puzzleEasyReady = False
        self.puzzleMedianReady = False
        self.puzzleHardReady = False
        th_puzzle = threading.Thread(target = self.generatePuzzle) # 一个线程用来生成这个puzzle
        th_puzzle.setDaemon(True)
        th_puzzle.start()
        
    def returnMain(self):
        self.frame.destroy()
        self.flag_count = False
        self.frame = Frame(self.window, width = WIDTH, height = HEIGHT)
        Label(self.frame, font = ("Purisa", 22), text = "欢迎来到数独世界！").place(x = WIDTH / 2, y = 60, anchor = 'center')
        Label(self.frame, font = ("Purisa", 10), text = "作者: 张辰宇").place(x = WIDTH / 2, y = 110, anchor = 'center')
        Label(self.frame, font = ("Purisa", 10), text = "欢迎来我的github主页逛逛: https://github.com/type-coder-engineer").place(x = WIDTH / 2, y = 130, anchor = 'center')
        
        Label(self.frame, font = ("Purisa", 12), text = '数独难度：').place(x = 120, y = 280, anchor = 'center')
        self.level = StringVar()
        self.level.set("median") # 默认初始值
        ttk.Combobox(self.frame, textvariable = self.level, values = ["easy", "median", "hard"]).place(x = WIDTH / 2, y = 280, anchor = 'center')
        Button(self.frame, font = ("Purisa", 15), text = '数独题目', width = 12, height = 2, command = self.sudokuPuzzleWait).place(x = WIDTH / 3, y = 220, anchor = 'center')
        Button(self.frame, font = ("Purisa", 15), text = '挑战模式', width = 12, height = 2, command = self.sudokuChallengeWait).place(x = WIDTH * 2 / 3, y = 220, anchor = 'center')
        Button(self.frame, font = ("Purisa", 15), text = '解数独', width = 12, height = 2, command = self.sudokuSolve).place(x = WIDTH / 2, y = 370, anchor = 'center')
        self.frame.pack()
        
    def sudokuPuzzleWait(self):
        self.frame.destroy()
        self.frame = Frame(self.window, width = WIDTH, height = HEIGHT)
        Label(self.frame, font = ("Purisa", 22), text = "正在生成题目").place(x = 150, y = 200, anchor = SW)
        self.frame.pack()
        th_animation = threading.Thread(target = self.signalPuzzleWait) # 另一个线程用来产生动画效果
        th_animation.setDaemon(True)
        th_animation.start()
        
    def sudokuChallengeWait(self):
        self.frame.destroy()
        self.frame = Frame(self.window, width = WIDTH, height = HEIGHT)
        Label(self.frame, font = ("Purisa", 22), text = "正在生成题目").place(x = 150, y = 200, anchor = SW)
        self.frame.pack()
        th_animation = threading.Thread(target = self.signalChallengeWait) # 另一个线程用来产生动画效果
        th_animation.setDaemon(True)
        th_animation.start()
        
    def animationWait(self, index):
        self.frame.destroy()
        self.frame = Frame(self.window, width = WIDTH, height = HEIGHT)
        if index % 4 == 0:
            Label(self.frame, font = ("Purisa", 22), text = "正在生成题目。。。").place(x = 150, y = 200, anchor = SW)
        elif (index + 1) % 4 == 0:
            Label(self.frame, font = ("Purisa", 22), text = "正在生成题目。。").place(x = 150, y = 200, anchor = SW)
        elif (index + 2) % 4 == 0:
            Label(self.frame, font = ("Purisa", 22), text = "正在生成题目。").place(x = 150, y = 200, anchor = SW)
        else:
            Label(self.frame, font = ("Purisa", 22), text = "正在生成题目").place(x = 150, y = 200, anchor = SW)
        self.frame.pack()
    
    def signalPuzzleWait(self):
        index = 2
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
        Label(self.frame, font = ("Purisa", 22), text = "您选择了挑战模式").place(x = WIDTH / 2, y = 130, anchor = 'center')
        Label(self.frame, font = ("Purisa", 22), text = "点击确认后就会开始计时").place(x = WIDTH / 2, y = 180, anchor = 'center')
        Button(self.frame, font = ("Purisa", 15), text = '确认挑战', width = 12, height = 2, command = self.sudokuChallengeShow).place(x = WIDTH / 2, y = 280, anchor = 'center')
        Button(self.frame, font = ("Purisa", 15), text = '回到主菜单', width = 12, height = 2, command = self.returnMain).place(x = WIDTH / 2, y = 370, anchor = 'center')    
        self.frame.pack()
        
    def generatePuzzle(self):
        lock.acquire()
        try:
            self.final = sudoku_final()
            self.puzzleEasy = sudoku_puzzle(self.final, 1)
            self.puzzleEasyReady = True
            # print '1ok'
            self.puzzleMedian = sudoku_puzzle(self.final, 2)
            self.puzzleMedianReady = True
            # print '2ok'
            self.puzzleHard = sudoku_puzzle(self.final, 3) 
            self.puzzleHardReady = True
            # print '3ok'
        finally:
            lock.release()
      
    def sudokuPuzzleShow(self):
        self.frame.destroy()
        self.frame = Canvas(self.window, width = 500, height = 550) # 注意如果是place的话要先确定好frame的尺寸
        if self.level.get() == 'easy':
            self.puzzle = self.puzzleEasy[:]
        elif self.level.get() == 'median':
            self.puzzle = self.puzzleMedian[:]
        else:
            self.puzzle = self.puzzleHard[:]
            
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
                    Label(self.frame, width = 3, height = 2, text = str(self.puzzle[i*9 + j])).place(x = pos_x, y = pos_y, anchor = 'center')
                    
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
        
        Button(self.frame, font = ("Purisa", 12), text = '提交', width = 12, height = 1, command = self.submit).place(x = 150, y = 460, anchor = 'center')
        Button(self.frame, font = ("Purisa", 12), text = '答案', width = 12, height = 1, command = self.getAnswer).place(x = 350, y = 460, anchor = 'center')
        Button(self.frame, font = ("Purisa", 12), text = '新数独', width = 12, height = 1, command = self.sudokuPuzzleWait).place(x = 150, y = 520, anchor = 'center')
        Button(self.frame, font = ("Purisa", 12), text = '回到主菜单', width = 12, height = 1, command = self.returnMain).place(x = 350, y = 520, anchor = 'center')
        self.frame.pack()
        # print 'new'
        self.puzzleEasyReady = False
        self.puzzleMedianReady = False
        self.puzzleHardReady = False
        th_puzzle = threading.Thread(target = self.generatePuzzle) # 一个线程用来生成这个puzzle
        th_puzzle.setDaemon(True)
        th_puzzle.start()
        
    def sudokuChallengeShow(self):
        self.start = time.time()
        self.count = 0
        self.flag_count = True
        self.flag_count_timeOut = False
        self.frame.destroy()
        self.frame = Canvas(self.window, width = 500, height = 550) 
        if self.level.get() == 'easy':
            self.puzzle = self.puzzleEasy[:]
        elif self.level.get() == 'median':
            self.puzzle = self.puzzleMedian[:]
        else:
            self.puzzle = self.puzzleHard[:]
        
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
                    Label(self.frame, width = 3, height = 2, text = str(self.puzzle[i*9 + j])).place(x = pos_x, y = pos_y, anchor = 'center')
                    
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
        
        Label(self.frame, font = ("Purisa", 12), text = '已用时： ').place(x = WIDTH / 2 - 60, y = 440, anchor = 'center')
        self.label_count = Label(self.frame, font = ("Purisa", 14), text = str(self.count))
        self.label_count.place(x = WIDTH / 2, y = 440, anchor = 'center')
        Label(self.frame, font = ("Purisa", 12), text = ' 秒').place(x = WIDTH / 2 + 40, y = 440, anchor = 'center')
        
        Button(self.frame, font = ("Purisa", 12), text = '提交', width = 12, height = 1, command = self.submitChallenge).place(x = 150, y = 480, anchor = 'center')
        Button(self.frame, font = ("Purisa", 12), text = '答案', width = 12, height = 1, command = self.getAnswer).place(x = 350, y = 480, anchor = 'center')
        Button(self.frame, font = ("Purisa", 12), text = '新数独', width = 12, height = 1, command = self.sudokuChallengeWait).place(x = 150, y = 530, anchor = 'center')
        Button(self.frame, font = ("Purisa", 12), text = '回到主菜单', width = 12, height = 1, command = self.returnMain).place(x = 350, y = 530, anchor = 'center')
        self.frame.pack()
        
        self.puzzleEasyReady = False
        self.puzzleMedianReady = False
        self.puzzleHardReady = False
        th_puzzle = threading.Thread(target = self.generatePuzzle) # 一个线程用来生成这个puzzle
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
        self.label_count = Label(self.frame, font = ("Purisa", 14), text = str(self.count))
        self.label_count.place(x = WIDTH / 2, y = 440, anchor = 'center')
        
    def submit(self):
        values = [one.get() for one in self.blanks]
        response = []
        all = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        for one in values:
            if one in all:
                response.append(int(one))
        
        if len(self.answer) != len(response):
            tkMessageBox.showwarning("检查答案", "还有漏填的空哦。。。")
            return
            
        if self.answer == response:
            tkMessageBox.showinfo("检查答案","棒极了，答案完全正确！")
        else:
            tkMessageBox.showwarning("检查答案", "答案有错误哦。。。")
        return  
 
    def submitChallenge(self):
        values = [one.get() for one in self.blanks]
        response = []
        all = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        for one in values:
            if one in all:
                response.append(int(one))
        
        if len(self.answer) != len(response):
            tkMessageBox.showwarning("检查答案", "还有漏填的空哦。。。")
            return
            
        if self.answer == response:
            self.flag_count = False
            text = "棒极了，答案完全正确！花费了 {} 秒完成 ".format(self.count)
            tkMessageBox.showinfo("检查答案", text)
        else:
            tkMessageBox.showwarning("检查答案", "答案有错误哦。。。")
        return  
        
    def getAnswer(self):
        self.flag_count_timeOut = True
        flag = tkMessageBox.askokcancel(message = "你真的想看答案吗?") 
        if flag:
            pass
        else:
            self.flag_count_timeOut = False
            return
        newWindow = Tk()
        newWindow.title("参考答案")
        newFrame = Canvas(newWindow, width = 500, height = 500)
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
                Label(newFrame, width = 3, height = 2, text = str(self.final[i*9 + j])).place(x = pos_x, y = pos_y, anchor = 'center')
                
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
                
        Button(newFrame, font = ("Purisa", 12), text="OK !", width = 12, height = 1, command = newWindow.destroy).place(x = WIDTH / 2, y = 450, anchor = 'center')
        newFrame.pack()
        newWindow.mainloop()
        
    def sudokuSolve(self):
        self.frame.destroy()  
        self.frame = Canvas(self.window, width = 500, height = 550)
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
                
        Button(self.frame, font = ("Purisa", 12), text = '自动求解!', width = 12, height = 2, command =self.solve).place(x = WIDTH / 2, y = 450, anchor = 'center')
        Button(self.frame, font = ("Purisa", 12), text = '求解新题目', width = 12, height = 2, command =self.sudokuSolve).place(x = WIDTH / 4, y = 510, anchor = 'center')
        Button(self.frame, font = ("Purisa", 12), text = '回到主菜单', width = 12, height = 2, command =self.returnMain).place(x = WIDTH * 3 / 4, y = 510, anchor = 'center')
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
                tkMessageBox.showwarning("检查题目", "题目中好像出现了奇怪的东西呢，只能填1到9的数字哦")
                return
        if puzzle_verify(puzzle):
            solved = sudoku_solving(puzzle)
        else:
            tkMessageBox.showwarning("检查题目", "题目有错误哦，你可能做到了假数独。。。")
            return
            
        if len(solved) == 0:
            tkMessageBox.showwarning("检查题目", "这个题目没有解，你可能做到了假数独。。。")
            return
        elif len(solved) > 1:
            tkMessageBox.showwarning("检查题目", "这个题目有多个解，你可能做到了假数独。。。")
        else:
            newWindow = Tk()
            newWindow.title("参考答案")
            newFrame = Canvas(newWindow, width = 500, height = 500)
            
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
                Label(newFrame, width = 3, height = 2, text = str(solved[0][i*9 + j])).place(x = pos_x, y = pos_y, anchor = 'center')
                
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
        
        Button(newFrame, font = ("Purisa", 12), text="OK !", width = 12, height = 1, command = newWindow.destroy).place(x = WIDTH / 2, y = 450, anchor = 'center')
        newFrame.pack()
        newWindow.mainloop()

lock = threading.Lock()
WIDTH = 500
HEIGHT = 550            
app = SudokuGUI()
app.window.mainloop()