#ifndef APP_H
#define APP_H

class app_2048
{

private:
    const int H = 4;
    const int L = 4;
    const int basicnum = 2;
    int **map;

public:
    app_2048() = default; //注意构造函数的名字要和class一样！！
    inline void swap(int &a, int &b) const;
    inline int issmaller(int &a, int &b) const;
    bool calculate_up();
    bool calculate_down();
    bool calculate_left();
    bool calculate_right();
    void newnum();
    int det();
    void init();
    int biggest();
    int show_map(const int i, const int b);

private:
    bool isFull();

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
