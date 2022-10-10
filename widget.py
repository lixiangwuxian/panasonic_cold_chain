# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys
import win32api

from PySide6.QtWidgets import QApplication, QWidget,QMainWindow,QPushButton,QTableView,QFileDialog
from PySide6.QtCore import QFile, Signal, Slot,QAbstractTableModel,QModelIndex,Qt
from PySide6.QtUiTools import QUiLoader
from ui_mainwindow import Ui_MainWindow
from PySide6.QtGui import QColor

from excel import ExcelReader
from sqliteController import sqliteController
from tablesWidghtModel import cirTableModel,itemTableModel

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        Ui_MainWindow().setupUi(self)
        self.addEventListener()
        self.addTableForm()
        self.excelObj=ExcelReader()
        self.sqliteObj=sqliteController()
    def addTableForm(self):
        print("Adding table form")
        self.circulationRecordTable=self.centralWidget().findChild(QTableView, "circulationListTableView")
        self.circulationRecordTable.setModel(cirTableModel())
        self.circulationRecordTable.verticalHeader().hide()
        #self.circulationRecordTable.horizontalHeader().resizeSection(0, 50)
        self.circulationRecordTable.horizontalHeader().setDefaultSectionSize(75)
        self.circulationRecordTable.verticalHeader().setDefaultSectionSize(5);
        self.headerWidthList=[100,150,80,150,50,180,50,50,50,50,80,80,80,100,50,80]
        for i in range(len(self.headerWidthList)):
            self.circulationRecordTable.horizontalHeader().resizeSection(i, self.headerWidthList[i])
        self.itemRecordTable=self.centralWidget().findChild(QTableView, "itemRecordTableView")
        self.itemRecordTable.setModel(itemTableModel())
        self.itemRecordTable.verticalHeader().hide()
        self.itemRecordTable.horizontalHeader().setDefaultSectionSize(75)
        self.itemRecordTable.verticalHeader().setDefaultSectionSize(5);
        self.headerWidthList=[200,150,200,100]
        for i in range(len(self.headerWidthList)):
            self.itemRecordTable.horizontalHeader().resizeSection(i, self.headerWidthList[i])

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"打开表格文件", "","表格文件 (*.xlsx *.xls);;All Files (*)", options=options)
        if fileName:
            print(fileName)
        return fileName
    def addEventListener(self):
        self.centralWidget().findChild(QPushButton, "importPushButton").clicked.connect(self.importPushButtonClicked)
        self.centralWidget().findChild(QPushButton, "deletePushButton").clicked.connect(self.deletePushButtonClicked)
        self.centralWidget().findChild(QPushButton, "printPushButton").clicked.connect(self.printPushButtonClicked)
        self.centralWidget().findChild(QPushButton, "findItemPushButton").clicked.connect(self.finditemPushButtonClicked)
        self.centralWidget().findChild(QPushButton, "deleteItemRecordPushButton").clicked.connect(self.deleteItemRecordPushButton)

    def importPushButtonClicked(self):
        print("importPushButtonClicked")
        filePath=self.openFileNameDialog()
        if filePath==None:
            return
        self.excelObj.initFile(filePath)
        dataSource=self.excelObj.getCirSheetAllData()
        for i in range(len(dataSource)):
            dataSource[i]=self.sqliteObj.handleCirTabDataLine(dataSource[i])
            print(dataSource[i])
        self.circulationRecordTable.model().load_data(dataSource)
    def deletePushButtonClicked(self):
        print("deletePushButtonClicked")
    def printPushButtonClicked(self):
        print("printPushButtonClicked")
    def finditemPushButtonClicked(self):
        print("finditemPushButtonClicked")
    def deleteItemRecordPushButton(self):
        print("deleteItemRecordPushButtonClicked")

if __name__ == "__main__":
    app = QApplication([])
    mainWindow = MainWindow()
    mainWindow.setWindowTitle("松下冷链");
    mainWindow.show()
    sys.exit(app.exec_())
