from xlrd import open_workbook
import win32com.client

def sendToPrinter(path):
    o = win32com.client.Dispatch('Excel.Application')
    o.visible = False
    o.DisplayAlerts = False
    wb = o.Workbooks.Open(path)
    wb.PrintOut()
    wb.Close(SaveChanges=False)
    o.Quit()