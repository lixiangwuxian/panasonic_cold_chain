#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <stdio.h>
#include "excel.h"
#include "sqlite.h"

QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

private slots:

    void on_deletePushButton_clicked();

    void on_importPushButton_clicked();

    void on_printPushButton_clicked();

    void on_findItemPushButton_clicked();

    void on_deleteItemRecordPushButton_clicked();

private:
    Ui::MainWindow *ui;
    Excel* excelReader;
};
#endif // MAINWINDOW_H
