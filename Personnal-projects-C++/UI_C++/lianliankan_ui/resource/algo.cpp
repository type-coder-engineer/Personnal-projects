#include "algo.h"
#define hehe H * L / 8

fun::fun(int row, int column): H(row),L(column)
{
    this->init();
}
// 初始化这个游戏的地图
void fun::init()
{
    map = new int*[H + 2];//最外面一圈是0
    for (int i = 0; i != H + 2; ++i){
        map[i] = new int[L + 2];
    }

    for (int i = 0; i != H + 2; ++i){
        for (int j = 0; j != L + 2; ++j){
            map[i][j] = 0;
        }
    }
    srand(time(0));
    int nb = H * L / 2;

    while(calculate_number() < hehe){ // 保证一开始的可能的解不至于太少
        for (int i = 0; i != H + 2; ++i){
            for (int j = 0; j != L + 2; ++j){
                map[i][j] = 0;
            }
        }
        for (int i = 1; i != nb + 1; ++i){
            int x1 = rand()%L;
            int y1 = rand()%H;
            while (map[y1 + 1][x1 + 1] != 0){
                x1 = rand()%L;
                y1 = rand()%H;
            }
            map[y1 + 1][x1 + 1] = i;
            int x2 = rand()%L;
            int y2 = rand()%H;
            while (map[y2 + 1][x2 + 1] != 0){
                x2 = rand()%L;
                y2 = rand()%H;
            }
            map[y2 + 1][x2 + 1] = i;
        }
    }
}

// 用来计算可能的解的数量
int fun::calculate_number(){
    int possible_solution = 0;
    for (int i = 1; i != H * L + 1; ++i){
        std::vector<int>::iterator it = std::find(fun::slove.begin(), fun::slove.end(), i);
        if (it == slove.end()){
            positions self_check;
            self_check = search(i);
            if(check(self_check) == 1){
                possible_solution += 1;
            }
        }
    }
    return possible_solution;
}

// 输入一个数字的时候可以找到这个数字的位置
positions fun::search(int x){
    int flag = 0;
    positions ex;
    ex.x1 = ex.x2 = 0;
    ex.y1 = ex.y2 = 0; // 加上这句，这样如果输入了已经消掉的数就可以知道了
    if (x == 0){
        return ex;
    }
    else {
        for (int i = 1; i != H + 1; ++i){
            for (int j = 1; j != L + 1; ++j){
                if (map[i][j] == x && flag == 0){
                    ex.y1 = i;
                    ex.x1 = j;
                    flag = 1;
                }
                else if(map[i][j] == x && flag == 1){
                    ex.y2 = i;
                    ex.x2 = j;
                }
            }
        }
    }
    return ex;
}

// 通过找到数字的位置来计算两个位置之间的x和y方向上的距离
fun::distances fun::calculate(positions fourpoints){
    distances ex;
    ex.disup1 = 0;
    ex.disdown1 = 0;
    ex.disleft1 = 0;
    ex.disright1 = 0;
    ex.disup2 = 0;
    ex.disdown2 = 0;
    ex.disleft2 = 0;
    ex.disright2 = 0;
// 注意这边循环的首尾一定要注意，如果有问题应该首先检查首尾有没有出错，这边我要得到距离，所以应该是由起始点的旁边的点开始
    for (int j = fourpoints.x1 - 1; j != -1; --j){
        if(map[fourpoints.y1][j] == 0){
            ex.disleft1 += 1;
        }
        else
            break;
    }

    for (int j = fourpoints.x2 - 1; j != -1; --j){
        if(map[fourpoints.y2][j] == 0){
            ex.disleft2 += 1;
        }
        else
            break;
    }

    for (int j = fourpoints.x1 + 1; j != L + 2; ++j){
        if(map[fourpoints.y1][j] == 0){
            ex.disright1 += 1;
        }
        else
            break;
    }

    for (int j = fourpoints.x2 + 1; j != L + 2; ++j){
        if(map[fourpoints.y2][j] == 0){
            ex.disright2 += 1;
        }
        else
            break;
    }

    for (int i = fourpoints.y1 - 1; i != -1; --i){
        if(map[i][fourpoints.x1] == 0){
            ex.disup1 += 1;
        }
        else
            break;
    }

    for (int i = fourpoints.y2 - 1; i != -1; --i){
        if(map[i][fourpoints.x2] == 0){
            ex.disup2 += 1;
        }
        else
            break;
    }

    for (int i = fourpoints.y1 + 1; i != H + 2; ++i){
        if(map[i][fourpoints.x1] == 0){
            ex.disdown1 += 1;
        }
        else
            break;
    }

    for (int i = fourpoints.y2 + 1; i != H + 2; ++i){
        if(map[i][fourpoints.x2] == 0){
            ex.disdown2 += 1;
        }
        else
            break;
    }

    return ex;
}

// 尝试所有可能的连线方式来确认是否可以成功连上
int fun::check(positions fourpoints){ // 这种debug就直接在测试中看哪种情况有问题就直接修改，这样效率高一些。
    if (fourpoints.x1 == fourpoints.x2 && fourpoints.y1 == fourpoints.y2)
        return 0;

    //第一种情况，横排坐标相等
    if(fourpoints.x1 == fourpoints.x2){
        if (abs(fourpoints.y1 - fourpoints.y2) == 1){
            return 1;
        } //相邻就直接ok
        else{
            int flagfind1 = 0;
            int flagfind2 = 0;
            int flagfind3 = 0;
            //看直线能不能连
            for (int i = fourpoints.y1 + 1; i != fourpoints.y2; ++i){
                if(map[i][fourpoints.x1] != 0){
                    flagfind1 = 1;
                    break;
                }
            }
            if (flagfind1 == 0){
                return 1;
            }
            //看走左面可不可以
            else{
                for(int j = fourpoints.x1 - 1; j != -1; --j){
                    if(map[fourpoints.y1][j] !=0 || map[fourpoints.y2][j] != 0){
                        flagfind2 = 1;
                        break;
                    }
                    for (int i = fourpoints.y1; i != fourpoints.y2 + 1; ++i){
                        if(map[i][j] != 0){
                            flagfind2 = 1;
                            break;
                        }
                    }
                    if (flagfind2 == 0){
                        return 1;
                    }
                    flagfind2 = 0;
                }
                // 看走右面可不可以
                for(int j = fourpoints.x1 + 1; j != L + 2; ++j){
                    if(map[fourpoints.y1][j] !=0 || map[fourpoints.y2][j] != 0){
                        flagfind3 = 1;
                        break;
                    }
                    for (int i = fourpoints.y1; i != fourpoints.y2 + 1; ++i){
                        if(map[i][j] != 0){
                            flagfind3 = 1;
                            break;
                        }
                    }
                    if (flagfind3 == 0){
                        return 1;
                    }
                    flagfind3 = 0;
                }
            }
        }
        return 0;
    }
    //第二种情况，纵坐标相等
    else if(fourpoints.y1 == fourpoints.y2){
        if(fourpoints.x2 - fourpoints.x1 == 1){
            return 1;
        }
        else{
            int flagfind1 = 0;
            int flagfind2 = 0;
            int flagfind3 = 0;
            //看直线能不能连
            for (int j = fourpoints.x1 + 1; j != fourpoints.x2; ++j){
                if(map[fourpoints.y1][j] != 0){
                    flagfind1 = 1;
                    break;
                }
            }
            if (flagfind1 == 0){
                return 1;
            }
            //看走上面一排可不可以
            else{
                for (int i = fourpoints.y1 - 1; i != -1; --i){
                    if(map[i][fourpoints.x1] !=0 || map[i][fourpoints.x2] != 0){
                        flagfind2 = 1;
                        break;
                    }
                    for (int j = fourpoints.x1; j != fourpoints.x2 + 1; ++j){
                        if(map[i][j] != 0){
                            flagfind2 = 1;
                            break;
                        }
                    }
                    if (flagfind2 == 0){
                        return 1;
                    }
                    flagfind2 = 0;
                }
                // 看走下面一排可不可以
                for (int i = fourpoints.y1 + 1; i != H + 2; ++i ){
                    if(map[i][fourpoints.x1] != 0 || map[i][fourpoints.x2] != 0){
                        flagfind3 = 1;
                        break;
                    }
                    for (int j = fourpoints.x1; j != fourpoints.x2 + 1; ++j){
                        if(map[i][j] != 0){
                            flagfind3 = 1;
                            break;
                        }
                    }
                    if (flagfind3 == 0){
                        return 1;
                    }
                    flagfind3 = 0;
                }
            }
        }
        return 0;
    }
    // 如果横坐标和纵坐标都不相等
    else{
        distances check;
        check = calculate(fourpoints);
        //左上右下
        if(fourpoints.x1 < fourpoints.x2){
            //一个折
            if(check.disdown1 >= abs(fourpoints.y2 - fourpoints.y1) && check.disleft2 >= abs(fourpoints.x1 - fourpoints.x2)){
                return 1;
            }
            //一个折
            else if(check.disright1 >= abs(fourpoints.x2 - fourpoints.x1) && check.disup2 >= abs(fourpoints.y1 - fourpoints.y2)){
                return 1;
            }
            //两个折 left
            else if(check.disleft1 >= 1 && check.disleft2 >= abs(fourpoints.x1 - fourpoints.x2) + 1){
                int flag = 0;
                int tem = check.disleft2 - abs(fourpoints.x1 - fourpoints.x2);
                for(int i = 0; i != issmaller(check.disleft1, tem); ++i){
                    for(int j = fourpoints.y1; j != fourpoints.y2; ++j){
                        if(map[j][fourpoints.x1 - i - 1] != 0){
                            flag = 1;
                            break;
                        }
                    }
                    if(flag == 0){
                        return 1;
                    }
                    flag = 0;
                }
            }
            //两个折 up
            else if(check.disup1 >= 1 && check.disup2 >= abs(fourpoints.y1 - fourpoints.y2) + 1){
                int flag = 0;
                int tem = check.disup2 - abs(fourpoints.y1 - fourpoints.y2);
                for(int i = 0; i != issmaller(check.disup1, tem); ++i){
                    for(int j = fourpoints.x1; j != fourpoints.x2; ++j){
                        if(map[fourpoints.y1 - i - 1][j] != 0){
                            flag = 1;
                            break;
                        }
                    }
                    if(flag == 0){
                        return 1;
                    }
                    flag = 0;
                }
            }
            //两个折 right
            else if(check.disright2 >= 1 && check.disright1 >= abs(fourpoints.x1 - fourpoints.x2) + 1){
                int flag = 0;
                int tem = check.disright1 - abs(fourpoints.x1 - fourpoints.x2);
                for(int i = 0; i != issmaller(check.disright2, tem); ++i){
                    for(int j = fourpoints.y1; j != fourpoints.y2; ++j){
                        if(map[j][fourpoints.x2 + i + 1] != 0){
                            flag = 1;
                            break;
                        }
                    }
                    if(flag == 0){
                        return 1;
                    }
                    flag = 0;
                }
            }
            //两个折 down
            else if(check.disdown2 >= 1 && check.disdown1 >= abs(fourpoints.y1 - fourpoints.y2) + 1){
                int flag = 0;
                int tem = check.disdown1 - abs(fourpoints.y1 - fourpoints.y2);
                for(int i = 0; i != issmaller(check.disdown2, tem); ++i){
                    for(int j = fourpoints.x1; j != fourpoints.x2; ++j){
                        if(map[fourpoints.y2 + i + 1][j] != 0){
                            flag = 1;
                            break;
                        }
                    }
                    if(flag == 0){
                        return 1;
                    }
                    flag = 0;
                }
            }
            //两个折 中间 第一种情况
            else if(check.disright1 + check.disleft2 >= abs(fourpoints.x2 - fourpoints.x1)){
                int flag = 0;
                int tem1 = fourpoints.x2 - check.disleft2;
                int tem2 = fourpoints.x1 + check.disright1 + 1;
                int tem3 = fourpoints.x1 + 1;
                for(int j = isbigger(tem3, tem1); j != issmaller(fourpoints.x2, tem2) ; ++j){
                    for(int i = fourpoints.y1; i != fourpoints.y2; ++i){
                        if(map[i][j] != 0){
                            flag = 1;
                            break;
                        }
                    }
                    if(flag == 0){
                        return 1;
                    }
                    flag = 0;
                }
            }
            //第二种情况
            else if(check.disdown1 + check.disup2 >= abs(fourpoints.y2 - fourpoints.y1)){
                int flag = 0;
                int tem1 = fourpoints.y2 - check.disup2;
                int tem2 = fourpoints.y1 + check.disdown1 + 1;
                int tem3 = fourpoints.y1 + 1;
                for(int j = isbigger(tem3, tem1); j != issmaller(fourpoints.y2, tem2) ; ++j){
                    for(int i = fourpoints.x1; i != fourpoints.x2; ++i){
                        if(map[j][i] != 0){
                            flag = 1;
                            break;
                        }
                    }
                    if(flag == 0){
                        return 1;
                    }
                    flag = 0;
                }
            }

        }

        //左下右上
        if(fourpoints.x1 > fourpoints.x2){
            //一个折
            if(check.disdown1 >= abs(fourpoints.y2 - fourpoints.y1) && check.disright2 >= abs(fourpoints.x1 - fourpoints.x2)){
                return 1;
            }
            //一个折
            else if(check.disleft1 >= abs(fourpoints.x2 - fourpoints.x1) && check.disup2 >= abs(fourpoints.y1 - fourpoints.y2)){
                return 1;
            }
            //两个折 left
            else if(check.disleft2 >= 1 && check.disleft1 >= abs(fourpoints.x1 - fourpoints.x2) + 1){
                int flag = 0;
                int tem = check.disleft1 - abs(fourpoints.x1 - fourpoints.x2);
                for(int i = 0; i != issmaller(check.disleft2, tem); ++i){
                    for(int j = fourpoints.y1; j != fourpoints.y2; ++j){
                        if(map[j][fourpoints.x2 - i - 1] != 0){
                            flag = 1;
                            break;
                        }
                    }
                    if(flag == 0){
                        return 1;
                    }
                    flag = 0;
                }
            }
            //两个折 up
            else if(check.disup1 >= 1 && check.disup2 >= abs(fourpoints.y1 - fourpoints.y2) + 1){
                int flag = 0;
                int tem = check.disup2 - abs(fourpoints.y1 - fourpoints.y2);
                for(int i = 0; i != issmaller(check.disup1, tem); ++i){
                    for(int j = fourpoints.x2; j != fourpoints.x1; ++j){
                        if(map[fourpoints.y1 - i - 1][j] != 0){
                            flag = 1;
                            break;
                        }
                    }
                    if(flag == 0){
                        return 1;
                    }
                    flag = 0;
                }
            }
            //两个折 right
            else if(check.disright1 >= 1 && check.disright2 >= abs(fourpoints.x1 - fourpoints.x2) + 1){
                int flag = 0;
                int tem = check.disright2 - abs(fourpoints.x1 - fourpoints.x2);
                for(int i = 0; i != issmaller(check.disright1, tem); ++i){
                    for(int j = fourpoints.y1; j != fourpoints.y2; ++j){
                        if(map[j][fourpoints.x1 + i + 1] != 0){
                            flag = 1;
                            break;
                        }
                    }
                    if(flag == 0){
                        return 1;
                    }
                    flag = 0;
                }
            }
            //两个折 down
            else if(check.disdown2 >= 1 && check.disdown1 >= abs(fourpoints.y1 - fourpoints.y2) + 1){
                int flag = 0;
                int tem = check.disdown1 - abs(fourpoints.y1 - fourpoints.y2);
                for(int i = 0; i != issmaller(check.disdown2, tem); ++i){
                    for(int j = fourpoints.x2; j != fourpoints.x1; ++j){
                        if(map[fourpoints.y2 + i + 1][j] != 0){
                            flag = 1;
                            break;
                        }
                    }
                    if(flag == 0){
                        return 1;
                    }
                    flag = 0;
                }
            }
            //两个折 中间 情况1
            else if(check.disright2 + check.disleft1 >= abs(fourpoints.x2 - fourpoints.x1)){
                int flag = 0;
                int tem1 = fourpoints.x1 - check.disleft1;
                int tem2 = fourpoints.x2 + check.disright2 + 1;
                int tem3 = fourpoints.x2 + 1;
                for(int j = isbigger(tem3, tem1); j != issmaller(fourpoints.x1, tem2) ; ++j){
                    for(int i = fourpoints.y1; i != fourpoints.y2; ++i){
                        if(map[i][j] != 0){
                            flag = 1;
                            break;
                        }
                    }
                    if(flag == 0){
                        return 1;
                    }
                    flag = 0;
                }
            }
            //情况2
            else if(check.disup2 + check.disdown1 >= abs(fourpoints.y2 - fourpoints.y1)){
                int flag = 0;
                int tem1 = fourpoints.y2 - check.disup2;
                int tem2 = fourpoints.y1 + check.disdown1 + 1;
                int tem3 = fourpoints.y1 + 1;
                for(int j = isbigger(tem3, tem1); j != issmaller(fourpoints.y2, tem2) ; ++j){
                    for(int i = fourpoints.x2; i != fourpoints.x1; ++i){
                        if(map[j][i] != 0){
                            flag = 1;
                            break;
                        }
                    }
                    if(flag == 0){
                        return 1;
                    }
                    flag = 0;
                }
            }

        }
        return 0;
    }
}

// 自检，看是否有可能的解
int fun::selfcheck(){
    for (int i = 1; i != H * L + 1; ++i){
        std::vector<int>::iterator it = std::find(fun::slove.begin(), fun::slove.end(), i);
        if (it == slove.end()){
            positions self_check;
            self_check = search(i);
            if(check(self_check) == 1){
                return 1;
            }
        }
    }
    return 0;
}

// 如果没有可能的数字时候的重新排序
void fun::reranking(){  //一开始怎么排序想了好久，后来发现想复杂了。。。
    for(int i = 0; i != H + 2; ++i){
        for(int j = 0; j != L + 2; ++j){
            if(map[i][j] != 0){
                int y = rand()%H;
                int x = rand()%L;
                while(map[y][x] == 0){
                    y = rand()%H;
                    x = rand()%L;
                }
                swap(map[i][j], map[y][x]);
            }
        }
    }
}

// 纯虚函数，用来继承用的
void fun::reorganize(){
}

// 消除数字
void fun::erase(positions fourpoints){
//    map[fourpoints.y1][fourpoints.x1] = 0;
//    map[fourpoints.y2][fourpoints.x2] = 0;
    map[fourpoints.x1][fourpoints.y1] = 0;
    map[fourpoints.x2][fourpoints.y2] = 0;
}

// 获得提示，可以知道消除哪个数字
int fun::help(){
    for (int i = 1; i != H + 1; ++i){
        for (int j = 1; j != L + 1; ++j){
            if (map[i][j] != 0){
                if (check(search(map[i][j])) == 1){
                    return map[i][j];
                }
            }
        }
    }
    return 0;
}

// 当所有数字都是0的时候游戏就结束了
int fun::end(){
    for(int i = 0; i != H + 2; ++i){
        for (int j = 0; j != L + 2; ++j){
            if (map[i][j] == 0){
                continue;
            }
            else
                return 0;
        }
    }
    for (int i = 0; i != H; ++i){
        delete []map[i];
    }
    delete []map;
    return 1;
}





