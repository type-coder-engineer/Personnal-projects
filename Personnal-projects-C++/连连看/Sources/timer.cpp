#include "timer.h"
#include <iostream>
#include <time.h>
using namespace std;

timer::timer():m_Elapse(0), m_hThread(NULL){

}

timer::~timer(){

}

void timer::Starter(unsigned int nElapse){
    m_Elapse = nElapse;
    m_hThread = CreateThread(NULL, 0, ThreadFunc, (LPVOID)(&m_Elapse), 0, NULL);
}

void timer::Ender(){
    CloseHandle(m_hThread);
}

DWORD WINAPI timer::ThreadFunc(LPVOID para){
    time_t t1, t2;
    double diff = 0;
    int elapse = *((int*)para);
    t1 = time(NULL);
    while(1){
       t2 = time(NULL);
       diff = difftime(t2, t1);
        if ((int)diff == 1){
            cout << "Time out!" << endl;
            t1 = t2;
        }
    }
    return 0;
}





