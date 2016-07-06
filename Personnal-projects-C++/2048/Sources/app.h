#ifndef APP_H
#define APP_H
#include <iostream>

class app
{
private:
    const int H;
    const int L;
    const int basicnum;
    int **map;

public:
    int direction;

    app(int basechoix, int dimension): H(dimension), L(dimension), basicnum(basechoix){} //注意构造函数的名字要和class一样！！
    ~app() = default;
//    ~app(){std::cout << "I am deleting this example" << std::endl;}
    inline void swap(int &a, int &b) const;
    inline int issmaller(int &a, int &b) const;
    int getorder();
    void calculate(int direction);
    void show();
    void newnum(int times);
    int det();
    void init();

};

#endif //
