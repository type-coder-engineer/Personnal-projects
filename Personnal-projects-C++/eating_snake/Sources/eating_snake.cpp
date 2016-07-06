#include <iostream>
#include <stdlib.h>
#include <conio.h>
#include <string>
#include <cstring>
#include <time.h>
#include <windows.h>
#include <cstdlib>

using namespace std;

const int H = 6;   //地图的高
const int L = 6;//地图的长
const int diff = 5;
string GameMap[H][L];   //游戏地图
int  key;  //按键保存
int  sum = 1, over = 0;  //蛇的长度, 游戏结束(自吃或碰墙)
int  dx[4] = {0, 0, -1, 1};  //左、右、上、下的方向
int  dy[4] = {-1, 1, 0, 0};
int step = -1;
static int game = 1;
int win;
int niveau;

struct Snake   //蛇的每个节点的数据类型
{
    int x, y;  //左边位置
    int now;   //保存当前节点的方向, 0,1,2,3分别为左右上下
}Snake[H*L];

const string Shead = "@";  //蛇头
const string Sbody = "#";  //蛇身
const string Sfood = "%";  //食物
const string Mnode = ".";  //'.'在地图上标示为空
void Initial();  //地图的初始化
void Create_Food(); //在地图上随机产生食物
void Show();   //刷新显示地图
int Button();  //取出按键,并判断方向
void Move();   //蛇的移动
void Check_Border();  //检查蛇头是否越界
void Check_Head(int x, int y);   //检查蛇头移动后的位置情况


int Button()  //取出按键,并判断方向
{
     if(kbhit() != 0) //检查当前是否有键盘输入，若有则返回一个非0值，否则返回0
     {
          while(kbhit() != 0){  //可能存在多个按键,要全部取完,以最后一个为主
              key = getch(); //将按键从控制台中取出并保存到key中
          }

          switch(key)
          {
                  //左
               case 75:
               Snake[0].now = 0;
               break;
                  //右
               case 77:
               Snake[0].now = 1;
               break;
                   //上
               case 72:
               Snake[0].now = 2;
               break;
                   //下
               case 80:
               Snake[0].now = 3;
               break;
                   //空格
               case 32:
               return 2;

               default:
               return 0;
          }

          return 1;
     }
     return 0;
}


void Check_Border()  //检查蛇头是否越界
{
 if(Snake[0].x < 0 || Snake[0].x >= H
 || Snake[0].y < 0 || Snake[0].y >= L){
     over = 1;
    }
}

void Create_Food(){ //在地图上随机产生食物
 int fx, fy;
 while(1)
 {
    fx = rand()%H;
        fy = rand()%L;

  if(GameMap[fx][fy] == Mnode)  //不能出现在蛇所占有的位置
    {
        GameMap[fx][fy] = Sfood;
        step += 1;
        break;
    }
  }
}

void Check_Head(int x, int y)  //检查蛇头移动后的位置情况
{

     if(GameMap[ Snake[0].x ][ Snake[0].y ] == Mnode)  //为空
         GameMap[ Snake[0].x ][ Snake[0].y ] = Shead;

     else{
        if(GameMap[ Snake[0].x ][ Snake[0].y ] == Sfood)  //为食物
        {
           GameMap[ Snake[0].x ][ Snake[0].y ] = Shead;
           Snake[sum].x = x;   //新增加的蛇身为蛇头后面的那个
           Snake[sum].y = y;
           Snake[sum].now = Snake[0].now;
           GameMap[ Snake[sum].x ][ Snake[sum].y ] = Sbody;
           sum++;
           Create_Food();  //食物吃完了马上再产生一个食物
        }
        else
        over = 1;
     }
}

void Move()   //蛇的移动
{
     int i, x, y;
     int t = sum;  //保存当前蛇的长度
     //记录当前蛇头的位置,并设置为空,蛇头先移动
     x = Snake[0].x;
     y = Snake[0].y;
     GameMap[x][y] = Mnode;

     Snake[0].x = Snake[0].x + dx[ Snake[0].now ];
     Snake[0].y = Snake[0].y + dy[ Snake[0].now ];
     Check_Border();   //蛇头是否越界
     if (over){
         return;  // 注意这边的两个return是必须的，不然如果上下撞墙了就会发生下标越界，所以一旦出问题了就要return回去。
     }
     Check_Head(x, y);  //蛇头移动后的位置情况,参数为: 蛇头的开始位置
     if (over){
         return;
     }
     if(sum == t){  //未吃到食物即蛇身移动
         for(i = 1; i != sum; ++i)  //要从蛇尾节点向前移动,前一个节点作为参照
         {
              if(i == 1)   //尾节点设置为空再移动
                   GameMap[ Snake[i].x ][ Snake[i].y ] = Mnode;

              if(i == sum - 1)  //为蛇头后面的蛇身节点,特殊处理
              {
                   Snake[i].x = x;
                   Snake[i].y = y;
                   Snake[i].now = Snake[0].now;
              }
              else   //其他蛇身即走到前一个蛇身位置
              {
                   Snake[i].x = Snake[i+1].x;
                   Snake[i].y = Snake[i+1].y;
                   Snake[i].now = Snake[i+1].now;
              }

            GameMap[ Snake[i].x ][ Snake[i].y ] = Sbody; //移动后要置为'#'蛇身
          }
     }
}

void Initial() { //地图的初始化
    int i, j;
    int hx, hy;
    int button;
    win = 0;
    over = 0;
    step = -1;
    sum = 1;
    niveau = 0;
    system("cls");

    cout << "Please choose the difficulty firstly!" << endl;
    cout << "1----------------------easy" << endl;
    cout << "2----------------------medium" << endl;
    cout << "3----------------------difficult" << endl;
    cout << "4----------------------crazy" << endl;
    cout << "Press 1,2,3 or 4 to choose easy, medium,difficult or crazy:" << endl;
    while(1){
        if(!(cin >> niveau)){
            cin.clear();
            cin.sync();
            cout << "Sorry what's your choice please?" << endl;
            continue;
        }
        if(niveau == 1 || niveau == 2 || niveau == 3 || niveau == 4){
            break;
        }
        else{
            cout << "Sorry what's your choice please?" << endl;
        }
    }
    system("cls");
//    system("title eating snake");  //控制台的标题
//    memset(GameMap, '.', sizeof(GameMap));  //初始化地图全部为空'.'
    for(i = 0; i != H; ++i){
        for(j = 0; j != L; ++j){
            GameMap[i][j] = Mnode;
        }
    }
    system("cls");

    srand(time(0));   //随机种子
    hx = rand()%H;    //产生蛇头
    hy = rand()%L;
    GameMap[hx][hy] = Shead;
    Snake[0].x = hx;
    Snake[0].y = hy;
    Snake[0].now = -1;
    Create_Food();   //随机产生食物

    for(i = 0; i != H; ++i){   //地图显示
        for(j = 0; j != L; ++j){
            cout << GameMap[i][j] << "   ";
        }
        cout << endl;
        cout << endl;
    }

    if (game == 1){
        cout << "A little game Snake" << endl;
        cout << "press any direction to start the game" << endl;
        cout << "press space bar to stop the game and press again to continue" << endl;
    }
    else{
        cout << "Welcome to try again" << endl;
        cout << "press any direction to start the game" << endl;
        cout << "press space bar to stop the game and press again to continue" << endl;
    }

    getch();   //先接受一个按键,使蛇开始往该方向走
    button = Button();  //取出按键,并判断方向

    while(button == 0){
        getch();
        button = Button();
    }
}


void Show(){  //刷新显示地图
    int i, j, speed;

    while(1)
    {
         if (niveau != 4){
             Sleep(900 - 250*niveau); //延迟半秒(1000为1s),即每半秒刷新一次地图
         }
         else {
             srand(time(0));   //随机种子
             speed = rand()%diff;    //产生速度
             Sleep(500 - 100*speed);
         }

         if(Button() == 2){    // 按空格键进入暂停模式，再按一次空格键继续开始
             cout << "Time out!" << endl;
             while(Button() != 2)
             {}
         }
         Move();

         if(over)  //自吃或碰墙即游戏结束
         {
             break;
         }
         system("cls");   //清空地图再显示刷新好的地图
         for(i = 0; i != H; ++i)
         {
              for(j = 0; j != L; ++j)
                    cout << GameMap[i][j] << "   ";
              cout << endl;
              cout << endl;
         }
         if (step == (H*L - 2)){
             win = 1;
             break;
         }
         cout << "You are playing the Snake designed by Chenyu ZHANG " << endl;
         cout << "You have eaten " << step << " food(s)" << endl;
    }
}

int main()
{
    string mystring;
    int times = 0;

    while(1){
        Initial();
        Show();
        if (win == 1){
            system("cls");
            for(int i = 0; i != H; ++i)
            {
                 for(int j = 0; j != L; ++j){
                     GameMap[i][j] = Mnode;
                 }
            }
            GameMap[0][1] = Sbody;
            GameMap[0][4] = Sbody;
            GameMap[1][0] = Sbody;
            GameMap[1][2] = Sbody;
            GameMap[1][3] = Shead;
            GameMap[1][5] = Sbody;
            GameMap[2][0] = Sbody;
            GameMap[2][5] = Sbody;
            GameMap[3][1] = Sbody;
            GameMap[3][4] = Sbody;
            GameMap[4][2] = Sbody;
            GameMap[4][3] = Sbody;
            for(int i = 0; i != H; ++i)
            {
                 for(int j = 0; j != L; ++j){
                     cout << GameMap[i][j] << "   ";
                 }
                 cout << endl;
                 cout << endl;
            }
            cout << "Congratulations you win!" << endl;
            cout << "Press 'retry' to retry or 'quit' to quit the game" << endl;
            cin >> mystring;
        }
        else{
            cout << "Game over. Sorry you lost...>_<" << endl;
            cout << "Press 'retry' to retry or 'quit' to quit the game" << endl;
            cin >> mystring;
        }
        while (mystring != "retry" && mystring != "quit"){
            if (times == 3){
                cout << "you are either insane or boring..." << endl;
                Sleep(1000);
                return 0;
            }
            else {
                cout << "Sorry, you want to retry or quit?" << endl;
                cin >> mystring;
                times += 1;
            }
        }
        if (mystring == "quit")
            break;
        else
            game += 1;
    }
    return 1;
}
