# This Python file uses the following encoding: utf-8
import os
import glob
from pathlib import Path
import sys
import win32api

from PySide6.QtWidgets import QApplication,QAbstractItemView, QWidget,QMainWindow,QPushButton,QTableView,QFileDialog,QLineEdit,QMessageBox
from PySide6.QtCore import QFile, Signal, Slot,QAbstractTableModel,QModelIndex,Qt
from PySide6.QtUiTools import QUiLoader
from ui_mainwindow import Ui_MainWindow
from PySide6.QtGui import QColor

from excel import ExcelReader,ExcelWriter
from sqliteController import sqliteController
from tablesWidghtModel import cirTableModel,itemTableModel
from qrcodeController import QrcodeController


def files(curr_dir = './tmp/', ext = '*'):       #  当前目录下的文件
  for i in glob.glob(os.path.join(curr_dir, ext)):
    yield i

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.sqliteObj=sqliteController()
        Ui_MainWindow().setupUi(self)
        self.addTableForm()
        self.excelObj=ExcelReader()
        self.printObj=ExcelWriter()
        self.qrcodeObj=QrcodeController()
        self.addEventListener()

    def addTableForm(self):
        print("Adding table form")
        self.circulationRecordTable=self.centralWidget().findChild(QTableView, "circulationListTableView")
        self.circulationRecordTable.setModel(cirTableModel())
        self.circulationRecordTable.setSelectionBehavior(QAbstractItemView.SelectRows);
        self.circulationRecordTable.verticalHeader().hide()
        self.circulationRecordTable.horizontalHeader().setDefaultSectionSize(75)
        self.circulationRecordTable.verticalHeader().setDefaultSectionSize(5);
        self.headerWidthList=[100,150,80,150,50,180,50,50,50,50,80,80,80,100,50,80]
        for i in range(len(self.headerWidthList)):
            self.circulationRecordTable.horizontalHeader().resizeSection(i, self.headerWidthList[i])
        self.itemRecordTable=self.centralWidget().findChild(QTableView, "itemRecordTableView")
        self.itemRecordTable.setModel(itemTableModel())
        self.itemRecordTable.verticalHeader().hide()
        self.itemRecordTable.setSelectionBehavior(QAbstractItemView.SelectRows);
        self.itemRecordTable.horizontalHeader().setDefaultSectionSize(75)
        self.itemRecordTable.verticalHeader().setDefaultSectionSize(5);
        self.headerWidthList=[200,150,200,100]
        for i in range(len(self.headerWidthList)):
            self.itemRecordTable.horizontalHeader().resizeSection(i, self.headerWidthList[i])
        self.itemRecordTable.model().load_data(self.sqliteObj.searchInformByPartID(''))

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"打开表格文件", "","表格文件 (*.xlsx);;All Files (*)", options=options)
        return fileName

    def addEventListener(self):
        self.centralWidget().findChild(QPushButton, "importPushButton").clicked.connect(self.importPushButtonClicked)
        self.centralWidget().findChild(QPushButton, "deletePushButton").clicked.connect(self.deletePushButtonClicked)
        self.centralWidget().findChild(QPushButton, "printPushButton").clicked.connect(self.printPushButtonClicked)
        #self.centralWidget().findChild(QPushButton, "findItemPushButton").clicked.connect(self.finditemPushButtonClicked)
        self.centralWidget().findChild(QPushButton, "deleteItemRecordPushButton").clicked.connect(self.deleteItemRecordPushButton)
        self.centralWidget().findChild(QLineEdit, "itemIdTextEdit").textChanged.connect(self.itemIdTextEditChanged)

    def importPushButtonClicked(self):
        print("importPushButtonClicked")
        filePath=self.openFileNameDialog()
        if filePath=="":
            return
        self.excelObj.initFile(filePath)
        dataSource=self.excelObj.getCirSheetAllData()
        for i in range(len(dataSource)):
            dataSource[i]=self.sqliteObj.handleCirTabDataLine(dataSource[i])
            dataSource[i].append(self.qrcodeObj.getQrCodeFromData(dataSource[i]))
            #print(dataSource[i])
        #dataSource[0][18].show()
        self.circulationRecordTable.model().load_data(dataSource)

    def deletePushButtonClicked(self):
        print("deletePushButtonClicked")
        self.cirSelectModel=self.circulationRecordTable.selectionModel()
        if(not self.cirSelectModel.hasSelection()):
            #print("No selection")
            return
        confirmDialog=QMessageBox()
        confirmDialog.setWindowTitle("提示")
        confirmDialog.setText("确认删除？")
        confirmDialog.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
        confirmDialog.setDefaultButton(QMessageBox.No)
        if(confirmDialog.exec()==QMessageBox.No):
            return
        for i in self.cirSelectModel.selectedRows():
            self.circulationRecordTable.model().removeRow(self.cirSelectModel.selectedRows()[0].row())

    def printPushButtonClicked(self):
        print("printPushButtonClicked")
        self.printObj.initFile("打印模版.xlsx")
        self.printObj.writeData(self.circulationRecordTable.model().dataSource)

    def deleteItemRecordPushButton(self):
        print("deleteItemRecordPushButtonClicked")
        self.itemSelectModel=self.itemRecordTable.selectionModel()
        if(not self.itemSelectModel.hasSelection()):
            #print("No selection")
            return
        confirmDialog=QMessageBox()
        confirmDialog.setWindowTitle("提示")
        confirmDialog.setText("确认删除？")
        confirmDialog.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
        confirmDialog.setDefaultButton(QMessageBox.No)
        if(confirmDialog.exec()==QMessageBox.No):
            return
        for i in self.itemSelectModel.selectedRows():
            self.sqliteObj.deleteItemRecord(self.itemRecordTable.model().dataSource[self.itemSelectModel.selectedRows()[0].row()][4])
            self.itemRecordTable.model().removeRow(self.itemSelectModel.selectedRows()[0].row())
            self.itemRecordTable.model().layoutChanged.emit()
            self.sqliteObj.commitSqlite()

    def itemIdTextEditChanged(self):
        print("itemIdTextEditChanged")
        itemId=self.centralWidget().findChild(QLineEdit, "itemIdTextEdit").text()
        #print(itemId)
        self.itemRecordTable.model().load_data(self.sqliteObj.searchInformByPartID(itemId))

if __name__ == "__main__":
    app = QApplication([])
    mainWindow = MainWindow()
    mainWindow.setWindowTitle("松下冷链");
    mainWindow.show()
    if app.exec() == 0:
        print("exit")
        for i in files("./tmp","*"):
            os.remove(i)
        print("All tmp files deleted")
    sys.exit(0)
