#include "mainwindow.h"
#include <QMessageBox>
#include <QMenuBar>
#include <QAction>
#include <QCoreApplication>
#include <QDialog>
#include <QRadioButton>
#include <QGridLayout>
#include <QPushButton>
#include <QLabel>

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent)
{
    this->setStyleSheet("background-color:#ffffff");
//    this->resize(800,800);
    this->setWindowTitle("pokeLink presented by ZHANG Chenyu");

    createActions();
    createMenus();

    QCoreApplication::setOrganizationName("Divsion");
    QCoreApplication::setApplicationName("Try_to_link");

    on_newGame();
   // layout()->setSizeConstraint(QLayout::SetFixedSize);
   // setFixedSize(this->width(),this->height());
}

MainWindow::~MainWindow()
{
}

void MainWindow::on_gameOver(){
    QMessageBox::information(this, tr("Result"), tr("Game over!"));
}

void MainWindow::createMenus(){
    game_menu = menuBar()->addMenu(tr("Game"));
    game_menu->addAction(new_game_action);
 //   game_menu->addSeparator();
//    game_menu->addAction(theme_action);
    game_menu->addSeparator();
    game_menu->addAction(exit_action);
  //  game_menu->setStyleSheet("background-color:#ffffff");

    help_menu = menuBar()->addMenu(tr("Help"));
    help_menu->addAction(about_game_action);
    help_menu->addAction(about_qt_action);
  //  help_menu->setStyleSheet("background-color:#ffffff");
}

void MainWindow::createActions(){
    new_game_action = new QAction(tr("New Game"),this);
    new_game_action->setShortcut(QKeySequence::New); // 可以生成一个Ctrl+N的快捷键
    connect(new_game_action,SIGNAL(triggered()),this,SLOT(on_newGame()));

//    theme_action = new QAction(tr("Theme"),this);
//    connect(theme_action,SIGNAL(triggered()),this,SLOT(on_theme()));

    exit_action = new QAction(tr("Exit"),this);
    exit_action->setShortcut(QKeySequence::Quit);
    connect(exit_action,SIGNAL(triggered()),this,SLOT(close()));

    about_game_action = new QAction(tr("About Game"),this);
    connect(about_game_action,SIGNAL(triggered()),this,SLOT(on_about_game()));

    about_qt_action = new QAction(tr("About Qt"),this);
    connect(about_qt_action,SIGNAL(triggered()),qApp,SLOT(aboutQt())); // 关于qt的官方介绍,需要有#include <QCoreApplication>并且有实例
}

// 游戏介绍
void MainWindow::on_about_game(){
    QString introduction(
        "<h2>" + tr("About pokeLink") + "</h2>"
        + "<p>" + tr("Nothing else to say, have fun!")+"</p>"
        + "<p>" + tr("Please see ") + "<a href=https://github.com/type-coder-engineer>https://github.com/type-coder-engineer</a>"+tr(" to find more interesting personnal projects by me")+"</p>"
        + "<br>" + tr("Author: ")+ "ZHANG Chenyu" + "</br>"
    );
    QMessageBox messageBox(QMessageBox::Information,tr("About pokeLink"), introduction, QMessageBox::Ok);
    messageBox.setWindowIcon(QIcon(""));

    messageBox.exec();
}

void MainWindow::on_newGame(){
    myarea = new BlockArea(4,10); // 一开始测试的时候发现8，8的时候卡住不动了。。。后来发现是因为一开始要初始化出至少8*8/4 = 16个解
    // 有点困难，所以现在就把一开始的解变少了。
    this->setCentralWidget(myarea);
    this->resize(12*120,6*130);
    this->setFixedSize(this->width(),this->height());
    connect(myarea, SIGNAL(gameOver()), this, SLOT(on_gameOver()));
}

//void MainWindow::on_theme(){
//    QDialog myDialog;
//    myDialog.setWindowTitle(tr("Theme"));

//    QLabel introLabel(tr("Choose your theme:"));
//    QPushButton closeButton(tr("Confirm"));
//    connect(&closeButton, SIGNAL(clicked(bool)), &myDialog, SLOT(accept()));

//    myRadiobtn1.setText("V");
//    myRadiobtn2.setText("Pokemon");
//    myRadiobtn3.setText("Manga");
////    myRadiobtn4.setText("Game");
//    myRadiobtn1.setChecked(true);

//    QGridLayout* mainlayout=new QGridLayout;
//    mainlayout->addWidget(&introLabel, 0, 0);
//    mainlayout->addWidget(&myRadiobtn1, 1, 0);
//    mainlayout->addWidget(&myRadiobtn2, 2, 0);
//    mainlayout->addWidget(&myRadiobtn3, 3, 0);
////    mainlayout->addWidget(&myRadiobtn4, 4, 0);
//    mainlayout->addWidget(&closeButton, 4, 0);
//    myDialog.setLayout(mainlayout);

//    myDialog.exec();//
//}













