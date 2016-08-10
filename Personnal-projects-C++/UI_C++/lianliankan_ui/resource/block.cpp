#include "block.h"
#include <QPainter>

const int PIX_SIZE = 40;

Block::Block(QWidget* parent)
    :QLabel(parent)
{
    this->resize(100,110);
    myRow = 0;
    myColumn = 0;
}

void Block::setNumber(int i, int j){
    myRow = i;
    myColumn = j;
}

onePointPosition Block::getNumber(){
    onePointPosition res;
    res.x = myRow;
    res.y = myColumn;
    return res;
}

void Block::mousePressEvent(QMouseEvent *event){
    onePointPosition position;
    if (event->button()==Qt::LeftButton){
        position.x = myRow;
        position.y = myColumn;
//        flag_getFocus = 1; 同一个数字连续点两次的情况已经在checkit讨论过了，所以就不需要这个变量了
        emit userAction(position);
    }
}


void Block::erase(){
    this->clear();
//    this->setStyleSheet("background-color:#000000");
//    this->flag_getFocus = 1;
    update();
    return;
}

void Block::drawEmbrace(const int &x, const int &y){
    QPainter myPainter(this);
    QPen myPen;
    myPen.setWidth(5);
    myPen.setColor(Qt::red);
    myPainter.setPen(myPen);
    myPainter.translate(y*PIX_SIZE,x*PIX_SIZE);
    myPainter.drawLine(0,0,PIX_SIZE,0);
    myPainter.drawLine(0,0,0,PIX_SIZE);
    myPainter.drawLine(0,PIX_SIZE,0,0);
    myPainter.drawLine(0,PIX_SIZE,PIX_SIZE,PIX_SIZE);
    myPainter.drawLine(PIX_SIZE,0,PIX_SIZE,PIX_SIZE);
    myPainter.drawLine(PIX_SIZE,0,0,0);
    myPainter.drawLine(PIX_SIZE,PIX_SIZE,PIX_SIZE,0);
    myPainter.drawLine(PIX_SIZE,PIX_SIZE,0,PIX_SIZE);
    myPainter.end();
}





