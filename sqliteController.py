import sqlite3
import excel
import datetime

def getStrForNum(num):
    returnStr=''
    for i in range(4):
        returnStr=chr(ord('0')+num%10)+returnStr
        num=num//10
    return returnStr
class sqliteController:
    def __init__(self):
        self.connCir=sqlite3.connect('book.db')
        self.connItem=sqlite3.connect('detail.db')
        self.CirConunter=0
        return
    def getInformByPartID(self,PartName):#返回部件其余信息
        cursor=self.connItem.execute('SELECT * FROM detail WHERE partid LIKE ?',("%"+PartName+"%",))
        partData=cursor.fetchone()
        return partData
    def searchInformByPartID(self,PartName):#返回查找到的所有部件信息
        cursor=self.connItem.execute('SELECT partid,material,norm,num,id FROM detail WHERE partid LIKE ?',("%"+PartName+"%",))
        partData=cursor.fetchall()
        return partData
    def handleCirTabDataLine(self,rowData):
        partData=self.getInformByPartID(rowData[3])
        if partData==None:
            partData=['','','','']
        self.CirConunter+=1
        today=datetime.date.today().strftime('%Y%m%d')
        data=[]
        data.append(today+getStrForNum(self.CirConunter))#编号
        data.append(rowData[1])#生产批号
        data.append(rowData[2])#生产台数
        data.append(rowData[3])#部品番号
        data.append(rowData[4])#定额
        data.append(partData[3])#规格
        data.append(rowData[7])#送货量
        data.append(partData[2])#材料
        data.append(rowData[5])#保管员
        data.append(rowData[8])#生产线
        data.append(rowData[10])#接收班组
        data.append(rowData[11])#供应商
        data.append(rowData[13])#到货日期
        data.append(rowData[9])#工序
        data.append(rowData[12])#工程名
        data.append(rowData[6])#安全标识
        data.append(rowData[0])#流转单号
        return data
    def getItemData(self):#返回detail表中所有数据
        cursor=self.connItem.execute('SELECT partid,material,norm,num,id FROM detail')
        return cursor.fetchall()
    def deleteItemRecord(self,ids):
        for id in ids:
            self.connItem.execute('DELETE FROM detail WHERE id=?',(id,))
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
    print(sqlCtl.getItemData())