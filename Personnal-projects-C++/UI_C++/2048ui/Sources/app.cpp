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
void app_2048::calculate_up(){
    for (int j = 0; j != L; ++j){
        for (int i = 1; i != H; ++i){
            if (map[i][j] != 0){
                while((i - 1 != -1)&& (map[i - 1][j] == 0)){
                    swap(map[i][j], map[i - 1][j]);
                    --i;
                }
                if ((i - 1 != -1) && (map[i - 1][j] == map[i][j])){
                    map[i - 1][j] = map[i - 1][j] * 2;
                    map[i][j] = 0;
                }
            }
        }
    }
}

void app_2048::calculate_down(){
    for (int j = 0; j != L; ++j){
        for (int i = H - 2; i != -1; --i){
            if(map[i][j] != 0){
                while((i + 1 != H) && (map[i + 1][j] == 0)){
                    swap(map[i][j], map[i + 1][j]);
                    ++i;
                }
                if ((i + 1 != H) && (map[i + 1][j] == map[i][j])){
                    map[i + 1][j] = map[i + 1][j] * 2;
                    map[i][j] = 0;
                }
            }
        }
    }
}

void app_2048::calculate_left(){
    for (int i = 0; i != H; ++i){
        for (int j = 1; j != L; ++j){
            if(map[i][j] != 0){
                while((map[i][j - 1] == 0) && (j - 1 != -1)){
                    swap(map[i][j], map[i][j - 1]);
                    --j;
                }
                if ((j - 1 != -1) && (map[i][j - 1] == map[i][j])){
                    map[i][j - 1] = map[i][j - 1] * 2;
                    map[i][j] = 0;
                }
            }
        }
    }
}

void app_2048::calculate_right(){
    for (int i = 0; i != H; ++i){
        for (int j = L - 2; j != -1; --j){
            if(map[i][j] != 0){
                while((j + 1 != L) && (map[i][j + 1] == 0)){ // 注意这边一定要把(j + 1 != L)这种判断条件放在前面，不然在数组中就是下标越界。
                    swap(map[i][j], map[i][j + 1]);
                    ++j;
                }
                if((j + 1 != L) && (map[i][j + 1] == map[i][j])){ // 这边同样的道理，要在if中加上防止下标越界的条件(j + 1 != L)
                    map[i][j + 1] = map[i][j + 1] * 2;
                    map[i][j] = 0;
                }
            }
        }
    }
}
//**************************************************
// 产生新的数字
void app_2048::newnum(){
    int *res = 0;
    int fill = 1;
 //   int count = 0;
    for(int i = 0; i != H; ++i){
        res = std::find(map[i], map[i] + L, 0);
        if (res != map[i] + L){
            fill = 0;
            break;
        }
        else
            continue;
    } // 注意这边要加一个这种判断是不是数字满了的步骤，不然下面的while会进入死循环

    if(fill == 0){
        int x = rand()%H;    //产生数字
        int y = rand()%L;
        while(map[x][y] != 0){
            x = rand()%H;    //产生数字
            y = rand()%L;
        }
// 本来这里是有一个出现的数字不是2而是场上最小的数字的算法的，但是发现这样就过于简单了，所以就去掉了
//        int base = basicnum * 4;  // 注意这边和MATLAB不一样，4次方不能用^

//        // 如果之后场上只有4或4以上的，那么新出现的数就不是2了，最大会直接出现8
//        for (int j = 0; j != L; ++j){
//            for (int i = 0; i != H; ++i){
//                if (map[i][j] != 0){
//                    ++count;
//                    base = issmaller(map[i][j], base);
//                }
//            }
//        }
//        if (count != 1) // 防止一开始的两个数直接加起来就只直接变成4了。
//            map[x][y] = base;
//        else
//            map[x][y] = basicnum;
        map[x][y] = basicnum;
    }
}

// 判断游戏是否结束了
int app_2048::det(){
    int *res = 0; //用来寻找有没有0的指针
    int fill = 1;
    vector<int> range;
    for(int i = 0; i != H; ++i){
        range.push_back(i);
    }

    for(int i = 0; i != H; ++i){
        res = std::find(map[i], map[i] + L, 0);
        if (res != map[i] + L){
            fill = 0;
            return 0;
        }
        else
            continue;
    }
    // 判断的标准是先看看是不是数字全满了，然后再看每个数字的上下左右是不是有相同可以运算的，如果全满加上没有数字可以和周围的运算了即表示游戏结束
    if (fill == 1){
        for(int x = 0; x != H; ++x){
            for(int y = 0; y != L; ++y){
                for (int x1 = x - 1; x1 != x + 2; ++x1){
                    for (int y1 = y - 1; y1 != y + 2; ++y1){ // 4个for，前两个是为了遍历每个元素，后两个是为了每个元素的前后
                        if (x1 != x || y1 != y){
                            if(x + y == x1 + y1 + 1 || x + y == x1 + y1 - 1){ // 这个if是为了比较的值是上下左右，而不考虑角四个上的值
                                vector<int>::iterator it1 = std::find(range.begin(), range.end(), x1);
                                vector<int>::iterator it2 = std::find(range.begin(), range.end(), y1);

                                if (it1 != range.end() && it2 != range.end()){ // 这个if是为了确认比较的范围在矩阵中
                                    if (map[x1][y1] == map[x][y]){
                                        return 0;
                                    }
                                }
                            }
                        }
                    }
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
    else
        return 0;
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



