#include "fun2.h"

void fun2::reorganize(){
//    for (int j = 2; j != L + 1; j += 2){
//      // 妈的又是一个傻逼的错误，注意 != 适用于++j，像这样j+=2 就要直接用 < 了，不然就直接跳过判断条件了！！！
//        for (int i = 1; i != H + 1; ++i){
//            if (map[i][j] != 0){
//                for (int k = i; k != 1; --k){
//                    if (map[k - 1][j] == 0){
//                        swap(map[k][j],map[k - 1][j]);
//                    }
//                    else
//                        break;
//                }
//            }
//        }
//    }
    for (int j = 1; j != L + 1; ++j){
        if (j % 2 != 0){
            for (int i = H; i != 0; --i){
                if (map[i][j] != 0){
                    for (int k = i; k != H; ++k){
                        if (map[k + 1][j] == 0){
                            swap(map[k][j],map[k + 1][j]);
                        }
                        else
                            break;
                    }
                }
            }
        }
        else{
            for (int i = 1; i != H + 1; ++i){
                if (map[i][j] != 0){
                    for (int k = i; k != 1; --k){
                        if (map[k - 1][j] == 0){
                            swap(map[k][j],map[k - 1][j]);
                        }
                        else
                            break;
                    }
                }
            }
        }
    }
}

//inline void fun2::swap(int &a, int &b) const{
//    int c;
//    c = a;
//    a = b;
//    b = c;
//}
