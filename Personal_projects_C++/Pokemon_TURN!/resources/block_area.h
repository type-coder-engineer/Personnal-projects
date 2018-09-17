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
    BlockArea(int level, QWidget* parent = 0);
    ~BlockArea() = default;

private:
    QGridLayout *mainLayout = NULL;
    fun *mygame;
    int oneReady;
    bool frozon = false;
    onePointPosition positionReady;
    int myRow;
    int myColumn;
    int myLevel;
    std::vector<int> level1;
    std::vector<int> level2;
    std::vector<int> level3;
    QSound *myBgm;
    QSound *mySuccessSound;
    int w;
    int h;
    std::map<int, int> myPicture;
    void choosePicture();
    void set_block_area();
    void originalState(Block *block);
    void clickState(Block *block);

private slots:
    void checkIt(onePointPosition nowPosition);
//    void on_gameOver();

signals:
    void gameOver();
};

#endif // BLOCK_AREA_H
