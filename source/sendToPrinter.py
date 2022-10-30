import win32com.client
import os

def sendToPrinter(path):
    o = win32com.client.Dispatch('Excel.Application')
    o.visible = False
    o.DisplayAlerts = False
    print(path)
    wb = o.Workbooks.Open(os.path.abspath(path))
    try:
        ws=wb.Worksheets(1)
        if ws is None:
            print('open failed')
            return
        ws.PageSetup.Zoom = False
        ws.PageSetup.FitToPagesTall = False
        ws.PageSetup.FitToPagesWide = 1
    except Exception as e:
        print(e)
    finally:
        try:
            wb.PrintOut()
        except Exception as e:
            print(e)
        finally:
            wb.Close(SaveChanges=False)
            o.Quit()