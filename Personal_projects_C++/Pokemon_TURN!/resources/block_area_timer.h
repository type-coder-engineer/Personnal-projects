#ifndef BLOCK_AREA_TIMER_H
#define BLOCK_AREA_TIMER_H
#include "algo.h"
#include "block.h"
#include <QObject>
#include <QWidget>
#include <QGridLayout>
#include <QSound>
#include <map>
#include <QTimer>
#include <QProgressBar>
#include <filestruct.h>

class BlockAreaCatch : public QWidget
{
    Q_OBJECT

public:
    BlockAreaCatch(int level, QWidget* parent = 0);
    ~BlockAreaCatch() = default;
    std::vector<int> getResult();

private:
    QVBoxLayout *mainLayout = NULL;
    QHBoxLayout *hLayout = NULL;
    QGridLayout *gridLayout = NULL;
    fun *mygame = NULL;
    int oneReady;
    bool frozon = false;
    onePointPosition positionReady;
    int myRow;
    int myColumn;
    int myLevel;
    std::vector<int> level1;
    std::vector<int> level2;
    std::vector<int> level3;
    QSound *mySuccessSound;
    int w;
    int h;
    int counter;
    QTimer timer;
    QProgressBar *bar = NULL;
    std::map<int, int> myPicture;
    void choosePicture();
    void set_block_area();
    void originalState(Block *block);
    void clickState(Block *block);
    std::vector<int> res;

private slots:
    void checkIt(onePointPosition nowPosition);
    void updateProgressbar();

signals:
    void gameWin();
    void gameLose();
};

#endif // BLOCK_AREA_TIMER_H
