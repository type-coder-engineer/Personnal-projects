#-------------------------------------------------
#
# Project created by QtCreator 2016-06-27T09:57:34
#
#-------------------------------------------------

QT       += core gui

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = 2048ui
TEMPLATE = app


SOURCES += main.cpp\
        mainwindow.cpp \
    app.cpp

HEADERS  += mainwindow.h \
    app.h

FORMS    += mainwindow.ui

DISTFILES += \
    2048.rc

RC_FILE = 2048.rc
