# -*- coding: utf-8 -*- 

# the order of the dict: year, author, ISBN, title
# I used the Python 2.7 to do the coding

'''
帮大锤做的一份作业，当时觉得做的还不错，现在看看简直血崩。。。
当时还为了去掉读取string后多出来的引号绞尽脑汁想了一个好奇怪的方法，
现在知道可以直接eval()了
'''

import os
#for the test
# book1 = {'ISBN': '12345678', 'title':'Gone with the wind', 'author': 'Margaret Mitchell', 'year': '1936' }
# book2 = {'ISBN': '12345679', 'title':'Harry Potter', 'author': 'J. K. Rowling ', 'year': '1997' }

# the class of the book
class Book():
# define a book by 4 arguments
    def __init__(self, year, author, ISBN, title):
        self.year = year
        self.author = author 
        self.ISBN = ISBN 
        self.title = title
        self.info = {"year": self.year, 'author': self.author, 'ISBN': self.ISBN, 'title': self.title}
    
#the class of the database
class Database():
    def __init__(self):
        self.book_list = []

# to choose the function you want        
    def choose(self):
       # to choose a function to run
        choice = raw_input("Please tap in 'add'; 'search'; 'remove'; 'load'; 'save' or 'info' to give your order\n")
        while choice.strip() != 'add' and choice.strip() != 'search' and choice.strip() != 'remove' and choice.strip() != 'load' and choice.strip() != 'save' and choice.strip() != 'info':
            print "I don't understand your order...."
            choice = raw_input("Please tap in 'add'; 'search'; 'remove'; 'load' or 'save' to give your order\n")
        return choice.strip()
 
# switch the function 
    def functions(self, argument):
        if argument == 'add':
            self.add()
        if argument == 'search':
            self.search()
        if argument == 'remove':
            self.remove()
        if argument == 'load':
            self.load()
        if argument == 'save':
            self.save()    
        if argument == 'info':
            self.info()
 
# the function to add a book in the database 
    def add(self):
        add = 'yes'
        while (add == 'yes'):
            print "Please give me the infomations of this book added:"
            # to enter the infomations
            check = ''
            while check != 'ok':
                year = raw_input("The published year?\n").strip()  # to make sure we have all the info needed
                while (year == ''):
                    print "No blank space, we have no Taylor Swift here" # just a joke
                    year = raw_input("The published year?\n").strip()
                    
                author = raw_input("The author?\n").strip()
                while (author == ''):
                    print "No blank space, we have no Taylor Swift here"
                    author = raw_input("The author?\n").strip()
                    
                ISBN = raw_input("The ISBN?\n").strip()
                while (ISBN == ''):
                    print "No blank space, we have no Taylor Swift here"
                    ISBN = raw_input("The ISBN?\n").strip()
                    
                title = raw_input("The title?\n").strip()
                while (title == ''):
                    print "No blank space, we have no Taylor Swift here"
                    title = raw_input("The title?\n").strip()
                
                print "\n"
                print "Please read the infomations to check. If it's ok, enter 'ok' to continue; tap other key to rewrite the informations"
                check = raw_input("year: " + year + " ; " + "author: " + author + " ; " + "ISBN: " + ISBN + " ; " + "title: " + title + ".\n")        
            
            # check if there is already a book with the same ISBN or title
            flag_new = 1
            if len(self.book_list) != 0:
                for book in self.book_list:
                    if ISBN == book.get("ISBN"):
                        print "We have already a book with the same ISBN as you can see, so we can't add this book, sorry..."
                        print book
                        print "\n"
                        flag_new = 0
                    if title == book.get("title"):
                        print "We have already a book with the same title as you can see, so we can't add this book, sorry..."
                        print book
                        print "\n"
                        flag_new = 0
                        
            # to create a new object and append in the book_list
            if flag_new == 1:
                newbook = Book(year, author, ISBN, title)
                self.book_list.append(newbook.info)
                del newbook
                print "The adding is done!"
                print "\n"
            
            add = raw_input("Do you have another book to add? Tap 'yes' if you do, any other key to get back to the main menu\n ")    
            
        os.system("cls")
        return 

# the function to search the book and show the infomations        
    def search(self):
        if len(self.book_list) == 0:
            print "Now you have nothing in the database, please try the functioin 'add' or 'load'.\n"
            return
            
        else:
            search = "yes"
            while (search == "yes"):
                key = raw_input("Please give me the ISBN or the title of the book you want to find\n")
                flag_found = 0
                for book in self.book_list:
                    if key == book.get("ISBN") or key == book.get("title"):
                        flag_found = 1
                        print "Your book is found"
                        print book
                        print "\n"
                        search = raw_input("You have another book to search? Tap 'yes' if you do, any other key to get back to the main menu\n")
                        
                if flag_found == 0:
                    print "Sorry your book is not found...."
                    print "\n"  
                    search = raw_input("You have another book to search? Tap 'yes' if you do, any other key to get back to the main menu\n")
              
            os.system("cls")
            return     

# the function to remove the book from the database
    def remove(self):
        if len(self.book_list) == 0:
            print "Now you have nothing in the database, please try the functioin 'add' or 'load'.\n"
            return
            
        else:
            remove = "yes"
            while (remove == "yes"):
                key = raw_input("Please give me the ISBN or the title of the book you want to remove\n")
                flag_found = 0
                # search the book by ISBN or title
                for book in self.book_list:  
                    if key == book.get("ISBN") or key == book.get("title"):
                        flag_found = 1
                        print "Your book is found"
                        print book
                        confirm = raw_input("You confirm the delete? Tap 'yes' to delete, any other key to undo\n")
                        if confirm == 'yes':
                            self.book_list.remove(book)  # remove the book
                        search = raw_input("You have another book to remove? Tap 'yes' if you do, any other key to get back to the main menu\n")
                        
                if flag_found == 0:
                    print "Sorry your book is not found...."
                    print "\n"  
                    remove = raw_input("You have another book to remove? Tap 'yes' if you do, any other key to get back to the main menu\n")
            
            os.system("cls")
            return              
 
#to load the file to the database 
    def load(self):
        print "You should put the file in the same folder and then tap in the name of this file"
        filename = raw_input("The file to load?\n")
        while not os.path.isfile(filename): # to make sure we have the file in the path
            print "The file is not found, please check if there is something wrong, tap 'menu' to get back to the main menu"
            filename = raw_input("The file to load?\n")
            if filename == "menu":
                return
        
        target = open(filename, 'r') # to read the file
        book_repeat = []
        while(1):
            line = target.readline()  # to treat line per line
            if not line:
                break
            else:
                line = line.lstrip('"{')
                line = line.rstrip('}\n')
                book_info = []
                for one in line.split(','):  # to get each info 
                    book_info.append(one)
                    
                # here we must use .strip(' \' ') to get rid of the '' around the info, or we can't have the right format
                year = book_info[3].split(':')[1].strip().strip(' \' ')
                author = book_info[1].split(':')[1].strip().strip(' \' ')
                ISBN = book_info[2].split(':')[1].strip().strip(' \' ')
                title = book_info[0].split(':')[1].strip().strip(' \' ')
                newbook = Book(year, author, ISBN, title)

                # we have a list "book_repeat" to store the book with repeating ISBN or title
                flag_new = 1 
                if len(self.book_list) != 0:
                    for book in self.book_list:
                        if ISBN == book.get("ISBN"):
                            book_repeat.append(book)
                            book_repeat.append(newbook.info)
                            book_repeat.append("****************************")
                            flag_new = 0
                        if title == book.get("title"):
                            book_repeat.append(book)
                            book_repeat.append(newbook.info)
                            book_repeat.append("****************************")                            
                            flag_new = 0
                            
                if flag_new == 1:
                    self.book_list.append(newbook.info)
                del newbook 
                
        target.close() # close the file 
        if len(book_repeat) != 0:
            print "There are some repeating books you need to modify and add to the database manually"
            for one in book_repeat:
                print one
                
        return
                
# to save the database to a file        
    def save(self):
        if len(self.book_list) == 0:
            print "Now you have nothing in the database, please try the functioin 'add' or 'load'.\n"
            return
            
        else:
            filename = raw_input('Please give a name for the file holding the data\n').strip()
            while filename == '':
                print "There must be a  filename"
                filename = raw_input("Please give a name for the file holding the data\n").strip()
            
            target = open(filename, 'w') # open a file to write
            for book in self.book_list: 
                target.write(str(book))  # turn to string to write
                target.write("\n")
            
            target.close()
            print "The saving is done!"
            return 
            
# to show all the books in the database        
    def info(self):
        if len(self.book_list) == 0:
            print "Now you have nothing in the database, please try the functioin 'add' or 'load'.\n"
            return    
            
        else:
            print "You have " + str(len(self.book_list)) + " book(s) in your database for now:"
            for book in self.book_list:
                print book
                print '\n'
            return
        
if __name__ == '__main__':
    os.system('cls')
    myDatabase = Database()

    print "Welcome to the book database!"
    print "You can choose from the functions: 1.add a book; 2.search the book; 3.remove a book; 4.load a database; 5.save the database; 6.see all the infomations of the database. If you are done, use 'Ctrl + c' to get out"
    while(1):
        choice = myDatabase.choose()
        myDatabase.functions(choice)
        