import sqlite3
import excel
import datetime

class sqliteController:
    def __init__(self):
        self.connCir=sqlite3.connect('book.db')
        self.connItem=sqlite3.connect('detail.db')
        self.CirConunter=0
        return
    def getInformByPartID(self,PartName):#返回部件其余信息
        cursor=self.connItem.execute('SELECT * FROM detail WHERE partid=?',(PartName,))
        partData=cursor.fetchone()
        return partData
    def handleCirTabDataLine(self,rowData):
        self.CirConunter+=1
        today=datetime.date.today().strftime('%Y%m%d')
        data=[]
        data.append(today+self.CirConunter)#partid
        data.append(rowData[1])#生产批号
        data.append(rowData[2])#生产台数
        data.append(rowData[3])#部品番号
        return

    ###用于初始化数据库
    def initData(self,excelCtl):
        self.connItem.execute('CREATE TABLE IF NOT EXISTS detail (id INTEGER PRIMARY KEY AUTOINCREMENT, partid TEXT,material TEXT,norm TEXT,num TEXT)')
        return
    def insertItemData(self,rowData):
        self.connItem.execute('INSERT INTO detail (partid,material,norm,num) VALUES (?,?,?,?)',(rowData[0],rowData[1],rowData[2],rowData[3]))
        return
    def commitSqlite(self):
        self.connItem.commit()
        return

if __name__=='__main__':#将excel中的数据导入到sqlite中
    sqlCtl=sqliteController()
    excelCtl=excel.ExcelReader()
    excelCtl.initFile('detail.xlsx')
    sqlCtl.initData(excelCtl)
    while True:
        rowData=excelCtl.getItemSheetData()
        if rowData==[]:
            break
        sqlCtl.insertItemData(rowData)
    sqlCtl.commitSqlite()