#include "mainwindow.h"
#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    MainWindow w;
    w.show();

    return a.exec();
}

// 想要左上角统一的图标只要加上一个.rc文件，然后做一个ico，在pro文件中加上DISTFILES += 2048.rc还有RC_FILE = 2048.rc 即可，后面一个命令是
// 在需要静态编译的时候要加上的
