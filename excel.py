import openpyxl

from PySide6.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
from PySide6.QtGui import QIcon

class ExcelReader:
    def __init__(self):
        self.pointerX='C'
        self.pointerY='1'
    def initFile(self,path):
        self.workbook=openpyxl.load_workbook(path)
        self.sheet=self.workbook.active
    def getSheetData(self,rowData):
        data=[]
        data.append(self.sheet[self.pointerX+self.pointerY])
        self.pointerX+=1
        self.pointerY+=1
        return data
    def getSheetAllData():
        data=[]
        rowData=None
        while getSheetData(rowData):
            data.append(rowData)
        return data

