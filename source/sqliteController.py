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
        self.conn=sqlite3.connect('./data/simple.db')
        #self.conn=sqlite3.connect('./data/detail.db')
        self.CirConunter=0
        return
    def getInformByPartID(self,PartName):#返回部件其余信息
        cursor=self.conn.execute('SELECT * FROM detail WHERE partid LIKE ?',("%"+PartName+"%",))
        partData=cursor.fetchone()
        return partData
    def searchInformByPartID(self,PartName):#返回查找到的所有部件信息
        cursor=self.conn.execute('SELECT partid,material,norm,num,id FROM detail WHERE partid LIKE ?',("%"+PartName+"%",))
        partData=cursor.fetchall()
        return partData
    def saveCurrentCirDataRow(self,rowData):#保存一行流转单数据
        #print(rowData)
        self.conn.execute('INSERT INTO book (编号,生产批号,生产台数,部品番号,定额,规格,送货量,材料,保管员,生产线,接收班组,供应商,到货日期,工序,工程名,安全标识,流转单号,二维码) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',rowData)
        return
    def saveCurrentCirData(self,excelData):#保存流转单数据
        self.conn.execute('CREATE TABLE IF NOT EXISTS book (编号 TEXT PRIMARY KEY, 生产批号 TEXT,生产台数 TEXT,部品番号 TEXT,定额 TEXT,规格 TEXT,送货量 TEXT,材料 TEXT,保管员 TEXT,生产线 TEXT,接收班组 TEXT,供应商 TEXT,到货日期 TEXT,工序 TEXT,工程名 TEXT,安全标识 TEXT,流转单号 TEXT,二维码 TEXT)')
        #print(excelData)
        for i in range(len(excelData)):
            self.saveCurrentCirDataRow(excelData[i])
        self.conn.commit()
        return
    def getLastTimeCirData(self):#获取上次流转单数据
        print('getLastTimeCirData')
        try:
            cursor=self.conn.execute('SELECT * FROM book')
            CirData=cursor.fetchall()
            #print(CirData)
            return CirData
        except Exception as e:
            print(e)
            return None
    def deleteCirData(self,id):#删除单行流转单数据
        self.conn.execute('DELETE FROM book WHERE 编号=?',(id[0],))
    def dropCirTable(self):#删除流转单数据
        try:
            self.conn.execute('DROP TABLE book')
        except Exception as e:
            print(e)
        self.conn.commit()
    def handleCirTabDataLine(self,rowData):#处理原始流转单数据
        partData=self.getInformByPartID(rowData[3])
        if partData==None:
            partData=['','','','']
        self.CirConunter+=1
        today=datetime.date.today().strftime('%Y%m%d')
        data=[]
        data.append(today+getStrForNum(self.CirConunter))#编号0
        data.append(rowData[1])#生产批号1
        data.append(rowData[2])#生产台数2
        data.append(rowData[3])#部品番号3
        data.append(rowData[4])#定额4
        data.append(partData[3])#规格5
        data.append(rowData[7])#送货量6
        data.append(partData[2])#材料7
        data.append(rowData[5])#保管员8
        data.append(rowData[8])#生产线9
        data.append(rowData[10])#接收班组10
        data.append(rowData[11])#供应商11
        data.append(rowData[13])#到货日期12
        data.append(rowData[9])#工序13
        data.append(rowData[12])#工程名14
        data.append(rowData[6])#安全标识15
        data.append(rowData[0])#流转单号16
        data.append(rowData[14])#二维码17
        return data
    def deleteItemRecord(self,id):#删除单行物料单数据
        self.conn.execute('DELETE FROM detail WHERE id=?',(id,))
        print("sqliteController:"+id.__str__())
    def resetCirCounter(self):#重置流转单计数编号
        self.CirConunter=0
        return

    ###以下用于初始化数据库
    def initData(self):#初始化物料单表
        try:
            self.conn.execute('DROP TABLE detail')
        except Exception as e:
            print(e)
        self.conn.execute('CREATE TABLE IF NOT EXISTS detail (id INTEGER PRIMARY KEY AUTOINCREMENT, partid TEXT,material TEXT,norm TEXT,num TEXT)')
        return
    def initDataWithOutDrop(self):
        self.conn.execute("")
    def insertItemData(self,rowData):#插入一行物料单数据
        self.conn.execute('INSERT INTO detail (partid,material,norm,num) VALUES (?,?,?,?)',(rowData[0],rowData[1],rowData[2],rowData[3]))
        return
    def commitSqlite(self):#提交数据库
        self.conn.commit()
        return

if __name__=='__main__':#将excel中的数据导入到sqlite中
    sqlCtl=sqliteController()
    excelCtl=excel.ExcelReader()
    excelCtl.initFile('./data/detail.xlsx')
    sqlCtl.initData()
    while True:
        rowData=excelCtl.getItemSheetData()
        if rowData==[]:
            break
        sqlCtl.insertItemData(rowData)
    sqlCtl.commitSqlite()