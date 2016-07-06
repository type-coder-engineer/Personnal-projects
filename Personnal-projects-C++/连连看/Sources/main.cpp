#include <iostream>
#include <conio.h>
#include "fun.h"
#include "fun1.h"
#include "fun2.h"
#include "timer.h"
#include <time.h>
#include <sstream>
//#include <thread>

using std::cin;
using std::cout;
using std::endl;

//void timer(){
//    time_t begin, end, period;
//    begin = time(NULL);
//    Sleep(1000);
//    while (1){
//        end = time(NULL);
//        period = end - begin;
//        if (period < 10)
//            cout << "\ryou have passed " << period << " s" ;
//        else if (period < 100)
//            cout << "\ryou have passed " << period << " s" ;
//        else
//            cout << "\ryou have passed " << period << " s" ;
//        Sleep(1000);
//    }
//}

int StringtoInt(const std::string& str){
    std::istringstream iss(str);
    int num;
    iss >> num;
    return num;
}

int main()
{
    int dimension, diff;
    cout << "welcome to this game!" << endl;
    cout << "Enter the number and you can remove it if possible. And tape \"help\" to get help" << endl;
    cout << "What dimenstion you want to play? You can choose in 4, 6, 8 or 10" << endl;
    cin >> dimension;
    while (dimension != 4 && dimension != 6 && dimension != 8 && dimension != 10){
        cout << "Sorry you can only choose in 4, 6, 8 or 10" << endl;
        cin.clear();
        cin.ignore();
        cin >> dimension;
    }

    cout << "Which difficulty you want to play? 1, 2 or 3?" << endl;
    cin >> diff;
    while (diff != 1 && diff != 2 && diff != 3){
        cout << "Sorry you can only choose in 1, 2 or 3" << endl;
        cin.clear();
        cin.ignore();
        cin >> diff;
    }
    fun *game; // 用指针实现多态，注意下面的成员函数要用->表示
    fun game1(dimension);
    fun1 game2(dimension);
    fun2 game3(dimension);
    while (diff != 1 && diff != 2 && diff != 3){
        cout << "Which difficulty you want to play? 1, 2 or 3?" << endl;
        cin >> diff;
    }
    if (diff == 1)
        game = &game1;
    else if(diff == 2)
        game = &game2;
    else if (diff == 3)
        game = &game3;
//    HANDLE h = CreateThread(NULL, 0, (LPTHREAD_START_ROUTINE)timer, NULL, 1, 0);
//    std::thread timerThread = std::thread(timer);

    game->init();
    while(game->selfcheck() == 0){
        game->init();
    }
    game->show();
//    ResumeThread(h);
    std::string enter;
    int number;
    int again, wrong;
    time_t tbegin, tend;
    tbegin = time(NULL);
    wrong = 0;
    while(1){
        again = 0;
        tend = time(NULL);
        if (wrong == 1){
            system("cls");
            game->show();
            wrong = 0;
        }
        cout << "You have got " << game->slove.size() << " numbers and it takes you " << (tend - tbegin) << " secondes" << endl;
        cout << "Which number you want to erase?" << endl;
        cin >> enter;
          //  std::string help;
          //  cin >> help;
        if (enter == "help"){
            system("cls");
            game->show();
            cout << "You can enter " << game->help() << endl;
            again = 1;
        }
        else{
            number = StringtoInt(enter);
        }

        if (again == 1)
            continue;

        if (game->check(game->search(number)) == 1){
            game->erase(game->search(number));
                //if (game->unique(number) == 1 && number < game->H * game->L / 2 && number > 0)
            game->slove.push_back(number);
        }
        else{
            wrong = 1;
            continue;
        }

//        else{
//            game.show();
//            cout << "This number doesn't work...." << endl;
//            continue;
//        }
        game->reorganize();

        system("cls");
        game->show();

        if(game->end() == 1){
            cout << "Congratulations!" << endl;
            cout << "It takes you " << (tend - tbegin) << " secondes in total to finish!" << endl;
            break;
        }

        if(game->selfcheck() == 0){
            cout << "There is no possible number, tap any key to have a reranking." << endl;
            getch();
            game->reranking();
            while(game->selfcheck() == 0){
                game->reranking();
            }
            game->show();
        }
    }
//    CloseHandle(h);
//    timerThread.join();
    cout << "The game is over, tap any key to quit." << endl;
    getch();
    return 0;

}
