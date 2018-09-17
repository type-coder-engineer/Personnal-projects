#include "block.h"
#include <QPainter>

const int PIX_SIZE = 40;

Block::Block(QWidget* parent)
    :QLabel(parent)
{
    this->resize(100, 110);
    myRow = 0;
    myColumn = 0;
}

void Block::setNumber(int i, int j){
    myRow = i;
    myColumn = j;
}

onePointPosition Block::getNumber(){
    onePointPosition pos;
    pos.x = myRow;
    pos.y = myColumn;
    return pos;
}

void Block::mousePressEvent(QMouseEvent *event){
    onePointPosition position;
    if (event->button()==Qt::LeftButton){
        position.x = myRow;
        position.y = myColumn;
        emit userAction(position);
    }
}





