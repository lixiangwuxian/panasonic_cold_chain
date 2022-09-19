from qrcode import QRCode

class QrcodeMaker:
    def __init__(self):
        self.qrcode = QRCode()
    def setMessage(self, message):
        self.qrcode.add_data("https://www.baidu.com")
        self.qrcode.make()
        self.img = self.qrcode.make_image()
    def show(self):
        self.img.show()

