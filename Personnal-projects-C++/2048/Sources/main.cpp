#include <iostream>
#include <conio.h>
#include <ctime>
#include "app.h"

int main()
{
    int order;
    int i = 0;
//    time_t start, end, period;

    int basechoix, dimension;
    std::cout << "you want to play with 2 or 3 as your base?" << std::endl;
    std::cin >> basechoix;
    while (basechoix != 2 && basechoix != 3){
        std::cout << "you want to play with 2 or 3 as your base?" << std::endl;
        std::cin >> basechoix;
    }

    std::cout << "you want to play with which dimension? you can choose from 3 to 5" << std::endl;
    std::cin >> dimension;
    while (dimension != 3 && dimension != 4 && dimension != 5){
        std::cout << "you want to play with which dimension? you can choose from 3 to 5" << std::endl;
        std::cin >> dimension;
    }
    app ex(basechoix, dimension); // 注意有构造函数时的声明方式！！

    ex.init();
    while(1){
//        start = clock();
        ex.calculate(ex.direction);
        ex.newnum(i);
//        end = clock();
//        period = end - start;
        system("cls");
        ex.show();
        std::cout << "you have moved " << ++i << " times" << std::endl;
//        std::cout << "this time takes " << period << " ms" << std::endl;
        if (ex.det() == 1){
            break;
        }
        order = ex.getorder();
        while (order != 1){
            order = ex.getorder();
        }
    }
    std::cout << "you failed!" << std::endl;
    std::cout << "press return to quit..." << std::endl;
    getch();
    return 0;

}
