import openpyxl
from openpyxl_image_loader import SheetImageLoader
from shutil import copyfile
from PySide6.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
from PySide6.QtGui import QIcon
import openpyxl.drawing.image
import os
import time
from PIL import Image
import win32com.client

import sendToPrinter

def xPosGetter(pointx):#将数字转换为字母
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
def yPosGetter(pointy):#占位
    return str(pointy)

class ExcelReader:
    def __init__(self):#初始化
        return
    def initFile(self,path):#初始化文件和位置指针
        self.pointerX=1
        self.pointerY=1
        self.workbook=openpyxl.load_workbook(path)
        self.sheet=self.workbook.active
    def getCirSheetData(self,data):#获取一行流转单数据
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
        xPos+=1
        yPos-=4
        rowData.append(self.image_loader.get(xPosGetter(xPos)+yPosGetter(yPos)))#二维码14
        for i in range(0,13):
            if rowData[i]==None:
                rowData[i]=''
            rowData[i]=str(rowData[i])
            rowData[i] = rowData[i].replace(u'\xa0', u'')
        #print(rowData)
        data.append(rowData)
        if self.pointerX==1:
            self.pointerX=9
        elif self.pointerX==9:
            self.pointerX=1
            self.pointerY+=5
        return True
    def getCirSheetAllData(self):#获取所有数据
        data=[]
        self.image_loader=SheetImageLoader(self.sheet)
        while self.getCirSheetData(data):
            continue
        return data
    def getItemSheetData(self):#获取一行物料单数据
        rowData=[]
        self.pointerY+=1
        self.pointerX=1
        #if self.sheet[xPosGetter(self.pointerX)+yPosGetter(self.pointerY)].value==None:
        #    return []
        rowData.append(self.sheet[xPosGetter(self.pointerX)+yPosGetter(self.pointerY)].value)#partid
        self.pointerX+=1
        rowData.append(self.sheet[xPosGetter(self.pointerX)+yPosGetter(self.pointerY)].value)#material
        self.pointerX+=1
        rowData.append(self.sheet[xPosGetter(self.pointerX)+yPosGetter(self.pointerY)].value)#norm
        self.pointerX+=1
        rowData.append(self.sheet[xPosGetter(self.pointerX)+yPosGetter(self.pointerY)].value)#num
        if rowData==[None,None,None,None]:
            return []
        for i in range(len(rowData)):
            if rowData[i]==None:
                rowData[i]=''
            rowData[i]=str(rowData[i])
            rowData[i] = rowData[i].replace(u'\xa0', u'')
        return rowData
    def initItemExcelToInsert(self):#初始化要插入的物料单excel
        copyfile("./data/流转单添加模版.xlsx", "./tmp/流转单添加模版.xlsx")
        o = win32com.client.Dispatch('Excel.Application')
        o.visible = True
        o.DisplayAlerts = True
        o.DisplayFullScreen = True
        oBook = o.Workbooks.Open(os.path.abspath("./tmp/流转单添加模版.xlsx"))
        oSheet = oBook.Worksheets("Sheet1")
        #print("初始化物料单excel成功")
        while 1:
            try:
                while o.visible:
                    time.sleep(1)
                    #print("等待物料单excel关闭中")
                break
            except:
                continue
        #print("物料单excel已关闭")
        self.initFile("./tmp/流转单添加模版.xlsx")#为后续读入做准备

class ExcelWriter:
    def __init__(self):#初始化
        self.pageCounter=0
    def initFile(self,path):#初始化文件
        self.sourceFile=path
        #self.pageCounter+=1
        #self.target="./tmp/"+self.pageCounter.__str__()+self.sourceFile
        self.target=self.sourceFile.replace("./data/","./tmp/")
        copyfile(self.sourceFile,self.target)
        self.workbook=openpyxl.load_workbook(self.target)
        self.sheet=self.workbook.active
        self.pointerX=1
        self.pointerY=1
    def writeRowData(self,rowData):#写入一行数据
        xPos=self.pointerX
        yPos=self.pointerY
        xPos+=2
        self.sheet[xPosGetter(xPos)+yPosGetter(yPos)].value=rowData[1]#生产批号
        xPos+=4
        self.sheet[xPosGetter(xPos)+yPosGetter(yPos)].value=rowData[2]#生产台数
        xPos-=4
        yPos+=1
        self.sheet[xPosGetter(xPos)+yPosGetter(yPos)].value=rowData[3]#部品番号
        xPos+=4
        self.sheet[xPosGetter(xPos)+yPosGetter(yPos)].value=rowData[4]#定额
        xPos-=4
        yPos+=1
        self.sheet[xPosGetter(xPos)+yPosGetter(yPos)].value=rowData[5]#规格
        xPos+=4
        self.sheet[xPosGetter(xPos)+yPosGetter(yPos)].value=rowData[7]#材料7
        xPos-=4
        yPos+=1
        self.sheet[xPosGetter(xPos)+yPosGetter(yPos)].value=rowData[8]#保管员8
        xPos+=2
        self.sheet[xPosGetter(xPos)+yPosGetter(yPos)].value=rowData[15]#安全标识15
        xPos+=2
        self.sheet[xPosGetter(xPos)+yPosGetter(yPos)].value=rowData[6]#送货量6
        xPos-=4
        yPos+=1
        self.sheet[xPosGetter(xPos)+yPosGetter(yPos)].value=rowData[9]#生产线
        xPos+=2
        self.sheet[xPosGetter(xPos)+yPosGetter(yPos)].value=rowData[13]#工序13
        xPos+=2
        self.sheet[xPosGetter(xPos)+yPosGetter(yPos)].value=rowData[10]#接收班组
        xPos-=4
        yPos+=1
        self.sheet[xPosGetter(xPos)+yPosGetter(yPos)].value=rowData[11]#供应商
        xPos+=2
        self.sheet[xPosGetter(xPos)+yPosGetter(yPos)].value=rowData[14]#工程名14
        xPos+=2
        self.sheet[xPosGetter(xPos)+yPosGetter(yPos)].value=rowData[12]#到货日期
        xPos-=6
        yPos-=1
        self.sheet[xPosGetter(xPos)+yPosGetter(yPos)].value=rowData[16]#流转单号16
        #self.sheet[xPosGetter(xPos)+yPosGetter(yPos)].alignment=openpyxl.styles.Alignment(horizontal='center',vertical='center')
        xPos+=7
        yPos-=4
        self.sheet[xPosGetter(xPos)+yPosGetter(yPos)].alignment=openpyxl.styles.Alignment(horizontal='center',vertical='center')
        QRImage=openpyxl.drawing.image.Image(rowData[17])
        QRImage.anchor=xPosGetter(xPos)+yPosGetter(yPos)
        QRImage.width=QRImage.height=145
        self.sheet.add_image(QRImage)
        if self.pointerX==1:
            self.pointerX=10
        elif self.pointerX==10:
            if self.pointerY!=29:
                self.pointerX=1
                self.pointerY+=7
            else:
                return False
                # self.saveFile(path=self.target)
                # self.printFileToPaper()#done one page
                # self.initFile(self.sourceFile)
        return True
    def writeData(self,data):#写入数据
        for i in range(len(data)):
            rs=self.writeRowData(data[i])
            if rs==False:
                self.saveFile(path=self.target)
                self.printFileToPaper()
                self.initFile(self.sourceFile)
        if len(data)%10!=0:
            self.saveFile(path=self.target)
            self.printFileToPaper()
            self.initFile(self.sourceFile)
        print("Print done")
    def saveFile(self,path):#保存文件
        self.workbook.save(path)
    def printFileToPaper(self):#打印文件
        print('printing to paper')
        fileName=self.target
        fileName=fileName.replace('./tmp/','/tmp/')
        fileName=fileName.replace('/','\\')
        currentPath=os.getcwd()
        fileName=currentPath+fileName
        sendToPrinter.sendToPrinter(fileName)
# if __name__ == '__main__':
#     excel=ExcelReader()
#     excel.initFile('样例.xlsx')
#     print(excel.getCirSheetAllData())
