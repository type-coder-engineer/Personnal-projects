#ifndef FUN1_H
#define FUN1_H
#include "fun.h"

class fun1 : public fun
{
public:

    void reorganize();
//    inline void swap(int &a, int &b) const;
    fun1(int dimension) : fun(dimension){}  // 注意子类的构造函数的继承，名字不一样所以肯定不是一个构造函数
    ~fun1() = default;
 //   inline void swap(int &a, int &b)const ;
};

#endif // FUN1_H
