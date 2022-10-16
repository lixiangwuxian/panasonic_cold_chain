#import qrcode


# def classReplacer(text):
#     if(text=='一厂发泡'):
#         return '1'
#     elif text=='二厂发泡':
#         return '2'
#     elif text=='三厂发泡':
#         return '16'
#     elif text=='四厂发泡':
#         return '21'
#     elif text=='组装':
#         return '8'
#     elif text=='生产准备':
#         return '19'
#     else:
#         raise Exception('班组 '+text+' 对应的序号未知')

# def messageHandler(message):
#     qrData=''
#     qrData+=message[11]#供应商
#     qrData+=','
#     qrData+=message[1]#生产批号
#     qrData+=','
#     qrData+=message[3]#部品番号
#     qrData+=','
#     qrData+=message[6]#送货量
#     qrData+=','
#     qrData+=classReplacer(message[10])#接收班组
#     #print(qrData)
#     return qrData

class QrcodeController:
    def __init__(self):
        # self.qrcoder =qrcode.QRCode(
        #     version=1,
        #     error_correction=qrcode.constants.ERROR_CORRECT_L,
        #     box_size=10,
        #     border=4
        # )
        self.imageCounter=0

    def getQrCodeFromData(self, message):
        #self.qrcoder.clear()
        #imgName=messageHandler(message)
        imgObj=message[17]
        #self.qrcoder.add_data(imgName)
        imgName=self.imageCounter.__str__()
        self.imageCounter+=1
        imgName+='.png'
        imgName='./tmp/qr'+imgName
        with open(imgName, 'wb') as f:
            message[17].save(f)
        message.pop(17)
        return imgName

# if __name__ == "__main__":
#     qrcodeMaker = QrcodeController()