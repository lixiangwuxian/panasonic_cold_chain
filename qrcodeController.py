import qrcode

def classReplacer(text):
    if text=='四厂发泡':
        return '21'
    if text=='二厂发泡':
        return '2'
    if text=='三厂发泡':
        return '16'
    if text=='组装':
        return '8'

def messageHandler(message):
    qrData=''
    qrData+=message[17]#供应商
    qrData+=','
    qrData+=message[1]#生产批号
    qrData+=','
    qrData+=message[3]#部品番号
    qrData+=','
    qrData+=message[6]#送货量
    qrData+=','
    qrData+=classReplacer(message[10])#接收班组
    #print(qrData)
    return qrData

class QrcodeController:
    def __init__(self):
        self.qrcoder =qrcode.QRCode()
    def getQrCodeFromData(self, message):
        self.qrcoder.clear()
        imgName=messageHandler(message)
        self.qrcoder.add_data(imgName)
        imgName+='.png'
        imgName='./tmp/qr'+imgName
        with open(imgName, 'wb') as f:
            self.qrcoder.make_image().save(f)
        return imgName

if __name__ == "__main__":
    qrcodeMaker = QrcodeController()