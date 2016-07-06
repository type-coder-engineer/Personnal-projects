#ifndef FUN2_H
#define FUN2_H
#include "fun.h"

class fun2 : public fun
{
public:
    void reorganize();
//    inline void swap(int &a, int &b) const;
    fun2(int dimension) : fun(dimension){}
    ~fun2() = default;
};

#endif // FUN2_H
