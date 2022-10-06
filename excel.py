import openpyxl

from PySide6.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
from PySide6.QtGui import QIcon

def xPosGetter(pointx):
    pointx-=1
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    xstring=''
    if pointx<0:
        return 'A'
    elif pointx>=0:
        while pointx>=0:
            xstring+=alphabet[pointx%26]
            pointx=pointx//26-1
    return xstring[::-1]

def yPosGetter(pointy):
    return str(pointy)

class ExcelReader:
    def __init__(self):
        self.pointerX=1
        self.pointerY=1
    def initFile(self,path):
        self.workbook=openpyxl.load_workbook(path)
        self.sheet=self.workbook.active
    def getSheetData(self,data):
        xPos=self.pointerX
        yPos=self.pointerY
        if self.sheet[xPosGetter(xPos)+yPosGetter(yPos)].value==None:
            yPos+=1
            if self.sheet[xPosGetter(xPos)+yPosGetter(yPos)].value==None:
                return False
            else:
                self.pointerY=yPos
        rowData=[]#流转单；生产批号；生产台数；部品番号；定额；保管员；安全标识；送货量；生产线；工序；接收班组；供应商；工程名；到货日期；
        yPos+=3
        rowData.append(self.sheet[xPosGetter(xPos)+yPosGetter(yPos)].value)#流转单
        yPos-=3
        xPos+=2
        rowData.append(self.sheet[xPosGetter(xPos)+yPosGetter(yPos)].value)#生产批号
        xPos+=4
        rowData.append(self.sheet[xPosGetter(xPos)+yPosGetter(yPos)].value)#生产台数
        xPos-=4
        yPos+=1
        rowData.append(self.sheet[xPosGetter(xPos)+yPosGetter(yPos)].value)#部品番号
        xPos+=4
        rowData.append(self.sheet[xPosGetter(xPos)+yPosGetter(yPos)].value)#定额
        xPos-=4
        yPos+=1
        rowData.append(self.sheet[xPosGetter(xPos)+yPosGetter(yPos)].value)#保管员
        xPos+=2
        rowData.append(self.sheet[xPosGetter(xPos)+yPosGetter(yPos)].value)#安全标识
        xPos+=2
        rowData.append(self.sheet[xPosGetter(xPos)+yPosGetter(yPos)].value)#送货量
        xPos-=4
        yPos+=1
        rowData.append(self.sheet[xPosGetter(xPos)+yPosGetter(yPos)].value)#生产线
        xPos+=2
        rowData.append(self.sheet[xPosGetter(xPos)+yPosGetter(yPos)].value)#工序
        xPos+=2
        rowData.append(self.sheet[xPosGetter(xPos)+yPosGetter(yPos)].value)#接收班组
        xPos-=4
        yPos+=1
        rowData.append(self.sheet[xPosGetter(xPos)+yPosGetter(yPos)].value)#供应商
        xPos+=2
        rowData.append(self.sheet[xPosGetter(xPos)+yPosGetter(yPos)].value)#工程名
        xPos+=2
        rowData.append(self.sheet[xPosGetter(xPos)+yPosGetter(yPos)].value)#到货日期
        for i in range(len(rowData)):
            if rowData[i]==None:
                rowData[i]=''
            rowData[i]=str(rowData[i])
            rowData[i] = rowData[i].replace(u'\xa0', u'')
        print(rowData)
        data.append(rowData)
        if self.pointerX==1:
            self.pointerX=9
        elif self.pointerX==9:
            self.pointerX=1
            self.pointerY+=5
        return True
    def getSheetAllData(self):
        data=[]
        while self.getSheetData(data):
            continue
        return data

if __name__ == '__main__':
    excel=ExcelReader()
    excel.initFile('样例.xlsx')
    print(excel.getSheetAllData())
