# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys

from PySide6.QtWidgets import QApplication, QWidget,QMainWindow,QPushButton
from PySide6.QtCore import QFile, Signal, Slot
from PySide6.QtUiTools import QUiLoader
from ui_mainwindow import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        Ui_MainWindow().setupUi(self)
        self.addEventListener()
    def addEventListener(self):
        self.centralWidget().findChild(QPushButton, "importPushButton").clicked.connect(self.importPushButtonClicked)
        self.centralWidget().findChild(QPushButton, "deletePushButton").clicked.connect(self.deletePushButtonClicked)
        self.centralWidget().findChild(QPushButton, "printPushButton").clicked.connect(self.printPushButtonClicked)
        self.centralWidget().findChild(QPushButton, "findItemPushButton").clicked.connect(self.finditemPushButtonClicked)
        self.centralWidget().findChild(QPushButton, "deleteItemRecordPushButton").clicked.connect(self.deleteItemRecordPushButton)

    def importPushButtonClicked(self):
        print("importPushButtonClicked")
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
