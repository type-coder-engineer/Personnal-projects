#coding: utf
import random
import time
import copy

class my2048:
    def __init__(self, num):
        self.map = [[0 for col in xrange(4)] for row in xrange(4)]
        self.num = num
        pos1_x = pos2_x = random.randint(0, 3)
        pos1_y = pos2_y = random.randint(0, 3)
        while(pos1_x == pos2_x and pos1_y == pos2_y):
            pos2_x = random.randint(0, 3)
            pos2_y = random.randint(0, 3)
        self.map[pos1_x][pos1_y] = self.num
        self.map[pos2_x][pos2_y] = self.num
        return
    
    def action_prove(self):
        origin_map = copy.deepcopy(self.map)
        list_prove = []
        for command in ['up', 'left', 'right', 'down']:
            self.map = copy.deepcopy(origin_map)
            self.action(command)
            if self.map == origin_map:
                pass
            else:
                list_prove.append(command)
        self.map = copy.deepcopy(origin_map)
        return list_prove
        
    def action(self, command):
        if command == 'up' or command == 'w': 
            for col in xrange(4):
                flag_times = 1
                times = 0
                if self.map[0][col] == self.map[1][col] != 0 and self.map[2][col] == self.map[3][col] != 0:
                    flag_times = 2
                for row in xrange(1, 4):
                    if self.map[row][col] != 0:
                        while(row - 1 >= 0 and self.map[row - 1][col] == 0):
                            self.map[row][col], self.map[row - 1][col] = self.map[row - 1][col], self.map[row][col]
                            row -= 1
                        if row - 1 >= 0 and self.map[row - 1][col] == self.map[row][col]:
                            if times < flag_times:
                                self.map[row - 1][col] *= 2
                                self.map[row][col] = 0
                                times += 1
                            else:
                                pass
        elif command == 'left' or command == 'a':
            # print 'left'
            for row in xrange(4):
                flag_times = 1
                times = 0
                if self.map[row][0] == self.map[row][1] != 0 and self.map[row][2] == self.map[row][3] != 0:
                    flag_times = 2
                for col in xrange(1, 4):
                    if self.map[row][col] != 0:
                        while(col - 1 >= 0 and self.map[row][col - 1] == 0):
                            self.map[row][col], self.map[row][col - 1] = self.map[row][col - 1], self.map[row][col]
                            col -= 1
                        if col - 1 >= 0 and self.map[row][col - 1] == self.map[row][col]:
                            if times < flag_times:
                                self.map[row][col - 1] *= 2
                                self.map[row][col] = 0
                                times += 1
                            else:
                                pass
        elif command == 'right' or command == 'd':
            # print 'right'
            for row in xrange(4):
                flag_times = 1
                times = 0
                if self.map[row][0] == self.map[row][1] != 0 and self.map[row][2] == self.map[row][3] != 0:
                    flag_times = 2
                for col in xrange(2, -1, -1):
                    if self.map[row][col] != 0:
                        while(col + 1 <= 3  and self.map[row][col + 1] == 0):
                            self.map[row][col], self.map[row][col + 1] = self.map[row][col + 1], self.map[row][col]
                            col += 1
                        if col + 1 <= 3 and self.map[row][col + 1] == self.map[row][col]:
                            if times < flag_times:
                                self.map[row][col + 1] *= 2
                                self.map[row][col] = 0
                                times += 1
                            else:
                                pass
        elif command == 'down' or command == 's':
            # print 'down'
            for col in xrange(4):
                flag_times = 1
                times = 0
                if self.map[0][col] == self.map[1][col] != 0 and self.map[2][col] == self.map[3][col] != 0:
                    flag_times = 2
                for row in xrange(2, -1, -1):
                    if self.map[row][col] != 0:
                        while(row + 1 <= 3 and self.map[row + 1][col] == 0):
                            self.map[row][col], self.map[row + 1][col] = self.map[row + 1][col], self.map[row][col]
                            row += 1
                        if row + 1 <= 3 and self.map[row + 1][col] == self.map[row][col]:
                            if times < flag_times:
                                self.map[row + 1][col] *= 2
                                self.map[row][col] = 0
                                times += 1
                            else:
                                pass       
        else:
            print 'Wrong command...'
        return 

    def print_array(self):
        for i in xrange(4):
            for j in xrange(4):
                length = len(str(self.map[i][j]))
                print self.map[i][j], ' '*(6 - length),
            print '\n'
        return

    def win(self):
        for i in xrange(4):
            for j in xrange(4):
                if self.map[i][j] == 2048:
                    return True
        return False
                
    def lose(self):
        if not self._isFull():
            return False
        else:
            for i in xrange(4):
                for j in xrange(4):
                    if i - 1 >= 0:
                        if self.map[i - 1][j] == self.map[i][j]:
                            return False
                    if j - 1 >= 0:
                        if self.map[i][j - 1] == self.map[i][j]:
                            return False
                    if i + 1 < 4:
                        if self.map[i + 1][j] == self.map[i][j]:
                            return False
                    if j + 1 < 4:
                        if self.map[i][j + 1] == self.map[i][j]:
                            return False
        return True
    
    def _isFull(self):
        for i in xrange(4):
            for j in xrange(4):
                if self.map[i][j] == 0:
                    return False
        return True
        
    def new_num(self):
        if self._isFull():
            return
        new_x = random.randint(0, 3)
        new_y = random.randint(0, 3)
        while(self.map[new_x][new_y] != 0):
            new_x = random.randint(0, 3)
            new_y = random.randint(0, 3)
        self.map[new_x][new_y] = self.num
        return
    
    def max_nb(self):
        max = 0
        for i in xrange(4):
            for j in xrange(4):
                if max < self.map[i][j]:
                    max = self.map[i][j]
        return max

# 为了算法写的一个2048的子类
class algo2048(my2048):
    def __init__(self, num):
        self.map = [[0 for col in xrange(4)] for row in xrange(4)]
        self.num = num
        
    def new_move(self):
        if self._isFull():
            yield self.map
        else:
            list_blank = []
            for i in xrange(4):
                for j in xrange(4):
                    if self.map[i][j] == 0:
                        list_blank.append((i, j))
                    else:
                        pass
            for one in list_blank:
                new_map = copy.deepcopy(self.map)
                new_map[one[0]][one[1]] = self.num
                yield new_map
        return 
        
# min_max的算法
class algo:
    def __init__(self, blank, average, max, smooth, mono, depth):
    # 关于评价函数参考了网上的一些看法，主要是1.空白格子数量； 2.平均值； 3.最大数字； 
    # 4.平滑性(两个数字之间的差值); 5. 单调性(行列中的数字是否是单调的)   
    
        self.game = my2048(2)
        self.weight_blank = blank
        self.weight_average = average
        self.weight_max = max
        self.weight_smooth = smooth
        self.weight_mono = mono
        self.depth = depth
        return
        
    def evaluate(self, map):
        nb_blank = 0
        max = 0
        sum = 0
        diff = 0
        mono = 0
        mono_x = 0
        mono_y = 0
        for i in xrange(4):
            for j in xrange(3):
                if map[i][j] <= map[i][j + 1]:
                    mono_y += 1
                else:
                    mono_y -= 1
        for i in xrange(4):
            for j in xrange(3):
                if map[j][i] <= map[j + 1][i]:
                    mono_x += 1
                else:
                    mono_x -= 1
        mono += (abs(mono_x) + abs(mono_y))
        for i in xrange(4):
            for j in xrange(4):
                sum += map[i][j]
                if map[i][j] == 0:
                    nb_blank += 1
                if map[i][j] > max:
                    max = map[i][j]
                if i < 3 and j < 3:
                    diff += abs(map[i][j] - map[i + 1][j])
                    diff += abs(map[i][j] - map[i][j + 1])
        return self.weight_blank * nb_blank + self.weight_max * max + \
        self.weight_average * sum / (16 - nb_blank) + self.weight_smooth * diff\
        + self.weight_mono * mono     
          
    # 我递归的深度定的是5，因为3的话太浅，但是增加到7没有提高很多正确率，时间却变成了8倍
    def mini_max(self, strategie, depth):
        score_list = []
        if depth == 1:
            origin = copy.deepcopy(strategie.map)
            for command in ['up', 'left', 'right', 'down']:
                strategie.map = copy.deepcopy(origin)
                strategie.action(command)
                score_list.append(self.evaluate(strategie.map))     
                # print score_list
            return max(score_list)
        
        else:
            if depth % 2 == 0:
                for new_map in strategie.new_move():
                    strategie.map = new_map
                    score_list.append(self.mini_max(strategie, depth - 1))
                # print 'PC move'
                # print 'depth', depth
                # print score_list
                return sum(score_list) / len(score_list)
                # return min(score_list)
# 这里我其实用的是max_average算法，因为电脑是随机出现2的，所以用min_max会过于保守
# 在同一种参数下这个算法成功率是70% 而 min_max是25%
        
            else:
                origin = copy.deepcopy(strategie.map)
                for command in ['up', 'left', 'right', 'down']:
                    strategie.map = copy.deepcopy(origin)
                    strategie.action(command)
                    if strategie.win():
                        score_list.append(999999*depth) # *深度可以得到不同的优先度
                    elif strategie.lose():
                        score_list.append(-9999*depth)
                    else:
                        score_list.append(self.mini_max(strategie, depth - 1))
                # print 'my move'
                # print 'depth', depth
                # print score_list
                if depth != self.depth:
                    return max(score_list)
                else:
                    list_command = []
                    options = ['up', 'left', 'right', 'down']
                    # print score_list
                    for i in xrange(4):
                        index = score_list.index(max(score_list))
                        list_command.append(options[index])
                        score_list.pop(index)   
                        options.pop(index)
                    return list_command
        
    def main(self):
        while(1):
            if self.game.win():
                print 'Won'
                self.game.print_array()
                return 1
            elif self.game.lose():
                print 'Lost'
                self.game.print_array()
                return 0

            strategie = algo2048(2)
            strategie.map = copy.deepcopy(self.game.map)
            command = self.mini_max(strategie, self.depth) 
            proved_command = self.game.action_prove()
            index = 0
            while(command[index] not in proved_command):
                index += 1
                
            self.game.action(command[index])
            self.game.new_num()   

    # 每一步都停下来看看结果
    def present(self):
        print 'The map at very first:\n'
        while(1):
            if self.game.win():
                print '*************************'
                print '\n'
                print 'Won'
                self.game.print_array()
                return 1
            elif self.game.lose():
                print '*************************'
                print '\n'
                print 'Lost'
                self.game.print_array()
                return 0
            self.game.print_array()
            # raw_input()
            strategie = algo2048(2)
            strategie.map = copy.deepcopy(self.game.map)
            command = self.mini_max(strategie, self.depth) 
            proved_command = self.game.action_prove()
            index = 0

            while(command[index] not in proved_command):
                index += 1
            print 'Our move is {}. Now the map is:\n'.format(command[index])
            self.game.action(command[index])
            self.game.print_array()
            raw_input()
            self.game.new_num()   
            print 'The new number appears:\n'

    def noLimit(self):
        while(1):
            if self.game.lose():
                print 'Game over, your final map is:'
                self.game.print_array()
                print 'Your biggest number is {}'.format(self.game.max_nb())
                return self.game.max_nb()

            strategie = algo2048(2)
            strategie.map = copy.deepcopy(self.game.map)
            command = self.mini_max(strategie, self.depth) 
            proved_command = self.game.action_prove()
            index = 0
            while(command[index] not in proved_command):
                index += 1
                
            self.game.action(command[index])
            self.game.new_num()   

# 用循环找到好的权重参数
def find_parameters():
    total_times = 10
    _blank = 10
    _average = 15
    _max = 1
    _smooth = -0.1
    _mono = 100
    blank_step = 2
    average_step = 2
    max_step = 0.3
    smooth_step = 0.03
    mono_step = 10
    res_dic = {}
    for blank in xrange(_blank - 4, _blank + 5, blank_step):
        for average in xrange(_average - 4, _average + 5, average_step):
            for max in xrange(_max - 0.5, _max + 0.6, max_step):
                for smooth in xrange(_smooth - 0.03, _smooth + 0.07, smooth_step):
                    for mono in xrange(_mono - 20, _mono + 21, mono_step):
                        highest = 0
                        for i in xrange(total_times):
                            projet = algo(blank, average, max, smooth, mono, 5)
                            final = projet.main()
                            highest += final
                        res_dic[(blank, average, max, smooth)] = highest
    # print 'The final points are {}'.format(highest)
    # print 'It has won {} times'.format(times_won)
    save_file(res_dic, 'res_test.txt')
    values = res_dic.values()
    values.sort()
    for high_value in values[-10:]:
        for key, value in res_dic.items():
            if value == high_value:
                print key
                print value
                print '************'
    return 
    
if __name__ == '__main__':
    start = time.time()
    project = algo(blank = 10, average = 15, max = 1, smooth = -0.1, mono = 100, depth = 5)
    project.main()
    '''
    times = 0
    for game in xrange(20):
        projet = algo(blank = 10, average = 15, max = 1, smooth = -0.1, mono = 100, depth = 5)
        if projet.main():
            times += 1
    print 'These parameters have won {} times by {} times'.format(times, 20)
    '''  
    end = time.time()
    print 'It took {} seconds'.format(end - start)
    
    