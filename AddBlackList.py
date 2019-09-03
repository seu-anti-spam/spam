import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets

class AddBlackListUi(QDialog):
    def __init__(self):
        super(AddBlackListUi, self).__init__()
        self.address = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle("添加")
        self.resize(270, 120)
        self.setFixedSize(self.width(), self.height())
        self.memberEdit = QLineEdit(self)
        self.memberEdit.setGeometry(30, 20, 211, 31)
        self.addBtn = QPushButton("添加", self)
        self.addBtn.setGeometry(90, 70, 81, 31)
        self.addBtn.clicked.connect(self.onBtnAdd)
        self.memberEdit.setPlaceholderText("请输入对方邮箱")
        self.accept()


    def onBtnAdd(self):
        self.address = self.memberEdit.text()
        print(self.address)
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialag = AddBlackListUi()
    dialag.show()
    sys.exit(app.exec_())