# coding: utf
import random
import time

# 获得一个随机的选择
def shuffling(all):
    new_list = all[:]
    for index in xrange(1, len(all)):
        index_exc = random.randint(0, index)
        new_list[index], new_list[index_exc] = new_list[index_exc], new_list[index]
    return new_list

# 将map打印出来
def print_map(map):
    print '-'*45
    print '|',
    for index in xrange(81):
        if map[index] != 0:
            print map[index], '|',
        else:
            print ' ', '|',
        if (index + 1) % 3 == 0 and (index + 1) % 9 != 0:
            print ', |', 
        if (index + 1) % 9 == 0 and (index + 1) % 27 != 0:
            print ''
            print '- '*23
            print '|',
        if (index + 1) % 27 == 0:
            print ' '
            print '-'*45
            if index != 80:
                print '-'*45
                print '|',
    return
 
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
    map = [0 for pos in xrange(81)]
    map[:9] = shuffling(all) # 注意这里是map[:9]!! 一开始写成:10了，导致map的长度被我减了1
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
    for row in xrange(9):
        list_col = []
        for col in xrange(9):
            if puzzle[row*9 + col] == 0:
                pass
            else:
                if puzzle[row*9 + col] in list_col:
                    return False
                else:
                    list_col.append(puzzle[row*9 + col])
    for col in xrange(9):
        list_row = []
        for row in xrange(9):
            if puzzle[row*9 + col] == 0:
                pass
            else:
                if puzzle[row*9 + col] in list_row:
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
    if not puzzle_verify(puzzle):
        print 'Not a valid puzzle...'
        return
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
    print_map(origin)
    
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
    if len(map_solved) == 1:
        print_map(map_solved[0])
    elif len(map_solved) > 1:
        for index in xrange(len(map_solved)):
            print_map(map_solved[index])
            print '***************'
        print 'Not unique solution'
    else:
        print 'No solution...'
    return

# 从'puzzle.txt'文件得到数独题目   
def get_puzzle():
    puzzle = []
    target = open('puzzle.txt')
    for line in target:
        line.strip('\n')
        content = line.split(' ')
        for one in content:
            if one != ' ' and one != '':
                puzzle.append(int(one))
    # print puzzle
    return puzzle

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
                        if index == blank_nb:
                            flag_over = True
                    else:
                        first_option = one[:]
                        break
                if flag_over:
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
def sudoku_puzzle(level):
    if level != 1 and level != 2 and level != 3:
        print 'Invalid level...'
        return
    print 'Generating the puzzle...'
    map_final = sudoku_final()
    save_answer(map_final)
    puzzle = dibble(map_final, level)
    list_notGood = []
    print 'Testing this puzzle, please wait...\n'
    while (not sudoku_verify(puzzle)):
        list_notGood.append(puzzle)
        while(puzzle in list_notGood):
            puzzle = dibble(map_final, level)
    print 'Here is your puzzle, have fun!\n'
    return puzzle

# 生成题目的同时将答案保存到'answer.txt'文件中参考
def save_answer(final):
    target = open('answer.txt','w')
    for index in xrange(81):
        target.write(str(final[index]))
        target.write('  ')
        if (index + 1) % 9 == 0 and index != 80:
            target.write('\n')
    target.close()
    return 
    
if __name__ == '__main__':
    start = time.time()
    # sudoku_solving(get_puzzle())
    print_map(sudoku_puzzle(1))
    end = time.time()
    print "it took {} seconds".format(end - start)
    