QT       += core gui

INCLUDEPATH += C:\Users\lixiangwuxian\vcpkg\packages\sqlite3_x86-windows\include\
               "C:\Program Files (x86)\OpenXLSX\include"

LIBS += -lcomdlg32\


greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

CONFIG += c++17

# You can make your code fail to compile if it uses deprecated APIs.
# In order to do so, uncomment the following line.
#DEFINES += QT_DISABLE_DEPRECATED_BEFORE=0x060000    # disables all the APIs deprecated before Qt 6.0.0

SOURCES += \
    src\excel.cpp \
    src\main.cpp \
    src\mainwindow.cpp \
    src\sqlite.cpp

HEADERS += \
    include\excel.h \
    include\mainwindow.h \
    include\sqlite.h

FORMS += \
    mainwindow.ui

# Default rules for deployment.
qnx: target.path = /tmp/$${TARGET}/bin
else: unix:!android: target.path = /opt/$${TARGET}/bin
!isEmpty(target.path): INSTALLS += target
