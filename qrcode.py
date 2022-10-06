import qrcode

class QrcodeMaker:
    def __init__(self):
        self.qrcoder = qrcode()
    def setMessage(self, message):
        self.qrcoder.add_data(message)
        self.qrcoder.make()
        self.img = self.qrcoder.make_image()
    def show(self):
        self.img.show()

if __name__ == "__main__":
    qrcodeMaker = QrcodeMaker()
    qrcodeMaker.setMessage("https://www.baidu.com")
    qrcodeMaker.show()