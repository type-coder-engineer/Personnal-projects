#include "fun1.h"

void fun1::reorganize(){
    for (int j = 1; j != L + 1; ++j){
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
}

