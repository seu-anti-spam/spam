import sys
from PyQt5.QtWidgets import *
import time
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets

class MymessageBox(QWidget):
    def __init__(self, txt):
        super(MymessageBox, self).__init__()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.close)
        self.timer.setSingleShot(True)
        self.timer.start(5000)
        self.txt = txt
        self.initUI()

    def initUI(self):
        self.resize(250, 150)
        self.desktop = QDesktopWidget()
        self.label = QLabel(self)
        self.label.setGeometry(0,0,250,150)
        self.label.setText(self.txt)
        self.move((self.desktop.availableGeometry().width() - self.width()),
                  self.desktop.availableGeometry().height()-self.height())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialag = MymessageBox("你好")
    dialag.show()
    sys.exit(app.exec_())