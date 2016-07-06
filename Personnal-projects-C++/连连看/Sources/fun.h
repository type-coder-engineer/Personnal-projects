#ifndef FUN_H
#define FUN_H
#include <iostream>
#include <vector>

class fun
{

struct positions{
    int x1;
    int y1;
    int x2;
    int y2;
};

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

protected:
//    const int H;
//    const int L;
    int **map;

public:
    const int H;
    const int L;

    std::vector<int> slove;

    int unique(int number);

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
    void timer();
    void init();
    positions search(int x);
    distances calculate(positions fourpoints);
    int check(fun::positions fourpoints);
    int selfcheck();
    virtual void reorganize();
    void reranking();
    void erase(positions fourpoints);
    int help();
    void show();
    int end();
    fun(int dimension) : H(dimension),L(dimension){}
    ~fun() = default;

};

#endif // FUN_H
