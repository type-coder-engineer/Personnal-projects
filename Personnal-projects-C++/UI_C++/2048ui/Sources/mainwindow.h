#ifndef MainWindow_H
#define MainWindow_H

#include <QMainWindow>
#include <QTimer>
#include <QWidget>
#include <QLCDNumber>
#include <QCloseEvent>
#include <QKeyEvent>
#include <QMessageBox>
#include <QString>
#include <QStringListModel>
#include <QAction>
#include <QDialog>
#include <QPushButton>
#include <QToolBar>
#include <QMenu>
#include <QMenuBar>
#include <QLayout>
#include <QInputDialog>
#include <QSettings>
#include <QIcon>
#include <QPalette>
#include "app.h"

namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = 0);
    ~MainWindow();

signals:
    void setrecord();
    void isover();
    void close_window();

private slots:
    void on_Timeout();
    void on_Isover();
    void on_Setrecord();
    void on_Newgame();
    void on_Rank();
    void on_about_game();

private:
    Ui::MainWindow *ui;
    QTimer mycount; //  注意尽量避免用指针，因为指针一定要初始化，不然会报错
    app_2048 mygame; // 在mainwindow.h中初始化game即可，同样尽量避免指针！！

    QAction* new_game_action;
    QAction* rank_action;
    QAction* exit_action;
    QAction* about_game_action;
    QAction* about_qt_action;

    int my_time_record;
    int my_number_record;
    int time_record;
    int number_record;
    int break_flag;
    int myowntimer;
    int game_begin;
    int game_end;
    QString time_record_name;
    QString number_record_name;
    QToolBar *mytoolbar;
    QMenu *game_menu;
    QMenu *help_menu;
    QPalette original;

private:
    void update_view();
    void choosetohide(QLCDNumber *lcd, int x);
    void keyPressEvent(QKeyEvent *qke);
    void show_reminder();
    void create_actions();
    void create_menus();
    void read_settings();
    void write_settings();

protected:
    void closeEvent(QCloseEvent*);

};

#endif // MainWindow_H
