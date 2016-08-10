#-------------------------------------------------
#
# Project created by QtCreator 2016-07-08T16:56:31
#
#-------------------------------------------------

QT       += core gui
QT       += multimedia

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = lianliankan_ui
TEMPLATE = app


SOURCES += main.cpp\
        mainwindow.cpp \
        algo.cpp \
        block.cpp \
        block_area.cpp

HEADERS  += mainwindow.h \
        algo.h \
        block.h \
        block_area.h \
        filestruct.h

RESOURCES += \
    multi.qrc

DISTFILES += \
    pipi.rc

RC_FILE = pipi.rc
