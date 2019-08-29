import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets

class InforUi(QDialog):

    def __init__(self, mail):
        super(InforUi, self).__init__()
        self.mail = mail
        self.initUI()

    def initUI(self):
        self.resize(600,500)
        self.setFixedSize(self.width(), self.height())
        self.setWindowOpacity(0.9)
        self.setStyleSheet('''
                                QDialog{
                                        background:#F5F5F5;
                                        font-family: "Microsoft Yahei";}         
                                ''')

        self.inforEdit = QTextEdit(self)
        self.inforEdit.setGeometry(0, 0, 600, 500)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.initInfor()
        self.accept()
        self.inforEdit.setStyleSheet('''
                        QTextEdit{
                                color:#4F4F4F;
                                font-family:"Microsoft Yahei";
                                font-size: 17px;
                                background: transparent;
                                border:none;}
                        ''')


    def initInfor(self):
        self.setWindowTitle(' 邮件内容 ')
        message = ('主题：' + self.mail['主题'] + '\n' + '发件人：' + self.mail['发件人'] +
                   '\n' + '时间：' + self.mail['时间'] + '\n' + '主要内容：\n' +
                   self.mail['主要内容'])
        self.inforEdit.setText(message)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialag = InforUi()
    dialag.show()
    sys.exit(app.exec_())