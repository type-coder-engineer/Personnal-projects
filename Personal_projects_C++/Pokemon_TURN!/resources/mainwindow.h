#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include "block_area.h"
#include "block_area_timer.h"
#include "algo.h"
#include <QMenu>
#include <QAction>
#include <QActionGroup>
#include <QRadioButton>
#include <vector>
#include <algorithm>
#include <unordered_map>
#include <string>

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = 0);
    ~MainWindow();

private:
    int gameLevel = 1;
    bool first50 = false;
    bool first100 = false;
    bool superRare = false;
    bool catchAll = false;
    std::vector<int> caught;
    std::vector<int> found;
    std::unordered_map<int, QString> nameMap;
    std::vector<QString> names = {
        "妙蛙种子",
        "妙蛙草",
        "妙蛙花",
        "小火龙",
        "火恐龙",
        "喷火龙",
        "杰尼龟",
        "卡咪龟",
        "水箭龟",
        "绿毛虫",
        "铁甲蛹",
        "巴大蝶",
        "独角虫",
        "铁壳蛹",
        "大针蜂",
        "波波",
        "比比鸟",
        "大比鸟",
        "小拉达",
        "拉达",
        "烈雀",
        "大嘴雀",
        "阿柏蛇",
        "阿柏怪",
        "皮卡丘",
        "雷丘",
        "穿山鼠",
        "穿山王",
        "尼多兰",
        "尼多娜",
        "尼多后",
        "尼多朗",
        "尼多力诺",
        "尼多王",
        "皮皮",
        "皮可西",
        "六尾",
        "九尾",
        "胖丁",
        "胖可丁",
        "超音蝠",
        "大嘴蝠",
        "走路草",
        "臭臭花",
        "霸王花",
        "派拉斯",
        "派拉斯特",
        "毛球",
        "摩鲁蛾",
        "地鼠",
        "三地鼠",
        "喵喵",
        "猫老大",
        "可达鸭",
        "哥达鸭",
        "猴怪",
        "火暴猴",
        "卡蒂狗",
        "风速狗",
        "蚊香蝌蚪",
        "蚊香君",
        "蚊香泳士",
        "凯西",
        "勇基拉",
        "胡地",
        "腕力",
        "豪力",
        "怪力",
        "喇叭芽",
        "口呆花",
        "大食花",
        "玛瑙水母",
        "毒刺水母",
        "小拳石",
        "隆隆石",
        "隆隆岩",
        "小火马",
        "烈焰马",
        "呆呆兽",
        "呆壳兽",
        "小磁怪",
        "三合一磁",
        "大葱鸭",
        "嘟嘟",
        "嘟嘟利",
        "小海狮",
        "白海狮",
        "臭泥",
        "臭臭泥",
        "大舌贝",
        "刺甲贝",
        "鬼斯",
        "鬼斯通",
        "耿鬼",
        "大岩蛇",
        "催眠貘",
        "引梦貘人",
        "大钳蟹",
        "巨钳蟹",
        "霹雳电球",
        "顽皮雷弹",
        "蛋蛋",
        "椰蛋树",
        "卡拉卡拉",
        "嘎啦嘎啦",
        "飞腿郎",
        "快拳郎",
        "大舌头",
        "瓦斯弹",
        "双弹瓦斯",
        "独角犀牛",
        "钻角犀兽",
        "吉利蛋",
        "蔓藤怪",
        "袋兽",
        "墨海马",
        "海刺龙",
        "角金鱼",
        "金鱼王",
        "海星星",
        "宝石海星",
        "魔墙人偶",
        "飞天螳螂",
        "迷唇姐",
        "电击兽",
        "鸭嘴火兽",
        "凯罗斯",
        "肯泰罗",
        "鲤鱼王",
        "暴鲤龙",
        "拉普拉斯",
        "百变怪",
        "伊布",
        "水伊布",
        "雷伊布",
        "火伊布",
        "3D龙",
        "菊石兽",
        "多刺菊石",
        "化石盔",
        "镰刀盔",
        "化石翼龙",
        "卡比兽",
        "急冻鸟",
        "闪电鸟",
        "火焰鸟",
        "迷你龙",
        "哈克龙",
        "快龙",
        "超梦",
        "梦幻"
    };
    void createMenus();
    void createActions();
    QAction *easy_action;
    QAction *middle_action;
    QAction *hard_action;
    QAction *new_training_action;
    QAction *new_catch_action;
    QAction *exit_action;
    QAction *dictionary_action;
    QAction *about_game_action;
    QAction *about_qt_action;
    QActionGroup *levelActionGroup;

    QMenu *game_menu;
    QMenu *level_menu;
    QMenu *help_menu;
    inline bool find_it(int i, std::vector<int> caught);
    void readSetting();
    void writeSetting();
    void closeEvent(QCloseEvent*);

private slots:
    void on_trainingWin();
    void on_catchWin();
    void on_catchLose();
    void on_about_game();
    void on_newGameTraining();
    void on_newGameCatch();
    void on_welcome();
    void on_dictionary();
    void on_selectMode();
    void on_level(QAction *levelAction);
};

#endif // MAINWINDOW_H
