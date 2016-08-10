#include "block_area.h"
#include <QGridLayout>
#include <QLayout>
#include <QPixmap>
//#include <QPen>
#include <QPainter>
#include <time.h>
#include <map>

const int PIX_SIZE = 20;

BlockArea::BlockArea(int row,int column,QWidget* parent)
    :QWidget(parent)
{
    this->setStyleSheet("background-color: #ffffff");
    mygame = new fun(row, column);
    choosePicture(row, column);
    set_block_area(row,column);
    oneReady = 0;
    positionReady.x = 0;
    positionReady.y = 0;
    connect(this, SIGNAL(reRankPicture()), this, SLOT(on_reRankPicture()));
    connect(this, SIGNAL(gameOver()), this, SLOT(on_gameOver()));
   // myBgm = new QSound(":/sound/pokemon.wav");
    mySuccessSound = new QSound(":/sound/pika.wav");
   // myBgm->setLoops(-1); // 表示无限循环
  //  myBgm->play();

}

// 一开始把图片添加到每个block上，然后排列到mainlayout上面
void BlockArea::set_block_area(int row,int column)
{
    myRow = row + 2;
    myColumn = column + 2;

    mainLayout = new QGridLayout(this);
    for(int i = 0;i < myRow;i++){
        for(int j = 0;j < myColumn;j++){
            Block *bb = new Block;
            w = bb->width();
            h = bb->height();
            bb->setNumber(i, j);
            originalState(bb);
            int number = mygame->map[i][j];
            bb->setPixmap(QPixmap(":/image/1_" + QString("%1").arg(myPicture[number]) + ".png").scaled(w,h,Qt::KeepAspectRatio));
            mainLayout->addWidget(bb, i, j);
            connect(bb, SIGNAL(userAction(onePointPosition)), this, SLOT(checkIt(onePointPosition)));
        }
    }
}

// 每次鼠标事件后会发送这个信号来检查鼠标事件的结果
void BlockArea::checkIt(onePointPosition nowPosition){
    if (mygame->map[nowPosition.x][nowPosition.y] == 0){
        return;
    }
    if (oneReady == 0){
        positionReady.x = nowPosition.x;
        positionReady.y = nowPosition.y;
        Block *readyBlock = static_cast<Block*>(mainLayout->itemAtPosition(positionReady.x, positionReady.y)->widget());
        // 将mainlayout中的widget转换成block格式，可以通过row和column的位置选择widget
        //readyBlock->setStyleSheet("background-color:#ff0000");
//        readyBlock->setStyleSheet("border:5px solid red;");
        //readyBlock->setText("f");
       // update();
        readyBlock->setPixmap(QPixmap(":/image/1_ok.png").scaled(w,h,Qt::KeepAspectRatio));
        oneReady = 1;
        return; //这个是没有block被选中的情况，先选中一个准备好
    }
    else{
        // 现在开始就是已经有一个被选中的情况了
        int gameResult = 0;
        positions fourpoints;
        Block *targetBlock1 = static_cast<Block*>(mainLayout->itemAtPosition(positionReady.x, positionReady.y)->widget());
        Block *targetBlock2 = static_cast<Block*>(mainLayout->itemAtPosition(nowPosition.x, nowPosition.y)->widget());
// 首先保证选中的两个数字都一样
        if (mygame->map[positionReady.x][positionReady.y] == mygame->map[nowPosition.x][nowPosition.y]){
            fourpoints.x1 = positionReady.x;
            fourpoints.y1 = positionReady.y;
            fourpoints.x2 = nowPosition.x;
            fourpoints.y2 = nowPosition.y;
            // 然后排除掉同一个block点击两次的情况
            if (fourpoints.x1 == fourpoints.x2 && fourpoints.y1 == fourpoints.y2){
                originalState(targetBlock1);
                oneReady = 0;
                return;
            }
            else{
                gameResult = mygame->check(mygame->search(mygame->map[nowPosition.x][nowPosition.y]));
                // 这里我们还是需要用search函数而不是直接用他们的坐标，因为search可以确定他们之间的相对位置关系，左上右下还是反着的
                if (gameResult == 1){
                    mySuccessSound->play(); // 可以播放音乐了
                    mygame->erase(fourpoints); // 一开始有一个bug，一直不知道怎么回事，后来发现是因为我一开始写erase
    // 函数的时候x和y是反着的，因为我是用的矩阵的表示方式先是row再是column，而这里本来就是用x表示row，y表示column的，虽然
    // 在check这个函数中还是原来的坐标体系，但是我直接把数字输进去就OK了，原来是怎么计算的我不用管了~~啦啦啦，API rules！！
                    targetBlock1->erase();
                    targetBlock2->erase();
                    oneReady = 0;
                    if (mygame->end() == 1){
                       // myBgm->stop(); // 可以直接停下来，网上说循环不能停是骗小孩的
                        mySuccessSound->stop();
                        emit gameOver();
                    }
                    else{
                        if (mygame->selfcheck() == 0){
                            while (mygame->calculate_number() < 1){
                                mygame->reranking();
                            }
                            emit reRankPicture();
                        }
                    }
                    return;
                }
                // 如果是同一个数字但是不能连起来
                else {
                    oneReady = 0;
                    originalState(targetBlock1);
                    originalState(targetBlock2);
                    return;
                }
            }
        }
        else{
            oneReady = 0;
            originalState(targetBlock1);
            originalState(targetBlock2);
        }
    }
}

void BlockArea::originalState(Block *block){
    int number = mygame->map[block->getNumber().x][block->getNumber().y];
    block->setPixmap(QPixmap(":/image/1_" + QString("%1").arg(myPicture[number]) + ".png").scaled(w,h,Qt::KeepAspectRatio));
    return;
}

// 重新打乱前要先删去原来的widget和layout，不然鼠标事件没法响应
void BlockArea::on_reRankPicture(){
    for(int i = 1;i < myRow - 1;i++)
        for(int j = 1;j < myColumn - 1;j++)
            delete static_cast<Block*>(mainLayout->itemAtPosition(i,j)->widget());
    delete mainLayout;

    mainLayout = new QGridLayout(this);
    for(int i = 0;i < myRow; i++){
        for(int j = 0;j < myColumn; j++){
            Block *bb = new Block;
            bb->setNumber(i, j);
            originalState(bb);
            if (mygame->map[i][j] != 0){
                int number = mygame->map[i][j];
                bb->setPixmap(QPixmap(":/image/1_" + QString("%1").arg(myPicture[number]) + ".png").scaled(w,h,Qt::KeepAspectRatio));
            }
            mainLayout->addWidget(bb, i, j);
            connect(bb, SIGNAL(userAction(onePointPosition)), this, SLOT(checkIt(onePointPosition)));
        }
    }
    return;
}

void BlockArea::on_gameOver(){
    for(int i = 1;i < myRow - 1;i++)
        for(int j = 1;j < myColumn - 1;j++)
            delete static_cast<Block*>(mainLayout->itemAtPosition(i,j)->widget());
    delete mainLayout;
}

void BlockArea::choosePicture(int row, int column){
    int total = 145; // 这个主题总的图片数目
    srand(time(0));
    myPicture.insert(std::make_pair(1, std::rand()%total + 1));

    for (int i = 2; i != row * column / 2 + 1; ++i){
        int j;
        while(1){
            j = std::rand()%total + 1;
            int flagOut = 1;
            for (std::map<int, int>::iterator mapit = myPicture.begin(); mapit != myPicture.end(); ++mapit){
                if (mapit->second == j){
                    flagOut = 0;
                    break;
                }
            }
            if (flagOut == 1){
                break;
            }
        }
        myPicture.insert(std::make_pair(i,j));
    }
    return;
}

//void BlockArea::drawEmbrace(const int &x, const int &y){
//    QPainter myPainter(this);
//    QPen myPen;
//    myPen.setWidth(5);
//    myPen.setColor(Qt::red);
//    myPainter.setPen(myPen);
//    myPainter.translate(y*PIX_SIZE,x*PIX_SIZE);
//    myPainter.drawLine(0,0,PIX_SIZE,0);
//    myPainter.drawLine(0,0,0,PIX_SIZE);
//    myPainter.drawLine(0,PIX_SIZE,0,0);
//    myPainter.drawLine(0,PIX_SIZE,PIX_SIZE,PIX_SIZE);
//    myPainter.drawLine(PIX_SIZE,0,PIX_SIZE,PIX_SIZE);
//    myPainter.drawLine(PIX_SIZE,0,0,0);
//    myPainter.drawLine(PIX_SIZE,PIX_SIZE,PIX_SIZE,0);
//    myPainter.drawLine(PIX_SIZE,PIX_SIZE,0,PIX_SIZE);
//    myPainter.end();
//}


