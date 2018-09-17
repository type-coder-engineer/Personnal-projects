#ifndef ALGO_H
#define ALGO_H
#include <iostream>
#include <cmath>

class fun
{

public:
    const int H;
    const int L;
    fun(int row, int column);
    ~fun() = default;
    void init();
    bool end();
    int **map;
};

#endif // ALGO_H
