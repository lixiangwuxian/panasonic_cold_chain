class QrcodeController:
    def __init__(self):
        self.imageCounter=0

    def getQrCodeFromData(self, message):
        imgObj=message[17]
        imgName=self.imageCounter.__str__()
        self.imageCounter+=1
        imgName+='.png'
        imgName='./tmp/qr'+imgName
        with open(imgName, 'wb') as f:
            message[17].save(f)
        message.pop(17)
        return imgName