#include "mainwindow.h"
#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    MainWindow w;
    w.show();

    return a.exec();
}
// 皮卡丘的图标直接把ico文件放在工程文件夹中，然后添加一个pipi.rc文件，最后在pro中加上RC_FILE = pipi.rc就OK了,装换ico的时候选最大的128*128
// 就可以，因为图标大小都是一样的，分辨率高看上去好看一些，体积也没有大多少
