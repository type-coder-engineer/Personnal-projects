#include "app.h"
#include <iostream>
#include <time.h>
#include <windows.h>
#include <cstdlib>
#include <algorithm>
#include <stdlib.h>
#include <conio.h>
#include <vector>

using std::cout;
using std::cin;
using std::endl;
using std::vector;

inline void app::swap(int &a, int &b) const{
    int c;
    c = a;
    a = b;
    b = c;
}

inline int app::issmaller(int &a, int &b) const{
    return ((a <= b)? a : b);
}

int app::getorder(){
    int key;

    if(kbhit() != 0) //检查当前是否有键盘输入，若有则返回一个非0值，否则返回0
    {
//         while(kbhit() != 0)  //可能存在多个按键,要全部取完,以最后一个为主
         key = getch(); //将按键从控制台中取出并保存到key中

         switch(key)
         {
                 //左
              case 75:
              direction = 0;
              break;
                 //右
              case 77:
              direction = 1;
              break;
                  //上
              case 72:
              direction = 2;
              break;
                  //下
              case 80:
              direction = 3;
              break;

              default:
              return 0;
         }
         return 1;
    }
    return 0;
}

void app::calculate(int direction){
    // right
    if (direction == 1){
//        for (int i = 0; i != H; ++i){
//            for (int j = L - 2; j != -1; --j){
//                if(map[i][j] != 0){
//                    while((map[i][j + 1] == 0) && (j + 1 != L)){
//                        swap(map[i][j], map[i][j + 1]);
//                        ++j;
//                    }
//                }
//            }

//            for (int j = L - 1; j != -1; --j){
//                if (map[i][j] == map[i][j - 1]){
//                    map[i][j - 1] = 0;
//                    map[i][j] = map[i][j] * 2;
//                    }
//            }

//            for (int j = L - 2; j != -1; --j){
//                if(map[i][j] != 0){
//                    while((map[i][j + 1] == 0) && (j + 1 != L)){
//                        swap(map[i][j], map[i][j + 1]);
//                        ++j;
//                    }
//                }
//            }
//        }
        //这个是最开始的算法，就是一坨屎，想的太复杂了，还分了两步前移。。。不过后来发现测试中的延时问题不是因为算法的复杂，不过因祸得福让我把算法精简了一下

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
    //left
    if (direction == 0){
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
    //down
    if (direction == 3){
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
    //up
    if (direction == 2){
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

}

void app::newnum(int times){
//    srand(time(0));   //随机种子,一个就OK了，不然每次计算的时间很长。。。不用在这儿再使用一次，在init使用一次就够了
    int *res;
    int fill = 1;
    for(int i = 0; i != H; ++i){
        res = std::find(map[i], map[i] + L, 0);
        if (res != map[i] + L){
            fill = 0;
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

        int base = basicnum * 4;  // 注意这边和MATLAB不一样，4次方不能用^
        if(times > 5){
            for (int j = 0; j != L; ++j){
                for (int i = 0; i != H; ++i){
                    if (map[i][j] != 0){
                        base = issmaller(map[i][j], base);
                    }
                }
            }
        }
        else{
            base = basicnum;
        }

        map[x][y] = base;
    }
}

int app::det(){
    int *res;
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
    // 判断的标准是先看看是不是数字全满了，然后再看每个数字的上下左右是不是有相同可以运算的，如果也全满加上没有数字可以和周围的运算了即表示游戏结束
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

void app::show(){
    for (int i = 0; i != H; ++i){
        for (int j = 0; j != L; ++j){
            if(map[i][j] > 100)
                std::cout << map[i][j] << "  ";
            else if (map[i][j] > 10)
                std::cout << map[i][j] << "   ";
            else
                std::cout << map[i][j] << "    ";
        }
        std::cout << std::endl;
        std::cout << std::endl;
        std::cout << std::endl;
    }
}

void app::init(){
    int button;
    system("cls");
    std::cout << "welcome to this game" << std::endl;

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

    show();

    cout << "tap a direction key to start" << endl;

    getch();   //先接受一个按键并且确认是方向键
    button = getorder();  //取出按键,并判断方向

    while(button == 0){
        getch();
        button = getorder();
    }
}




