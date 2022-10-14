import openpyxl
from shutil import copyfile

from PySide6.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog

from PySide6.QtGui import QIcon
import openpyxl.drawing.image
import os
import sendToPrinter

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

class ExcelWriter:
    def __init__(self):
        self.pageCounter=0
    def initFile(self,path):
        self.sourceFile=path
        #self.pageCounter+=1
        #self.target="./tmp/"+self.pageCounter.__str__()+self.sourceFile
        self.target="./tmp/"+self.sourceFile
        copyfile(self.sourceFile,self.target)
        self.workbook=openpyxl.load_workbook(self.target)
        self.sheet=self.workbook.active
        self.pointerX=1
        self.pointerY=1
    def writeRowData(self,rowData):
        self.pointerX+=2
        self.sheet[xPosGetter(self.pointerX)+yPosGetter(self.pointerY)].value=rowData[1]#生产批号
        self.pointerX+=2
        self.sheet[xPosGetter(self.pointerX)+yPosGetter(self.pointerY)].value=rowData[2]#生产台数
        self.pointerX-=2
        self.pointerY+=1
        self.sheet[xPosGetter(self.pointerX)+yPosGetter(self.pointerY)].value=rowData[3]#部品番号
        self.pointerX+=2
        self.sheet[xPosGetter(self.pointerX)+yPosGetter(self.pointerY)].value=rowData[4]#定额
        self.pointerX-=2
        self.pointerY+=1
        self.sheet[xPosGetter(self.pointerX)+yPosGetter(self.pointerY)].value=rowData[5]#规格
        self.pointerX+=2
        self.sheet[xPosGetter(self.pointerX)+yPosGetter(self.pointerY)].value=rowData[6]#送货量
        self.pointerX-=2
        self.pointerY+=1
        self.sheet[xPosGetter(self.pointerX)+yPosGetter(self.pointerY)].value=rowData[7]#材料
        self.pointerX+=2
        self.sheet[xPosGetter(self.pointerX)+yPosGetter(self.pointerY)].value=rowData[8]#保管员
        self.pointerX-=2
        self.pointerY+=1
        self.sheet[xPosGetter(self.pointerX)+yPosGetter(self.pointerY)].value=rowData[9]#生产线
        self.pointerX+=2
        self.sheet[xPosGetter(self.pointerX)+yPosGetter(self.pointerY)].value=rowData[10]#接收班组
        self.pointerX-=2
        self.pointerY+=1
        self.sheet[xPosGetter(self.pointerX)+yPosGetter(self.pointerY)].value=rowData[11]#供应商
        self.pointerX+=2
        self.sheet[xPosGetter(self.pointerX)+yPosGetter(self.pointerY)].value=rowData[12]#到货日期
        self.pointerX-=4
        self.sheet[xPosGetter(self.pointerX)+yPosGetter(self.pointerY)].value=rowData[16]#流转单号
        self.sheet[xPosGetter(self.pointerX)+yPosGetter(self.pointerY)].alignment=openpyxl.styles.Alignment(horizontal='center',vertical='center')
        self.pointerX+=5
        self.pointerY-=5
        self.sheet[xPosGetter(self.pointerX)+yPosGetter(self.pointerY)].alignment=openpyxl.styles.Alignment(horizontal='center',vertical='center')
        QRImage=openpyxl.drawing.image.Image(rowData[18])
        QRImage.anchor=xPosGetter(self.pointerX)+yPosGetter(self.pointerY)
        QRImage.width=QRImage.height=145
        self.sheet.add_image(QRImage)
        self.pointerX-=5
        if self.pointerX==1:
            self.pointerX=8
        elif self.pointerX==8:
            if self.pointerY!=22:
                self.pointerX=1
                self.pointerY+=7
            else:
                return False
                # self.saveFile(path=self.target)
                # self.printFileToPaper()#done one page
                # self.initFile(self.sourceFile)
        return True
    def writeData(self,data):
        for i in range(len(data)):
            rs=self.writeRowData(data[i])
            if rs==False:
                self.saveFile(path=self.target)
                self.printFileToPaper()
                self.initFile(self.sourceFile)
        if len(data)%8!=0:
            self.saveFile(path=self.target)
            self.printFileToPaper()
            self.initFile(self.sourceFile)
        print("Print done")
    def saveFile(self,path):
        self.workbook.save(path)
    def printFileToPaper(self):
        print('printing to paper')
        fileName=self.target
        fileName=fileName.replace('./tmp/','/tmp/')
        fileName=fileName.replace('/','\\')
        currentPath=os.getcwd()
        fileName=currentPath+fileName
        sendToPrinter.sendToPrinter(fileName)

if __name__ == '__main__':
    excel=ExcelReader()
    excel.initFile('样例.xlsx')
    print(excel.getCirSheetAllData())
