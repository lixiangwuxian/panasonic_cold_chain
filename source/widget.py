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
from PIL import Image

from excel import ExcelReader,ExcelWriter
from sqliteController import sqliteController
from tablesWidghtModel import cirTableModel,itemTableModel
from qrcodeController import QrcodeController


def files(curr_dir = './tmp/', ext = '*'):
  for i in glob.glob(os.path.join(curr_dir, ext)):
    yield i

class MainWindow(QMainWindow):
    def __init__(self):
        if not os.path.exists("./tmp"):
            os.mkdir("./tmp")
        super(MainWindow, self).__init__()
        self.sqliteObj=sqliteController()
        Ui_MainWindow().setupUi(self)
        self.qrcodeObj=QrcodeController()
        self.addTableForm()
        self.excelObj=ExcelReader()
        self.excelWriterObj=ExcelWriter()
        self.addEventListener()
    def addTableForm(self):#添加表格模版
        #print("Adding table form")
        self.circulationRecordTable=self.centralWidget().findChild(QTableView, "circulationListTableView")
        self.circulationRecordTable.setModel(cirTableModel())
        self.circulationRecordTable.setSelectionBehavior(QAbstractItemView.SelectRows);
        self.circulationRecordTable.verticalHeader().hide()
        self.circulationRecordTable.horizontalHeader().setDefaultSectionSize(75)
        self.circulationRecordTable.verticalHeader().setDefaultSectionSize(5);
        self.headerWidthList=[100,200,80,150,50,200,50,50,50,50,80,80,80,100,50,80]
        for i in range(len(self.headerWidthList)):
            self.circulationRecordTable.horizontalHeader().resizeSection(i, self.headerWidthList[i])
        self.reloadCirData()
        self.itemRecordTable=self.centralWidget().findChild(QTableView, "itemRecordTableView")
        self.itemRecordTable.setModel(itemTableModel())
        self.itemRecordTable.verticalHeader().hide()
        self.itemRecordTable.setSelectionBehavior(QAbstractItemView.SelectRows);
        self.itemRecordTable.horizontalHeader().setDefaultSectionSize(75)
        self.itemRecordTable.verticalHeader().setDefaultSectionSize(5);
        self.headerWidthList=[200,100,300,100]
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
        self.centralWidget().findChild(QPushButton, "insertItemRecordPushButton").clicked.connect(self.insertItemRecordPushButtonClicked)
        #self.centralWidget().findChild(QPushButton, "findItemPushButton").clicked.connect(self.finditemPushButtonClicked)
        self.centralWidget().findChild(QPushButton, "deleteItemRecordPushButton").clicked.connect(self.deleteItemRecordPushButton)
        self.centralWidget().findChild(QLineEdit, "itemIdTextEdit").textChanged.connect(self.itemIdTextEditChanged)
    def reloadCirData(self):
        self.dataSource=self.sqliteObj.getLastTimeCirData()
        #print(self.dataSource)
        if self.dataSource!=None:
            for i in range(len(self.dataSource)):
                self.dataSource[i]=list(self.dataSource[i])
                #self.dataSource[i].append(self.qrcodeObj.getQrCodeFromData(self.dataSource[i]))
        self.circulationRecordTable.model().load_data(self.dataSource)
#以下为监听事件

    def importPushButtonClicked(self):
        #print("importPushButtonClicked")
        filePath=self.openFileNameDialog()
        if filePath=="":
            return
        self.excelObj.initFile(filePath)
        self.dataSource=self.excelObj.getCirSheetAllData()
        self.sqliteObj.resetCirCounter()
        if self.dataSource==None or self.dataSource==[]:
            QMessageBox.information(self,"提示","请检查表格文件是否正确")
            return
        #self.dataSource[0][14].show()
        for i in files("./tmp","*"):
            os.remove(i)
        #print("All tmp files deleted")
        for i in range(len(self.dataSource)):
            self.dataSource[i]=self.sqliteObj.handleCirTabDataLine(self.dataSource[i])
            self.dataSource[i].append(self.qrcodeObj.getQrCodeFromData(self.dataSource[i]))
            #print(dataSource[i])
        self.circulationRecordTable.model().load_data(self.dataSource)
        self.sqliteObj.dropCirTable()
        self.sqliteObj.saveCurrentCirData(self.dataSource)
    def deletePushButtonClicked(self):
        #print("deletePushButtonClicked")
        self.cirSelectModel=self.circulationRecordTable.selectionModel()
        if(not self.cirSelectModel.hasSelection()):
            #print("No selection")
            return
        confirmDialog=QMessageBox()
        confirmDialog.setWindowTitle("提示")
        if len(self.cirSelectModel.selectedRows())>=100:
            confirmDialog.setText("确定要删除"+str(len(self.cirSelectModel.selectedRows()))+"条记录吗？删除后无法撤销\n删除大量数据可能会导致程序卡住一会，请耐心等待")
        else:
            confirmDialog.setText("确定要删除"+str(len(self.cirSelectModel.selectedRows()))+"条记录吗？删除后无法撤销")
        confirmDialog.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
        confirmDialog.setDefaultButton(QMessageBox.No)
        if(confirmDialog.exec()==QMessageBox.No):
            return
        for i in range(len(self.cirSelectModel.selectedRows())-1,-1,-1):
            self.sqliteObj.deleteCirData(self.dataSource[self.cirSelectModel.selectedRows()[i].row()])
        self.cirSelectModel.clearSelection()
        self.sqliteObj.commitSqlite()
        #self.circulationRecordTable.model().layoutChanged.emit()
        #self.itemIdTextEditChanged()
        self.reloadCirData()
    def printPushButtonClicked(self):
        #print("printPushButtonClicked")
        waitDialog=QMessageBox()
        if self.circulationRecordTable.model().dataSource is None or len(self.circulationRecordTable.model().dataSource)==0:
            return
        self.excelWriterObj.initFile("./data/打印模版.xlsx")
        waitDialog.setWindowTitle("提示")
        waitDialog.setText("正在打印，请稍后")
        waitDialog.setStandardButtons(QMessageBox.NoButton)
        waitDialog.show()
        try:
            self.excelWriterObj.writeData(self.circulationRecordTable.model().dataSource)
        except Exception as e:
            print(e)
            QMessageBox.information(self,"提示","打印出错，错误信息："+e.__str__())
        waitDialog.close()
    def insertItemRecordPushButtonClicked(self):
        #print("insertItemRecordPushButtonClicked")
        self.excelObj.initItemExcelToInsert()
        isEmpty=True
        while True:
            rowData=self.excelObj.getItemSheetData()
            #print(rowData)
            if rowData==[]:
                break
            isEmpty=False
            self.sqliteObj.insertItemData(rowData)
        if not isEmpty:
            self.sqliteObj.commitSqlite()
            self.itemIdTextEditChanged()
            QMessageBox.information(self,"提示","添加完成")
    def deleteItemRecordPushButton(self):
        #print("deleteItemRecordPushButtonClicked")
        self.itemSelectModel=self.itemRecordTable.selectionModel()
        if(not self.itemSelectModel.hasSelection()):
            #print("No selection")
            return
        confirmDialog=QMessageBox()
        confirmDialog.setWindowTitle("提示")
        if len(self.itemSelectModel.selectedRows())>=100:
            confirmDialog.setText("确认要删除"+str(len(self.itemSelectModel.selectedRows()))+"条记录吗？删除后无法撤销\n删除大量数据可能会导致程序卡住一会，请耐心等待")
        else:
            confirmDialog.setText("确认要删除"+str(len(self.itemSelectModel.selectedRows()))+"条记录吗？删除后无法撤销")
        confirmDialog.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
        confirmDialog.setDefaultButton(QMessageBox.No)
        if(confirmDialog.exec()==QMessageBox.No):
            return
        for i in range(len(self.itemSelectModel.selectedRows())-1,-1,-1):
            self.sqliteObj.deleteItemRecord(self.itemRecordTable.model().dataSource[self.itemSelectModel.selectedRows()[i].row()][4])
        self.itemSelectModel.clearSelection()
        #self.itemRecordTable.model().layoutChanged.emit()
        self.sqliteObj.commitSqlite()
        self.itemIdTextEditChanged()
    def itemIdTextEditChanged(self):
        #print("itemIdTextEditChanged")
        itemId=self.centralWidget().findChild(QLineEdit, "itemIdTextEdit").text()
        #print(itemId)
        self.itemRecordTable.model().load_data(self.sqliteObj.searchInformByPartID(itemId))

if __name__ == "__main__":
    app = QApplication([])
    mainWindow = MainWindow()
    mainWindow.setWindowTitle("松下冷链");
    mainWindow.show()
    sys.exit(app.exec())
