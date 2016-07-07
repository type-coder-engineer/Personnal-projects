#include "mainwindow.h"
#include "app.h"
#include "ui_MainWindow.h"

//static int number_record = 2; // 我以为把纪录设置为静态变量就可以直接保存修改了，但是还是不行。。。
//程序关掉重开后纪录就被抹掉了，其实这个很显然，关闭后父组件被删去，静态变量肯定也一并删去了。如果想保存数据的话一定要用QSetting
//static int time_record = 9999;
//static QString number_record_name = "";
//static QString time_record_name = "";
const int no_number_record = 2;
const int no_time_record = 9999;
const QString no_record_name = "";

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    setWindowIcon(QIcon(":/paojie1.png"));
    resize(860,450);
    setWindowTitle("2048 presented by ZHANG Chenyu");

    mycount.setInterval(1000); // 设置每1s发射一次信号
    connect(&mycount, SIGNAL(timeout()), this, SLOT(on_Timeout()));
    connect(this, SIGNAL(isover()), this, SLOT(on_Isover()));
    connect(this, SIGNAL(close_window()), this, SLOT(close()));
    connect(this, SIGNAL(setrecord()), this, SLOT(on_Setrecord()));

    create_actions();
    create_menus();

    original = ui->lcdNumber00->palette(); // 一开始先保存一下默认的lcd调色板

    // 这两段是QSettings默认构造函数，如果想在之后别的地方用就要先声明。。。花了2个小时debug，醉了。。。
    QCoreApplication::setOrganizationName("Divsion");
    QCoreApplication::setApplicationName("2048");

    read_settings();
    on_Newgame();
}

MainWindow::~MainWindow()
{
    delete ui;
}

// 如果是0就没有显示
void MainWindow::choosetohide(QLCDNumber *lcd, int x){
    lcd->setAutoFillBackground(false); // 因为颜色是跟着数字动的，所以一开始先取消填色和调色板
    lcd->setPalette(original);
    // 这里用的是默认的调色板来取消加上去的颜色，没有这个那么边框会有颜色，而且数字是有背景颜色的时候的样子
    if (x != 0){
        lcd->display(x);
        if (x >= 32 && x < 128){
            lcd->setAutoFillBackground(true);
            lcd->setPalette(Qt::darkGreen);
        }
        if (x >= 128 && x < 512){
            lcd->setAutoFillBackground(true);
            lcd->setPalette(Qt::darkCyan);
        }
        if (x >= 512 && x < 2048){
            lcd->setAutoFillBackground(true);
            lcd->setPalette(Qt::darkBlue);
        }
        if (x >= 2048){
            lcd->setAutoFillBackground(true);
            lcd->setPalette(Qt::darkMagenta);
        }
    }
    else
        lcd->display("");    
}

// 把数字和提示时间显示在屏幕上
void MainWindow::update_view(){
    choosetohide(ui->lcdNumber00, mygame.map[0][0]);
    choosetohide(ui->lcdNumber01, mygame.map[0][1]);
    choosetohide(ui->lcdNumber02, mygame.map[0][2]);
    choosetohide(ui->lcdNumber03, mygame.map[0][3]);

    choosetohide(ui->lcdNumber10, mygame.map[1][0]);
    choosetohide(ui->lcdNumber11, mygame.map[1][1]);
    choosetohide(ui->lcdNumber12, mygame.map[1][2]);
    choosetohide(ui->lcdNumber13, mygame.map[1][3]);

    choosetohide(ui->lcdNumber20, mygame.map[2][0]);
    choosetohide(ui->lcdNumber21, mygame.map[2][1]);
    choosetohide(ui->lcdNumber22, mygame.map[2][2]);
    choosetohide(ui->lcdNumber23, mygame.map[2][3]);

    choosetohide(ui->lcdNumber30, mygame.map[3][0]);
    choosetohide(ui->lcdNumber31, mygame.map[3][1]);
    choosetohide(ui->lcdNumber32, mygame.map[3][2]);
    choosetohide(ui->lcdNumber33, mygame.map[3][3]);

    if (mygame.det() == 1){
        emit isover();
        return;
    }
    else
        return;
}

// 键盘时间的switch
void MainWindow::keyPressEvent(QKeyEvent *qke){
    if (qke->key() == Qt::Key_Space){ // 空格键可以暂停
        if (break_flag == 1){
            permit = 0;
            mycount.stop();
            break_flag = 0;
        }
        else {
            permit = 1;
            if (game_begin == 1)
                mycount.start();
            break_flag = 1;
        }
    }
    else if (permit == 1){ // 设置一个permit，这样输完record后就不能用键盘控制了，要重新开始游戏才能把permit重新设为1
        if (game_begin == 0){ // 一开始按动移动键开始计时
            game_begin = 1;
            mycount.start();
        }
        switch(qke->key()){
            case Qt::Key_Up:
                mygame.calculate_up();
                mygame.newnum();
                update_view();
                showreminder();
            break;

            case Qt::Key_Down:
                mygame.calculate_down();
                mygame.newnum();
                update_view();
                showreminder();
            break;

            case Qt::Key_Left:
                mygame.calculate_left();
                mygame.newnum();
                update_view();
                showreminder();
            break;

            case Qt::Key_Right:
                mygame.calculate_right();
                mygame.newnum();
                update_view();
                showreminder();
            break;

            default:
                return ;
        }
    }
    return ;
}

// 显示计时器
void MainWindow::on_Timeout(){
    myowntimer += 1;
    ui->timer->display(QString("%1").arg(myowntimer)); // 本来用的QTime，但是想要实现暂停所以后来换成不停的 +=1 了
    //ui->timer->display(QString("%1").arg(mytime.elapsed()/1000));
}

// 结束时的message以及之后的对话框
void MainWindow::on_Isover(){
    mycount.stop();
    my_number_record = mygame.biggest();

    // 如果两项纪录都没有被打破的情况
    if (my_number_record <= number_record && my_time_record >= time_record){
        QDialog overdialog;
        QPushButton *new_game_pbt = new QPushButton(tr("New game"));
        QPushButton *close_game_pbt = new QPushButton(tr("Quit game"));
        connect(new_game_pbt, SIGNAL(clicked(bool)), &overdialog, SLOT(accept()));
        connect(close_game_pbt, SIGNAL(clicked(bool)), &overdialog, SLOT(reject()));

        QLabel *overlabel = new QLabel(tr("The game is over, do you want to have a new game?"));
        overlabel->adjustSize();

        QGridLayout *uplayout = new QGridLayout;
        QHBoxLayout *downlayout = new QHBoxLayout;
        QVBoxLayout *mainlayout = new QVBoxLayout;
        uplayout->addWidget(overlabel, 0, 0);
        downlayout->addWidget(new_game_pbt);
        downlayout->addWidget(close_game_pbt);
        mainlayout->addLayout(uplayout);
        mainlayout->addLayout(downlayout);

        overdialog.setLayout(mainlayout);

        if (overdialog.exec() == QDialog::Accepted)
            on_Newgame();
        else
            emit close_window();
    }
    // 至少有一项被打破
    else
    {
        if (my_number_record <= number_record || my_time_record >= time_record){
            QDialog overdialog;
            QLabel *overlabel = new QLabel(tr("The game is over, congratulations you have broken one record!"));
            overlabel->adjustSize();
            QPushButton *new_game_pbt = new QPushButton(tr("Start a new game"));
            QPushButton *set_record_pbt = new QPushButton(tr("Set the record"));
            connect(new_game_pbt, SIGNAL(clicked(bool)),&overdialog, SLOT(accept()));
            connect(set_record_pbt, SIGNAL(clicked(bool)), &overdialog, SLOT(reject()));

            QGridLayout *uplayout = new QGridLayout;
            QHBoxLayout *downlayout = new QHBoxLayout;
            QVBoxLayout *mainlayout = new QVBoxLayout;
            uplayout->addWidget(overlabel, 0, 0);
            downlayout->addWidget(set_record_pbt);
            downlayout->addWidget(new_game_pbt);
            mainlayout->addLayout(uplayout);
            mainlayout->addLayout(downlayout);
            overdialog.setLayout(mainlayout);

            if (overdialog.exec() == QDialog::Accepted)
                on_Newgame();
//            else if (overdialog.exec() == QDialog::Rejected)
// 注意这里不需要再加上一个exec()， 因为如果再写一次的话，那么如果选了setrecord就相当于到else那个分支又执行了一次exec，所以之前要点两次serrecord
// 才行，直接else，如果不是accpeted就是rejected，两种情况下都退出了这个dialog的界面
            else
                emit setrecord();
        }
        else {
                QDialog overdialog;
                QLabel *overlabel = new QLabel(tr("The game is over, you have broken two records! Fantastic!!"));
                overlabel->adjustSize();
                QPushButton *new_game_pbt = new QPushButton(tr("Start a new game"));
                QPushButton *set_record_pbt = new QPushButton(tr("Set the records"));
                connect(new_game_pbt, SIGNAL(clicked(bool)), &overdialog, SLOT(accept()));
                connect(set_record_pbt, SIGNAL(clicked(bool)), &overdialog, SLOT(reject()));
// triggered 和 clicked的区别
                QGridLayout *uplayout = new QGridLayout;
                QHBoxLayout *downlayout = new QHBoxLayout;
                QVBoxLayout *mainlayout = new QVBoxLayout;
                uplayout->addWidget(overlabel, 0, 0);
                downlayout->addWidget(set_record_pbt);
                downlayout->addWidget(new_game_pbt);
                mainlayout->addLayout(uplayout);
                mainlayout->addLayout(downlayout);
                overdialog.setLayout(mainlayout);

                if (overdialog.exec() == QDialog::Accepted)
                    on_Newgame();
                else
                    emit setrecord();
        }
    }
}

// 显示左下角的提示语
void MainWindow::showreminder(){
    QStringList data; // 因为settext只能是QStrng的形参，所以我用QStringList来输入多格式的文本，不知道有没有别的方法,似乎还可以用html的格式写来实现，以后再研究
    QString str = "";
    if (game_begin == 1){
        if (mygame.biggest() != 2048)
            data << "You have reached " << tr("%1").arg(mygame.biggest());
        else{
            data << "Congratulation! You have reached 2048 in " << tr("%1").arg(myowntimer) << " seconds";
            my_time_record = myowntimer;
        }
        foreach(QString s, data){
            str += s;
        }
    }
    else
        str.push_back("Please tap any direction key to get started");
    ui->myreminder->setText(str);
    QFont ft;
    ft.setPointSize(12); // 设置字体大小，数字越大就越大
    ui->myreminder->setFont(ft);
    ui->myreminder->adjustSize(); // 可以自动调整label的大小来匹配内容，但是要放在setText的后面
//    //设置颜色
//    QPalette pa;
//    pa.setColor(QPalette::WindowText,Qt::red);
//    ui->myreminder->setPalette(pa);
}

// 工具栏中按钮的actions
void MainWindow::create_actions(){
    new_game_action = new QAction(tr("New Game"),this);
    new_game_action->setShortcut(QKeySequence::New); // 可以生成一个Ctrl+N的快捷键
    connect(new_game_action,SIGNAL(triggered()),this,SLOT(on_Newgame()));

    rank_action = new QAction(tr("Rank"),this);
    connect(rank_action,SIGNAL(triggered()),this,SLOT(on_Rank()));

    exit_action = new QAction(tr("Exit"),this);
    exit_action->setShortcut(QKeySequence::Quit);
    connect(exit_action,SIGNAL(triggered()),this,SLOT(close()));

    about_game_action = new QAction(tr("About Game"),this);
    connect(about_game_action,SIGNAL(triggered()),this,SLOT(on_about_game()));

    about_qt_action = new QAction(tr("About Qt"),this);
    connect(about_qt_action,SIGNAL(triggered()),qApp,SLOT(aboutQt())); // 关于qt的官方介绍
}

// 新游戏的初始化
void MainWindow::on_Newgame()
{
    mygame.init();
    ui->timer->display("0");
    myowntimer = 0;
    mycount.stop();
    my_time_record = 9999;
    my_number_record = 2;
    permit = 1;
    break_flag = 1;
    game_begin = 0;
    update_view();
    showreminder();
}

// 历史排行榜
void MainWindow::on_Rank(){
    QDialog mydialog;
    mydialog.setWindowTitle(tr("Rank"));

    QGridLayout* mainlayout=new QGridLayout;
    mainlayout->addWidget(new QLabel(tr("Standard")),0,0);
    mainlayout->addWidget(new QLabel(tr("Record")),0,1);
    mainlayout->addWidget(new QLabel(tr("Name")),0,2);
    mainlayout->addWidget(new QLabel(tr("2048 Time min")),1,0);
    mainlayout->addWidget(new QLabel(tr("%1").arg(time_record)),1,1);
    mainlayout->addWidget(new QLabel(tr("%1").arg(time_record_name)),1,2);
    mainlayout->addWidget(new QLabel(tr("Standard")),2,0);
    mainlayout->addWidget(new QLabel(tr("Record")),2,1);
    mainlayout->addWidget(new QLabel(tr("Name")),2,2);
    mainlayout->addWidget(new QLabel(tr("The number max reached")),3,0);
    mainlayout->addWidget(new QLabel(tr("%1").arg(number_record)),3,1);
    mainlayout->addWidget(new QLabel(tr("%1").arg(number_record_name)),3,2);

    QPushButton *close_button = new QPushButton(tr("Close"));
    QPushButton *reset_button = new QPushButton(tr("Reset"));
    connect(close_button, SIGNAL(clicked(bool)), &mydialog, SLOT(reject()));
    connect(reset_button, SIGNAL(clicked(bool)), &mydialog, SLOT(accept()));
    mainlayout->addWidget(close_button, 4, 0, Qt::AlignRight);
    mainlayout->addWidget(reset_button, 4, 2, Qt::AlignLeft);

    mainlayout->setColumnStretch(0,2);
    mainlayout->setColumnStretch(1,2);
    mainlayout->setColumnStretch(2,2);

    mainlayout->setRowStretch(0,2);
    mainlayout->setRowStretch(1,2);
    mainlayout->setRowStretch(2,2);
    mainlayout->setRowStretch(3,2);
    mainlayout->setRowStretch(4,3);

    mydialog.setLayout(mainlayout); // 注意setlayout最后一定要写，平时因为是this所以可以省略，但是这里要明确的写mydialog，不然就是空白的
    mydialog.resize(500,300);

    if (mydialog.exec() == QDialog::Accepted){
        time_record = no_time_record;
        number_record = no_number_record;
        time_record_name = number_record_name = no_record_name;
    }
}

// game的下拉菜单
void MainWindow::create_menus(){
    game_menu = menuBar()->addMenu(tr("Game"));
    game_menu->addAction(new_game_action);
    game_menu->addSeparator();
    game_menu->addAction(rank_action);
    game_menu->addSeparator();
    game_menu->addAction(exit_action);

    help_menu = menuBar()->addMenu(tr("Help"));
    help_menu->addAction(about_game_action);
    help_menu->addAction(about_qt_action);
}

// 游戏结束的时候如果破纪录的界面
void MainWindow::on_Setrecord(){
    QString name;

    if (my_number_record <= number_record){
        name = QInputDialog::getText(this, tr("Setting record"), tr("You have created a time record, please enter your name here"));
        if (!name.isEmpty()){
            time_record = my_time_record;
            time_record_name = name;
        }
    }
    else if (my_time_record >= time_record){
        name = QInputDialog::getText(this, tr("Setting record"), tr("You have created a number record, please enter your name here"));
        if (!name.isEmpty()){
            number_record = my_number_record;
            number_record_name = name;
        }
    }
    else{
        name = QInputDialog::getText(this, tr("Setting record"), tr("You have created two records, please enter your name here"));
        if (!name.isEmpty()){
            number_record = my_number_record;
            number_record_name = name;
            time_record = my_time_record;
            time_record_name = name;
            }
        }
    permit = 0;
}

// 游戏介绍
void MainWindow::on_about_game(){
    QString introduction(
        "<h2>" + tr("About 2048") + "</h2>"
        + "<p>" + tr("This game is played by using the direction keys to move the numbers, the numbers on the moving direction will be accumulated automatiquely if they are the same. At first you need to tap any dirction to get started the time_counter, in the game you can tap space key to take a break and tap again to get back in the game. Besides the first move, the new number appeared will not be certainly 2, there is a possibility that it will be 4 or 8. The game is over when there are no room for new number and no possibility to accumulate. There are two records, one is the time min to reach 2048 and the other one is the biggest number you have reached. Enjoy your game!")+"</p>"
        + "<p>" + tr("Please see ") + "<a href=https://github.com/type-coder-engineer>https://github.com/type-coder-engineer</a>"+tr(" to find more interesting personnal projects by me")+"</p>"
        + "<br>" + tr("Author: ")+ "ZHANG Chenyu" + "</br>"
    );
    QMessageBox messageBox(QMessageBox::Information,tr("About 2048"), introduction, QMessageBox::Ok);
    messageBox.setWindowIcon(QIcon(":paojie1.png"));

    messageBox.exec();
}

// 读取保存的settings
void MainWindow::read_settings(){
    QSettings mySettings;

    mySettings.beginGroup("MainWindow");
//    resize(mySettings.value("size").toSize());
    move(mySettings.value("pos").toPoint());
    mySettings.endGroup();

    mySettings.beginGroup("Rank");
    time_record = mySettings.value("time_record").toInt() == 0 ? no_time_record : mySettings.value("time_record").toInt();
    number_record = mySettings.value("number_record").toInt() == 0 ? no_number_record : mySettings.value("number_record").toInt();
    time_record_name = mySettings.value("time_record_name").toString() == "" ? no_record_name : mySettings.value("time_record_name").toString();
    number_record_name = mySettings.value("number_record_name").toString() == "" ? no_record_name : mySettings.value("number_record_name").toString();
    mySettings.endGroup();
}

// 关闭的时候记录当前的settings
void MainWindow::write_settings(){
    QSettings mySettings;

    mySettings.beginGroup("MainWindow");
//    mySettings.setValue("size", size()); // 有这句不能生成ui界面，不知道是不是因为我用的是qt designer，因为我把constructor中的
//    resize删掉还是不行。。。。不过可以保存位置我就很满意了
    mySettings.setValue("pos", pos());
    mySettings.endGroup();

    mySettings.beginGroup("Rank");
    mySettings.setValue("time_record", time_record);
    mySettings.setValue("number_record", number_record);
    mySettings.setValue("time_record_name", time_record_name);
    mySettings.setValue("number_record_name", number_record_name);
    mySettings.endGroup();
}

// 重载关闭事件来调用write_settings
void MainWindow::closeEvent(QCloseEvent* )
{
    write_settings();
}
