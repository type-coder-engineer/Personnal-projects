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
#include <QListWidget>
#include <QSettings>

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent)
{
    this->setWindowTitle("神奇宝贝翻翻乐");
    this->resize(1200, 800);
    this->setFixedSize(1200, 800);
    createActions();
    createMenus();
    QCoreApplication::setOrganizationName("Divsion");
    QCoreApplication::setApplicationName("Turn over");
    for (int i = 0; i != 151; ++i) {
        nameMap[i] = names[i];
    }
    readSetting();
    on_welcome();
}

MainWindow::~MainWindow()
{
}

void MainWindow::on_trainingWin(){
    QMessageBox::information(this, tr("恭喜"), tr("你完成了这个训练!"));
}

void MainWindow::on_catchWin(){
    QMessageBox::information(this, tr("恭喜"), tr("你抓住了所有神奇宝贝!"));
    for (int i:found){
        if (std::find(caught.begin(), caught.end(), i) == caught.end()) {
            caught.push_back(i);
        }
    }
    if (caught.size() > 50 && !first50) {
        QMessageBox::information(this, tr("祝贺你"), tr("你已经抓住了50只以上的神奇宝贝，成为初级训练师!"));
        first50 = true;
    }
    if (caught.size() > 100 && !first100) {
        QMessageBox::information(this, tr("祝贺你"), tr("你已经抓住了100只以上的神奇宝贝，成为中级训练师!"));
        first100 = true;
    }
    if ((find_it(144, caught) || find_it(145, caught) || find_it(146, caught) || find_it(150, caught) || find_it(151, caught)) && !superRare && first100) {
        QMessageBox::information(this, tr("祝贺你"), tr("你已经抓住了包括超级罕见神奇宝贝的多数神奇宝贝，成为高级训练师！"));
        superRare = true;
    }
    if (caught.size() == 151 && !catchAll) {
        QMessageBox::information(this, tr("祝贺你"), tr("你已经抓住了所有神奇宝贝，成为传奇训练师！"));
        catchAll = true;
    }
}

void MainWindow::on_catchLose(){
    QMessageBox::information(this, tr("对不起"), tr("你没有在规定时间内抓住所有神奇宝贝..."));
//    on_selectMode();
    found.clear();
}

void MainWindow::createMenus(){
    game_menu = menuBar()->addMenu(tr("游戏"));
    game_menu->addAction(new_training_action);
    game_menu->addSeparator();
    game_menu->addAction(new_catch_action);
    game_menu->addSeparator();
    game_menu->addAction(dictionary_action);
    game_menu->addSeparator();
    game_menu->addAction(exit_action);

    level_menu = menuBar()->addMenu(tr("难度"));
    level_menu->addAction(easy_action);
    level_menu->addAction(middle_action);
    level_menu->addAction(hard_action);

    help_menu = menuBar()->addMenu(tr("帮助"));
    help_menu->addAction(about_game_action);
    game_menu->addSeparator();
    help_menu->addAction(about_qt_action);
}

void MainWindow::createActions() {
    new_training_action = new QAction(tr("新游戏(训练模式)"), this);
    new_training_action->setShortcut(QKeySequence::New); // 可以生成一个Ctrl+N的快捷键
    connect(new_training_action, SIGNAL(triggered()), this, SLOT(on_newGameTraining()));

    new_catch_action = new QAction(tr("新游戏(捕捉模式)"), this);
    connect(new_catch_action, SIGNAL(triggered()), this, SLOT(on_newGameCatch()));

    dictionary_action = new QAction(tr("宠物图鉴"), this);
    connect(dictionary_action, SIGNAL(triggered()), this, SLOT(on_dictionary()));

    exit_action = new QAction(tr("退出"), this);
    exit_action->setShortcut(QKeySequence::Quit);
    connect(exit_action, SIGNAL(triggered()), this, SLOT(close()));

    easy_action = new QAction(tr("简单(常见的神奇宝贝)"), this);
    easy_action->setCheckable(true);
    middle_action = new QAction(tr("中等(出现高级神奇宝贝)"), this);
    middle_action->setCheckable(true);
    hard_action = new QAction(tr("困难(可能捕获稀有神奇宝贝)"), this);
    hard_action->setCheckable(true);
    levelActionGroup = new QActionGroup(this);
    levelActionGroup->addAction(easy_action);
    levelActionGroup->addAction(middle_action);
    levelActionGroup->addAction(hard_action);
    connect(levelActionGroup, SIGNAL(triggered(QAction*)), this, SLOT(on_level(QAction*)));

    about_game_action = new QAction(tr("关于游戏"), this);
    connect(about_game_action, SIGNAL(triggered()), this, SLOT(on_about_game()));

    about_qt_action = new QAction(tr("关于 Qt"), this);
    connect(about_qt_action, SIGNAL(triggered()), qApp, SLOT(aboutQt())); // 关于qt的官方介绍,需要有#include <QCoreApplication>并且有实例
}

// 游戏介绍
void MainWindow::on_about_game() {
    QString introduction(
        "<h2>" + tr("翻转pokemon游戏") + "</h2>"
        + "<p>" + tr("一个练习C++和Qt的小项目，顺便怀念了一下小时候痴迷的神奇宝贝~游戏的同时能锻炼短期记忆能力，希望你能喜欢^^")+"</p>"
        + "<p>" + tr("请在 ") + "<a href=https://github.com/type-coder-engineer>https://github.com/type-coder-engineer</a>"+tr(" 了解更多我做的有趣的编程项目")+"</p>"
        + "<br>" + tr("作者: ")+ "代码龟" + "</br>"
    );
    QMessageBox messageBox(QMessageBox::Information,tr("关于游戏"), introduction, QMessageBox::Ok);
    messageBox.setWindowIcon(QIcon(""));

    messageBox.exec();
}

void MainWindow::on_newGameTraining() {
    BlockArea *myArea = new BlockArea(gameLevel);
    this->setCentralWidget(myArea);
    this->setStyleSheet("#mainWindow{border-image:url(:/image/gbg1.png);}");

    this->setFixedSize(this->width(),this->height());
    connect(myArea, SIGNAL(gameOver()), this, SLOT(on_trainingWin()));
}

void MainWindow::on_newGameCatch() {
    BlockAreaCatch *myArea = new BlockAreaCatch(gameLevel);
    found = myArea->getResult();
    this->setCentralWidget(myArea);
    this->setStyleSheet("#mainWindow{border-image:url(:/image/gbg2.png);}");

    this->setFixedSize(this->width(),this->height());
    connect(myArea, SIGNAL(gameWin()), this, SLOT(on_catchWin()));
    connect(myArea, SIGNAL(gameLose()), this, SLOT(on_catchLose()));
}

void MainWindow::on_welcome() {
    QWidget *window = new QWidget;
    this->setCentralWidget(window);
    this->setObjectName("mainWindow");
    this->setStyleSheet("#mainWindow{border-image:url(:/image/bg1.png);}");

    QLabel *welcomeText = new QLabel(tr("神奇宝贝翻翻乐"), window);
    QFont welcomeFont;
    welcomeFont.setPointSize(50);
    welcomeFont.setBold(true);
    welcomeText->setFont(welcomeFont);

    QPushButton *startButton = new QPushButton(tr("开始游戏"), window);
    QPushButton *dictionaryButton = new QPushButton(tr("宠物图鉴"), window);
    QFont buttonFont;
    buttonFont.setPointSize(20);
    buttonFont.setBold(true);
    startButton->setFont(buttonFont);
    dictionaryButton->setFont(buttonFont);

    welcomeText->setGeometry(QRect(QPoint(300, 150),QSize(700, 100)));
    startButton->setGeometry(QRect(QPoint(490, 400),QSize(220, 60)));
    dictionaryButton->setGeometry(QRect(QPoint(490, 550),QSize(220, 60)));
    connect(startButton, SIGNAL(clicked(bool)), this, SLOT(on_selectMode()));
    connect(dictionaryButton, SIGNAL(clicked(bool)), this, SLOT(on_dictionary()));
}

void MainWindow::on_dictionary() {
    QWidget *window = new QWidget;
    this->setCentralWidget(window);
    this->setStyleSheet("#mainWindow{border-image:url(:/image/bg1.png);}");

    QLabel *label = new QLabel("宠物小精灵图鉴", window);
    QFont labelFont;
    labelFont.setPointSize(30);
    labelFont.setBold(true);
    label->setFont(labelFont);

    QPushButton *returnButton = new QPushButton(tr("返回主菜单"), window);
    QFont buttonFont;
    buttonFont.setPointSize(20);
    buttonFont.setBold(true);
    returnButton->setFont(buttonFont);

    QListWidget *list = new QListWidget(window);
    for (int i = 1; i != 152; ++i) {
        if (find_it(i, caught)) {
            list->addItem(new QListWidgetItem(QPixmap(":/image/" + QString("%1").arg(i) + ".png"), nameMap[i - 1]));
        }
        else
            list->addItem(new QListWidgetItem(QPixmap(":/image/gray_" + QString("%1").arg(i) + ".png"), tr("???")));
    }
    list->setViewMode(QListView::IconMode);    //加上这句后可以使用不同的视图，我更喜欢这个
    list->setIconSize(QSize(200,200));
    list->setResizeMode(QListWidget::Adjust); // 调整list中图片的大小

    list->setGeometry(QRect(QPoint(250, 120),QSize(700, 530)));
    label->setGeometry(QRect(QPoint(420, 20),QSize(400, 100)));
    returnButton->setGeometry(QRect(QPoint(490, 680), QSize(220, 60)));
    connect(returnButton, SIGNAL(clicked(bool)), this, SLOT(on_welcome()));
}

void MainWindow::on_selectMode() {
    QWidget *window = new QWidget;
    this->setCentralWidget(window);
    this->setStyleSheet("#mainWindow{border-image:url(:/image/bg1.png);}");

    QLabel *label = new QLabel("请选择游戏模式", window);
    QFont labelFont;
    labelFont.setPointSize(40);
    labelFont.setBold(true);
    label->setFont(labelFont);

    QPushButton *button1 = new QPushButton(tr("练习模式"), window);
    QPushButton *button2 = new QPushButton(tr("捕捉模式"), window);
    QPushButton *button3 = new QPushButton(tr("返回菜单"), window);
    QFont buttonFont;
    buttonFont.setPointSize(20);
    buttonFont.setBold(true);
    button1->setFont(buttonFont);
    button2->setFont(buttonFont);
    button3->setFont(buttonFont);

    label->setGeometry(QRect(QPoint(350, 100),QSize(600, 100)));
    button1->setGeometry(QRect(QPoint(490, 300),QSize(220, 60)));
    button2->setGeometry(QRect(QPoint(490, 450),QSize(220, 60)));
    button3->setGeometry(QRect(QPoint(490, 600),QSize(220, 60)));
    connect(button1, SIGNAL(clicked(bool)), this, SLOT(on_newGameTraining()));
    connect(button2, SIGNAL(clicked(bool)), this, SLOT(on_newGameCatch()));
    connect(button3, SIGNAL(clicked(bool)), this, SLOT(on_welcome()));
}

void MainWindow::on_level(QAction *levelAction) {
    if (levelAction == easy_action) {
        gameLevel = 1;
    }
    else if (levelAction == middle_action) {
        gameLevel = 2;
    }
    else {
        gameLevel = 3;
    }
}

inline bool MainWindow::find_it(int i, std::vector<int> caught) {
    std::vector<int>::iterator it = std::find(caught.begin(), caught.end(), i);
    if (it == caught.end())
        return false;
    else
        return true;
}

void MainWindow::writeSetting() {
    QSettings mySettings;

    mySettings.beginGroup("MainWindow");
    mySettings.setValue("pos", pos());
    mySettings.endGroup();

    mySettings.beginWriteArray("found"); // 因为是vector所以需要用array来储存
    for (unsigned int i = 0; i != caught.size(); ++i) {
        mySettings.setArrayIndex(i);
        mySettings.setValue("one", caught.at(i));
    }
    mySettings.endArray();

    mySettings.setValue("first50", first50);
    mySettings.setValue("first100", first100);
    mySettings.setValue("superRare", superRare);
    mySettings.setValue("catchAll", catchAll);
}

void MainWindow::readSetting() {
    QSettings mySettings;

    mySettings.beginGroup("MainWindow");
    move(mySettings.value("pos").toPoint());
    mySettings.endGroup();

    unsigned int length = mySettings.beginReadArray("found");
    for (unsigned int i = 0; i != length; ++i) {
        mySettings.setArrayIndex(i);
        caught.push_back(mySettings.value("one").toInt());
    }
    mySettings.endArray();

    first50 = mySettings.value("first50").toBool();
    first100 = mySettings.value("first100").toBool();
    superRare = mySettings.value("superRare").toBool();
    catchAll = mySettings.value("catchAll").toBool();
}

// 重载关闭事件来加入保存设置
void MainWindow::closeEvent(QCloseEvent*) {
    writeSetting();
}


