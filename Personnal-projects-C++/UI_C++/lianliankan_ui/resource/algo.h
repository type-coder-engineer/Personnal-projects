#ifndef ALGO_H
#define ALGO_H
#include <iostream>
#include <stdlib.h>
#include <algorithm>
#include <vector>
#include <cmath>
#include <time.h>
#include <filestruct.h>

class fun
{
//public:
//struct onePointPosition{
//    int x;
//    int y;
//};

//struct positions{
//    int x1;
//    int y1;
//    int x2;
//    int y2;
//};

struct distances{
    int disup1;
    int disdown1;
    int disleft1;
    int disright1;
    int disup2;
    int disdown2;
    int disleft2;
    int disright2;
};

public:
    const int H;
    const int L;
    std::vector<int> slove;
    fun(int row, int column);
    ~fun() = default;
    void init();
    positions search(int x);
    distances calculate(positions fourpoints);
    int check(positions fourpoints);
    int selfcheck();
    virtual void reorganize();
    void reranking();
    void erase(positions fourpoints);
    int help();
    int end();
    int calculate_number();
    int **map;

protected:
    inline int issmaller(int &a, int &b) const{
        return ((a <= b)? a : b);
    }

    inline int isbigger(int &a, int &b) const{
        return ((a >= b)? a : b);
    }

    inline void swap(int &a, int &b) const{
        int c;
        c = a;
        a = b;
        b = c;
    }
};


#endif // ALGO_H
