import sys
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QDialog
from PyQt5.QtCore import *
from PyQt5.QtGui import QMovie
import time

class BackendThread(QThread):
    closeself_emit = pyqtSignal()

    def run(self):
        while True:
            time.sleep(2)
            if True:
                self.closeself_emit.emit()

class LoadingGif(QDialog):
    def __init__(self):
        super().__init__()
        self.backThreadinit()
        self.label = QLabel("", self)
        self.setFixedSize(128, 128)
        self.setWindowFlags(Qt.Dialog | Qt.CustomizeWindowHint)
        self.movie = QMovie('./images/loading.gif')
        # self.movie.setScaledSize()
        self.label.setMovie(self.movie)

        # 构建一个计时器
        self.timer = QBasicTimer()
        # 计数
        self.step = 0


        self.movie.start()
    def backThreadinit(self):
        self.backend = BackendThread()
        self.backend.closeself_emit.connect(self.handle)
        self.backend.start()

    def handle(self):
        self.close()
        self.backend.terminate()
        pass


if __name__ =="__main__":
    app = QApplication(sys.argv)
    form = LoadingGif()
    form.show()
    sys.exit(app.exec_())