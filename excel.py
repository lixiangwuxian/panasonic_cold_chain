import openpyxl
class ExcelReader:
    def __init__(self):
        return
    def read(self, path):
        workbook=openpyxl.load_workbook(path)