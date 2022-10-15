from PySide6.QtWidgets import QApplication, QWidget,QMainWindow,QPushButton,QTableView,QFileDialog
from PySide6.QtCore import QFile, Signal, Slot,QAbstractTableModel,QModelIndex,Qt
from PySide6.QtUiTools import QUiLoader
from ui_mainwindow import Ui_MainWindow
from PySide6.QtGui import QColor

class MyTableModel(QAbstractTableModel):
    def __init__(self, data=None):
        QAbstractTableModel.__init__(self)
        self.dataSource=None

    def rowCount(self, parent=QModelIndex()):
        return self.row_count

    def columnCount(self, parent=QModelIndex()):
        return self.column_count

    def data(self, index, role=Qt.DisplayRole):
        column = index.column()
        row = index.row()
        if role == Qt.DisplayRole:
            cellData=self.dataSource[row][column]
            return cellData
        elif role == Qt.BackgroundRole:
            return QColor(Qt.white)
        elif role == Qt.TextAlignmentRole:
            return Qt.AlignLeft
        return None

class cirTableModel(MyTableModel):
    def __init__ (self):
        super(cirTableModel, self).__init__()
        self.load_data(None)
    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            return ("编号", "生产批号","生产台数","部品番号","定额","规格","送货量","材料","保管员","生产线","接收班组","供应商","到货日期","工序","工程名","安全标识")[section]
        else:
            return f"{section}"

    def load_data(self, data):
        self.dataSource = data
        self.column_count = 16
        if(data==None):
            self.row_count = 0
        else:
            self.row_count = len(data)
        self.layoutChanged.emit()
    def removeRow(self, row):
        self.dataSource.pop(row)
        self.row_count -= 1



class itemTableModel(MyTableModel):
    def __init__(self, data=None):
        QAbstractTableModel.__init__(self)
        self.load_data(data)
        self.dataSource=None

    def load_data(self, data):
        self.dataSource = data
        self.column_count = 4 #共4列，见headerData
        if(data==None):
            self.row_count = 0
        else:
            self.row_count = len(data)
        self.layoutChanged.emit()

    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            return ("部品番号","材料","规格","数量")[section]
        else:
            return f"{section}"

    def removeRow(self, row):
        self.dataSource.pop(row)
        self.row_count -= 1
        self.layoutChanged.emit()
