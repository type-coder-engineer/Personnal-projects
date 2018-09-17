#ifndef BLOCK_H
#define BLOCK_H

#include <QLabel>
#include "algo.h"
#include <QPixmap>
#include <QMouseEvent>
#include <filestruct.h>

class Block : public QLabel
{
    Q_OBJECT

public:
    explicit Block(QWidget* parent = 0);
    ~Block() = default;
    void setNumber(int i, int j);
    onePointPosition getNumber();

protected:
    void mousePressEvent(QMouseEvent* event);

private:
    int myRow = 0;
    int myColumn = 0;

signals:
    void userAction(onePointPosition position);

};
#endif // BLOCK_H
