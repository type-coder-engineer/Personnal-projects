#ifndef TIMER_H
#define TIMER_H
#include <windows.h>

class timer
{
public:
    timer();
    ~timer();
    void Starter(unsigned int nElapse);
    void Ender();
    static DWORD WINAPI ThreadFunc(LPVOID para);
private:
    unsigned int m_Elapse;
    HANDLE m_hThread;

};

#endif // TIMER_H
