#include "mainwindow.h"
#include "ui_mainwindow.h"

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    excelReader=new Excel;
}

MainWindow::~MainWindow()
{
    delete ui;
}




void MainWindow::on_deletePushButton_clicked()
{

}


void MainWindow::on_importPushButton_clicked()
{
    this->excelReader->SetExcelPath();
}


void MainWindow::on_printPushButton_clicked()
{

}


void MainWindow::on_findItemPushButton_clicked()
{

}


void MainWindow::on_deleteItemRecordPushButton_clicked()
{

}

