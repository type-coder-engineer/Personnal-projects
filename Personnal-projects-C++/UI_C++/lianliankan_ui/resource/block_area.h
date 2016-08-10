#ifndef BLOCK_AREA_H
#define BLOCK_AREA_H
#include "algo.h"
#include "block.h"

#include <QObject>
#include <QWidget>
#include <QGridLayout>
#include <QSound>
#include <filestruct.h>
#include <map>

class BlockArea : public QWidget
{
    Q_OBJECT

public:
    BlockArea(int row, int column, QWidget* parent=0);
    ~BlockArea() = default;

private:
    int row;
    int column;
    void set_block_area(int row, int column);
    QGridLayout *mainLayout;
    fun *mygame;
    int oneReady;
    onePointPosition positionReady;
    void originalState(Block *block);
    int myRow;
    int myColumn;
    QSound *myBgm;
    QSound *mySuccessSound;
    int w;
    int h;
    void choosePicture(int row, int column);
    std::map<int, int> myPicture;

private slots:
    void checkIt(onePointPosition nowPosition);
    void on_reRankPicture();
    void on_gameOver();

signals:
    void gameOver();
    void reRankPicture();
};

#endif // BLOCK_AREA_H
