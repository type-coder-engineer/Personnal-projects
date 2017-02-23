#include "app.h"
#include "mainwindow.h"
#include <iostream>
#include <time.h>
#include <cstdlib>
#include <algorithm>
#include <stdlib.h>
#include <vector>

using std::vector;

// 上下左右移动的算法
bool app_2048::calculate_up(){
    bool action = false;
    for (int col = 0; col != L; ++col){
        int flag_times = 1;
        int times = 0;
        if (map[0][col] == map[1][col] && map[1][col] != 0 && map[2][col] == map[3][col] && map[3][col] != 0)
            flag_times = 2;
        for (int row = 1; row != H; ++row){
            if (map[row][col] != 0){
                while((row - 1 >= 0) && (map[row - 1][col] == 0)){
                    action = true;
                    swap(map[row][col], map[row - 1][col]);
                    --row;
                }
                if ((row - 1 >= 0) && (map[row - 1][col] == map[row][col])){
                    if (times < flag_times){
                        action = true;
                        map[row - 1][col] *= 2;
                        map[row][col] = 0;
                        times += 1;
                    }
                }
            }
        }
    }
    return action;
}

bool app_2048::calculate_down(){
    bool action = false;
    for (int col = 0; col != L; ++col){
        int flag_times = 1;
        int times = 0;
        if (map[0][col] == map[1][col] && map[1][col] != 0 && map[2][col] == map[3][col] && map[3][col] != 0)
            flag_times = 2;
        for (int row = H - 2; row != -1; --row){
            if (map[row][col] != 0){
                while((row + 1 <= H - 1) && (map[row + 1][col] == 0)){
                    action = true;
                    swap(map[row][col], map[row + 1][col]);
                    ++row;
                }
                if ((row + 1 <= H - 1) && (map[row + 1][col] == map[row][col])){
                    if (times < flag_times){
                        action = true;
                        map[row + 1][col] *= 2;
                        map[row][col] = 0;
                        times += 1;
                    }
                }
            }
        }
    }
    return action;
}

bool app_2048::calculate_left(){
    bool action = false;
    for (int row = 0; row != H; ++row){
        int flag_times = 1;
        int times = 0;
        if (map[row][0] == map[row][1] && map[row][1] != 0 && map[row][2] == map[row][3] && map[row][3] != 0)
            flag_times = 2;
        for (int col = 1; col != L; ++col){
            if (map[row][col] != 0){
                while((col - 1 >= 0) && (map[row][col - 1] == 0)){
                    action = true;
                    swap(map[row][col], map[row][col - 1]);
                    --col;
                }
                if ((col - 1 >= 0) && (map[row][col - 1] == map[row][col])){
                    if (times < flag_times){
                        action = true;
                        map[row][col - 1] *= 2;
                        map[row][col] = 0;
                        times += 1;
                    }
                }
            }
        }
    }
    return action;
}

bool app_2048::calculate_right(){
    bool action = false;
    for (int row = 0; row != H; ++row){
        int flag_times = 1;
        int times = 0;
        if (map[row][0] == map[row][1] && map[row][1] != 0 && map[row][2] == map[row][3] && map[row][3] != 0)
            flag_times = 2;
        for (int col = L - 2; col != -1; --col){
            if (map[row][col] != 0){
                while((col + 1 <= L - 1) && (map[row][col + 1] == 0)){
                    action = true;
                    swap(map[row][col], map[row][col + 1]);
                    ++col;
                }
                if ((col + 1 <= L - 1) && (map[row][col + 1] == map[row][col])){
                    if (times < flag_times){
                        action = true;
                        map[row][col + 1] *= 2;
                        map[row][col] = 0;
                        times += 1;
                    }
                }
            }
        }
    }
    return action;
}
//**************************************************
bool app_2048::isFull(){
    for (int row = 0; row != H; ++row){
        for (int col = 0; col != L; ++col){
            if (map[row][col] == 0)
                return false;
        }
    }
    return true;
}

// 产生新的数字
void app_2048::newnum(){
    if (isFull())
        return;// 注意这边要加一个这种判断是不是数字满了的步骤，不然下面的while会进入死循环

    int x = rand()%H;    //产生数字
    int y = rand()%L;
    while(map[x][y] != 0){
        x = rand()%H;    //产生数字
        y = rand()%L;
    }
    int option = rand()%10;
    if (option == 0)
        map[x][y] = basicnum*2;
    else
        map[x][y] = basicnum;
    return;
}

// 判断游戏是否结束了
int app_2048::det(){
//    if (map[0][0] == 2)
//        return 1;
// 测试结束功能用的

    if (!isFull())
        return 0;

    for (int row = 0; row != H; ++row){
        for (int col = 0; col != L; ++col){
            if (row < H - 1){
                if (map[row][col] == map[row + 1][col])
                    return 0;
            }
            if (col < L - 1){
                if (map[row][col] == map[row][col + 1])
                    return 0;
            }
        }
    }
    // 释放内存空间
    for(int i = 0; i != H; ++i){
        delete []map[i];
    }
    delete []map;

    return 1;

}

// 初始化，出现一开始的两个数字
void app_2048::init(){
    map = new int*[H];  // 注意这边不能写成 int **map, 不然就是又定义了一个局部变量把class中的map取代了！
    for (int i = 0; i != H; ++i){
        map[i] = new int[L];
    }

    for (int i = 0; i != H; ++i){
        for (int j = 0; j != L; ++j){
            map[i][j] = 0;
        }
    }

    srand(time(0)); //随机种子,一个就OK了，不然每次计算的时间很长。。。而且只要在init()中设定一个就OK了，不然会有问题。
    int x1 = rand()%H;    //产生数字
    int y1 = rand()%L;
    int x2 = rand()%H;    //产生数字
    int y2 = rand()%L;
    while (x1 == x2 && y1 == y2){
        x2 = rand()%H;    //产生数字
        y2 = rand()%L;
    }

//    cout << "you want to play with 2 or 3?" << endl;
//    cin >> basic;

    map[x1][y1] = basicnum;
    map[x2][y2] = basicnum;
}

// 找出已经有的最大的数字
int app_2048::biggest(){
    int res = basicnum;
    for (int i = 0; i != H; ++i){
        for (int j = 0; j != L; ++j){
            if (map[i][j] > res)
                res = map[i][j];
        }
    }
    return res;
}

int app_2048::show_map(const int i, const int j){
    return map[i][j];
}



