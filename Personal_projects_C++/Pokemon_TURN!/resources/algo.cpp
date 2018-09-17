#include "algo.h"
#include "time.h"

fun::fun(int row, int column): H(row),L(column)
{
    this->init();
}
// 初始化这个游戏的地图
void fun::init() {
    map = new int*[H];
    for (int i = 0; i != H; ++i){
        map[i] = new int[L];
    }

    for (int i = 0; i != H; ++i){
        for (int j = 0; j != L; ++j){
            map[i][j] = 0;
        }
    }
    srand(time(0));
    int nb = H * L / 2;

    for (int i = 0; i != H; ++i){
        for (int j = 0; j != L; ++j){
            map[i][j] = 0;
        }
    }
    for (int i = 1; i != nb + 1; ++i){
        int x1 = rand()%L;
        int y1 = rand()%H;
        while (map[y1][x1] != 0){
            x1 = rand()%L;
            y1 = rand()%H;
        }
        map[y1][x1] = i;
        int x2 = rand()%L;
        int y2 = rand()%H;
        while (map[y2][x2] != 0){
            x2 = rand()%L;
            y2 = rand()%H;
        }
        map[y2][x2] = i;
    }
}

// 当所有数字都是0的时候游戏就结束了
bool fun::end() {
    for(int i = 0; i != H; ++i){
        for (int j = 0; j != L; ++j){
            if (map[i][j] == 0){
                continue;
            }
            else
                return false;
        }
    }
    for (int i = 0; i != H; ++i){
        delete []map[i];
    }
    delete []map;
    return true;
}


