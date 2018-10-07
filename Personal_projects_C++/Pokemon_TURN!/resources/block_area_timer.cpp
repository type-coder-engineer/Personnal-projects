#include "block_area_timer.h"
#include <QGridLayout>
#include <QLayout>
#include <QPixmap>
#include <QPainter>
#include <time.h>
#include <map>

// 这个文件是捕捉模式，也就是有计时功能的
BlockAreaCatch::BlockAreaCatch(int level, QWidget* parent)
    :QWidget(parent)
{
    myLevel = level;
    if (myLevel == 1) {
        int index = 1;
        while(index < 88) {
            if (index != 3 && index != 6 && index != 9 && index != 25 && index != 26) {
                level1.push_back(index);
            }
            ++index;
        }
        myRow = 3;
        myColumn = 6;
        counter = 500; // 设置的时间间隔是100,也就是0.1s，所以这里500是50秒
    }
    else if (myLevel == 2) {
        int index = 1;
        while(index < 142) {
            if (index != 122 && index != 132 && index != 134 && index != 135 && index != 136 && index != 137) {
                level2.push_back(index);
            }
            ++index;
        }
        myRow = 4;
        myColumn = 7;
        counter = 650;  // 65 秒
    }
    else {
        int index = 88;
        srand(time(0));
        int luck = std::rand()%30;  // 减少稀有神奇宝贝的出现概率
        if (luck == 1) {  // 有梦幻
            while(index < 152) {
                if (index != 134 && index != 135 && index != 136 && index != 137 && index != 142 && index != 144 && index != 145 && index != 146 && index != 150) {
                    level3.push_back(index);
                }
                ++index;
            }
        }
        else if (luck == 2) {  // 有超梦
            while(index < 152) {
                if (index != 134 && index != 135 && index != 136 && index != 137 && index != 142 && index != 144 && index != 145 && index != 146 && index != 151) {
                    level3.push_back(index);
                }
                ++index;
            }
        }
        else if (luck >= 3 && luck <= 5){  // 有三只鸟
            while(index < 152) {
                if (index != 134 && index != 135 && index != 136 && index != 137 && index != 142 && index != 150 && index != 151) {
                    level3.push_back(index);
                }
                ++index;
            }
        }
        else if (luck >= 6 && luck <= 10) {  // 有伊布三种形态，3D龙，化石翼龙
            while(index < 152) {
                if (index != 144 && index != 145 && index != 146 && index != 150 && index != 151) {
                    level3.push_back(index);
                }
                ++index;
            }
        }
        else {
            while(index < 152) {
                if (index != 134 && index != 135 && index != 136 && index != 137 && index != 142 && index != 144 && index != 145 && index != 146 && index != 150 && index != 151) {
                    level3.push_back(index);
                }
                ++index;
            }
        }
        myRow = 5;
        myColumn = 8;
        counter = 800;  // 80 秒
    }

    mygame = new fun(myRow, myColumn);
    choosePicture();
    set_block_area();
    oneReady = 0;
    positionReady.x = 0;
    positionReady.y = 0;
    myLevel = level;
}

// 一开始把图片添加到每个block上，然后排列到mainlayout上面
void BlockAreaCatch::set_block_area() {
    mainLayout = new QVBoxLayout(this);
    hLayout = new QHBoxLayout();
    QLabel *text = new QLabel("剩余时间: ");
    QFont labelFont;
    labelFont.setPointSize(14);
    text->setFont(labelFont);
    bar = new QProgressBar();
    bar->resize(600, 30);
    hLayout->addWidget(text);
    hLayout->addWidget(bar);
    gridLayout = new QGridLayout();
    for(int i = 0; i < myRow; ++i){
        for(int j = 0; j < myColumn; ++j){
            Block *bb = new Block;
            w = bb->width();
            h = bb->height();
            bb->setNumber(i, j);
            originalState(bb);
            bb->setPixmap(QPixmap(":/image/0.png"));
            gridLayout->addWidget(bb, i, j, Qt::AlignCenter);
            connect(bb, SIGNAL(userAction(onePointPosition)), this, SLOT(checkIt(onePointPosition)));
        }
    }
    mainLayout->addLayout(hLayout);
    mainLayout->addLayout(gridLayout);
    bar->setMaximum(counter);
    timer.setInterval(100);
    connect(&timer, SIGNAL(timeout()), this, SLOT(updateProgressbar()));
    timer.start();
}

void BlockAreaCatch::updateProgressbar() {
    if(counter >= 0) {
        --counter;
        bar->setValue(counter);
//        QPalette p = progressBar.palette();
//        p.setColor(QPalette::Highlight, Qt::blue);
//        progressBar->setStyleSheet("background_color: #ff0000");
        bar->show();
    }
    else {
        timer.stop();
        frozon = true;
        emit gameLose();
    }
}

// 每次鼠标事件后会发送这个信号来检查鼠标事件的结果
void BlockAreaCatch::checkIt(onePointPosition nowPosition) {
    if (frozon || mygame->map[nowPosition.x][nowPosition.y] == 0) {
        return;
    }
    if (oneReady == 0) {
        positionReady.x = nowPosition.x;
        positionReady.y = nowPosition.y;
        Block *readyBlock = static_cast<Block*>(gridLayout->itemAtPosition(positionReady.x, positionReady.y)->widget());
        onePointPosition pos = readyBlock->getNumber();
        int number = mygame->map[pos.x][pos.y];
        readyBlock->setPixmap(QPixmap(":/image/" + QString("%1").arg(myPicture[number]) + ".png"));
        oneReady = 1;
        return; //这个是没有block被选中的情况，先选中一个准备好
    }
    else {
        // 现在开始就是已经有一个被选中的情况了
        Block *targetBlock1 = static_cast<Block*>(gridLayout->itemAtPosition(positionReady.x, positionReady.y)->widget());
        Block *targetBlock2 = static_cast<Block*>(gridLayout->itemAtPosition(nowPosition.x, nowPosition.y)->widget());
        // 首先保证选中的两个数字都一样
        if (mygame->map[positionReady.x][positionReady.y] == mygame->map[nowPosition.x][nowPosition.y]) {
            // 然后排除掉同一个block点击两次的情况
            if (positionReady.x == nowPosition.x && positionReady.y == nowPosition.y) {
                originalState(targetBlock1);
                oneReady = 0;
            }
            else {
                clickState(targetBlock1);
                clickState(targetBlock2);
                mygame->map[positionReady.x][positionReady.y] = 0;
                mygame->map[nowPosition.x][nowPosition.y] = 0;
                oneReady = 0;
            }
        }
        else {
            originalState(targetBlock1);
            clickState(targetBlock2);
            positionReady.x = nowPosition.x;
            positionReady.y = nowPosition.y;
            oneReady = 1;
        }
    }
    if (mygame->end()) {
        timer.stop();
        frozon = true;
        emit gameWin();
    }
    return;
}

// 回到原来没有被选中的状态
void BlockAreaCatch::originalState(Block *block) {
    block->setPixmap(QPixmap(":/image/0.png"));
    return;
}

void BlockAreaCatch::clickState(Block *block) {
    onePointPosition pos = block->getNumber();
    int number = mygame->map[pos.x][pos.y];
    block->setPixmap(QPixmap(":/image/" + QString("%1").arg(myPicture[number]) + ".png"));
    return;
}

void BlockAreaCatch::choosePicture() {
    int total;// 这个主题总的图片数目
    std::vector<int> options;
    srand(time(0));

    if (myLevel == 1) {
        total = level1.size();
        options = level1;
    }
    else if (myLevel == 2) {
        total = level2.size();
        options = level2;
    }
    else {
        total = level3.size();
        options = level3;

//        int luck = std::rand()%5;
//        if (luck == 1) {
//            total = level3.size();
//            options = level3;
//        }
//        else {
//            total = level3.size() - 2;
//            options = level3;
//            options.pop_back();
//            options.pop_back();
//        }
    }
    myPicture.insert(std::make_pair(1, options[std::rand()%total]));
    res.push_back(myPicture[1]);

    for (int i = 2; i != myRow * myColumn / 2 + 1; ++i){
        int j;
        while(1){
            j = options[std::rand()%total];
            int flagOut = 1;
            for (std::map<int, int>::iterator mapit = myPicture.begin(); mapit != myPicture.end(); ++mapit){
                if (mapit->second == j){
                    flagOut = 0;
                    break;
                }
            }
            if (flagOut){
                break;
            }
        }
        myPicture.insert(std::make_pair(i,j));
        res.push_back(j);
    }
    return;
}

std::vector<int> BlockAreaCatch::getResult() {
    return res;
}
