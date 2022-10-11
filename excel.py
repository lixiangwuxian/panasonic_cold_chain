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
        return
    def initFile(self,path):
        self.pointerX=1
        self.pointerY=1
        self.workbook=openpyxl.load_workbook(path)
        self.sheet=self.workbook.active
    def getCirSheetData(self,data):
        xPos=self.pointerX
        yPos=self.pointerY
        if self.sheet[xPosGetter(xPos)+yPosGetter(yPos)].value==None:
            yPos+=1
            if self.sheet[xPosGetter(xPos)+yPosGetter(yPos)].value==None:
                return False
            else:
                self.pointerY=yPos
        if self.sheet[xPosGetter(xPos)+yPosGetter(yPos)].value!="流":
            return False#不是流转单表
        rowData=[]#流转单；生产批号；生产台数；部品番号；定额；保管员；安全标识；送货量；生产线；工序；接收班组；供应商；工程名；到货日期；
        yPos+=3
        rowData.append(self.sheet[xPosGetter(xPos)+yPosGetter(yPos)].value)#流转单0
        yPos-=3
        xPos+=2
        rowData.append(self.sheet[xPosGetter(xPos)+yPosGetter(yPos)].value)#生产批号
        xPos+=4
        rowData.append(self.sheet[xPosGetter(xPos)+yPosGetter(yPos)].value)#生产台数2
        xPos-=4
        yPos+=1
        rowData.append(self.sheet[xPosGetter(xPos)+yPosGetter(yPos)].value)#部品番号
        xPos+=4
        rowData.append(self.sheet[xPosGetter(xPos)+yPosGetter(yPos)].value)#定额
        xPos-=4
        yPos+=1
        rowData.append(self.sheet[xPosGetter(xPos)+yPosGetter(yPos)].value)#保管员5
        xPos+=2
        rowData.append(self.sheet[xPosGetter(xPos)+yPosGetter(yPos)].value)#安全标识
        xPos+=2
        rowData.append(self.sheet[xPosGetter(xPos)+yPosGetter(yPos)].value)#送货量
        xPos-=4
        yPos+=1
        rowData.append(self.sheet[xPosGetter(xPos)+yPosGetter(yPos)].value)#生产线
        xPos+=2
        rowData.append(self.sheet[xPosGetter(xPos)+yPosGetter(yPos)].value)#工序9
        xPos+=2
        rowData.append(self.sheet[xPosGetter(xPos)+yPosGetter(yPos)].value)#接收班组
        xPos-=4
        yPos+=1
        rowData.append(self.sheet[xPosGetter(xPos)+yPosGetter(yPos)].value)#供应商
        xPos+=2
        rowData.append(self.sheet[xPosGetter(xPos)+yPosGetter(yPos)].value)#工程名12
        xPos+=2
        rowData.append(self.sheet[xPosGetter(xPos)+yPosGetter(yPos)].value)#到货日期13
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
    def getCirSheetAllData(self):
        data=[]
        while self.getCirSheetData(data):
            continue
        return data
    def getItemSheetData(self):
        rowData=[]
        self.pointerY+=1
        self.pointerX=1
        if self.sheet[xPosGetter(self.pointerX)+yPosGetter(self.pointerY)].value==None:
            return []
        rowData.append(self.sheet[xPosGetter(self.pointerX)+yPosGetter(self.pointerY)].value)#partid
        self.pointerX+=1
        rowData.append(self.sheet[xPosGetter(self.pointerX)+yPosGetter(self.pointerY)].value)#material
        self.pointerX+=1
        rowData.append(self.sheet[xPosGetter(self.pointerX)+yPosGetter(self.pointerY)].value)#norm
        self.pointerX+=1
        rowData.append(self.sheet[xPosGetter(self.pointerX)+yPosGetter(self.pointerY)].value)#num
        for i in range(len(rowData)):
            if rowData[i]==None:
                rowData[i]=''
            rowData[i]=str(rowData[i])
            rowData[i] = rowData[i].replace(u'\xa0', u'')
        return rowData

if __name__ == '__main__':
    excel=ExcelReader()
    excel.initFile('样例.xlsx')
    print(excel.getCirSheetAllData())
