#-------------------------------------------------
#
# Project created by QtCreator 2016-07-08T16:56:31
#
#-------------------------------------------------

QT       += core gui
QT       += multimedia

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = pokemon_game
TEMPLATE = app


SOURCES += main.cpp\
        mainwindow.cpp \
        block.cpp \
        block_area.cpp \
        algo.cpp \
        block_area_timer.cpp

HEADERS  += mainwindow.h \
        block.h \
        block_area.h \
        filestruct.h \
        algo.h \
        block_area_timer.h

RESOURCES += \
    multi.qrc

DISTFILES += \
    pipi.rc

RC_FILE = pipi.rc
