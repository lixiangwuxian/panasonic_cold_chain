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

class cirTableModel(QAbstractTableModel):
    def __init__(self, data=None):
        QAbstractTableModel.__init__(self)
        self.load_data(data)
        self.dataSource=None

    def load_data(self, data):
        self.input_dates =[] # [1,2,3,4,5,6,7,8,9,10]
        self.input_magnitudes =[]# [2,3,4,5,6,7,8,9,10,11]

        self.column_count = 16 #共14列，见headerData
        self.row_count = 20

    def rowCount(self, parent=QModelIndex()):
        return self.row_count

    def columnCount(self, parent=QModelIndex()):
        return self.column_count

    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            return ("编号", "生产批号","生产台数","部品番号","定额","规格","送货量","材料","保管员","生产线","接收班组","供应商","到货日期","工序","工程名","安全标识")[section]
        else:
            return f"{section}"

    def data(self, index, role=Qt.DisplayRole):
        column = index.column()
        row = index.row()
        return None#debug
        if role == Qt.DisplayRole:
            cellData=self.dataSource[row][column]
        elif role == Qt.BackgroundRole:
            return QColor(Qt.white)
        elif role == Qt.TextAlignmentRole:
            return Qt.AlignRight
        return None

    def setDataSource(self,dataSource,row_count):
        self.dataSource=dataSource
        self.row_count=row_count
        self.layoutChanged.emit()

#class itemTableModel(QAbstractTableModel):



class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        Ui_MainWindow().setupUi(self)
        self.addEventListener()
        self.addTableForm()
        self.excelObj=ExcelReader()
    def addTableForm(self):
        print("Adding table form")
        self.circulationRecordTable=self.centralWidget().findChild(QTableView, "circulationListTableView")
        self.circulationRecordTable.setModel(cirTableModel())
        self.circulationRecordTable.verticalHeader().hide()
        #self.circulationRecordTable.horizontalHeader().setStretchLastSection(True)#无需铺满
        #self.circulationRecordTable.horizontalHeader().resizeSection(0, 50)
        self.circulationRecordTable.horizontalHeader().setDefaultSectionSize(75)
        self.circulationRecordTable.verticalHeader().setDefaultSectionSize(5);
        #self.headerWidthList=[50,100,]//todo..
        self.itemRecordTable=self.centralWidget().findChild(QTableView, "itemRecordTableView")

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
        self.excelObj.initFile(self.openFileNameDialog())
        self.circulationRecordTable.model().setDataSource(self.excelObj.getSheetDataAll(),1)
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
