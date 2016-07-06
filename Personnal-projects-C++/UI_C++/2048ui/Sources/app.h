#ifndef APP_H
#define APP_H

class app_2048
{

private:
    const int H = 4;
    const int L = 4;
    const int basicnum = 2;

public:
    int **map;
    app_2048() = default; //注意构造函数的名字要和class一样！！
    inline void swap(int &a, int &b) const;
    inline int issmaller(int &a, int &b) const;
    void calculate_up();
    void calculate_down();
    void calculate_left();
    void calculate_right();
    void newnum();
    int det();
    void init();
    int biggest();
};

inline void app_2048::swap(int &a, int &b) const{
    int c;
    c = a;
    a = b;
    b = c;
}

inline int app_2048::issmaller(int &a, int &b) const{
    return ((a <= b)? a : b);
}

#endif //
