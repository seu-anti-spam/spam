import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore, QtGui, QtWidgets
import imap


class AddBlackListUi(QDialog):
    def __init__(self):
        super(AddBlackListUi, self).__init__()
        self.address = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle("添加")
        # self.setWindowIcon(QIcon('images/nlogo.png'))
        self.resize(270, 120)
        self.setFixedSize(self.width(), self.height())
        self.memberEdit = QLineEdit(self)
        self.memberEdit.setGeometry(30, 20, 211, 31)
        self.addBtn = QPushButton("添加", self)
        self.addBtn.setGeometry(90, 70, 81, 31)
        self.addBtn.clicked.connect(self.onBtnAdd)
        self.memberEdit.setPlaceholderText("请输入对方邮箱")
        self.accept()
        self.setStyleSheet('''
                        QDialog{
                                background:white;
                                font-family: "Microsoft Yahei";}
                ''')
        self.addBtn.setStyleSheet('''QPushButton
                                                 {text-align : center;
                                                 background-color : white;
                                                 font: bold;
                                                 font-family: "Microsoft Yahei";
                                                 border-color: gray;
                                                 border-width: 2px;
                                                 border-radius: 10px;
                                                 padding: 6px;
                                                 height : 14px;
                                                 border-style: outset;
                                                 font : 14px;}
                                                 QPushButton:pressed
                                                 {text-align : center;
                                                 background-color : light gray;
                                                 font: bold;
                                                 border-color: gray;
                                                 border-width: 2px;
                                                 border-radius: 10px;
                                                 padding: 6px;
                                                 height : 14px;
                                                 border-style: outset;
                                                 font : 14px;}''')
        self.memberEdit.setStyleSheet('''
                                    QLineEdit{
                                        color:#4F4F4F;
                                        font-family:"Segoe UI";
                                        border:solid;
                                        border-radius:8px;
                                        padding:2px 4px;}
                                        ''')


    def onBtnAdd(self):
        self.address = self.memberEdit.text()
        if '@' in self.address:
            imap.black_list.append(self.address)
            self.close()
        else:
            reply = QMessageBox.warning(self, '!', '邮箱格式不正确', QMessageBox.Yes)
            reply.setStyleSheet('''
            QMessageBox{
            
            ''')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialag = AddBlackListUi()
    dialag.show()
    sys.exit(app.exec_())
    sys.exit(app.exec_())