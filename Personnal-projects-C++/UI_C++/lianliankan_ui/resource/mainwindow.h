#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include "block_area.h"
#include "algo.h"
#include <QMenu>
#include <QAction>
#include <QRadioButton>

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = 0);
    ~MainWindow();

private:
    BlockArea *myarea;
    bool flag_oneChosen;
    void createMenus();
    void createActions();
    QAction *new_game_action;
  //  QAction *theme_action;
    QAction *exit_action;
    QAction *about_game_action;
    QAction *about_qt_action;

    QMenu *game_menu;
    QMenu *help_menu;

//    QRadioButton myRadiobtn1;
//    QRadioButton myRadiobtn2;
//    QRadioButton myRadiobtn3;
//    QRadioButton myRadiobtn4;

private slots:
    void on_gameOver();
    void on_about_game();
    void on_newGame();
  //  void on_theme();
};

#endif // MAINWINDOW_H
