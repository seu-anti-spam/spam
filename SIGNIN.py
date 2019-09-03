import sys
import Sign
import Fail
import Suc
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QLineEdit
from PyQt5.QtCore import *

email = '@qq.com'
password = "000"
ifsf = True

# def compare(A,B):
#     if A==B:
#         ifsf = True
#     else:
#         ifsf = False

class MyTypeSignal(QObject):
    sendmsg = pyqtSignal(object)

    def run(self):
        self.sendmsg.emit()


class Sign_Window(QMainWindow, Sign.Ui_MainWindow):
    def __init__(self, MyTypeSignal):
        self.msignal = MyTypeSignal
        super(Sign_Window, self).__init__()
        self.setupUi(self)

    def closewin(self):
         # email = self.emailLine.toPlainText()
         # password = self.pwLine.toPlainText()
         if ifsf:
            self.msignal.run()
            self.close()
            # self.FailWindow.show()


class Fail_Window(QtWidgets.QWidget, Fail.Ui_Form):
    def __init__(self):
        super(Fail_Window,self).__init__()
        self.setupUi(self)

    def closewin(self):
        self.close()

    def ifshow(self):
        if not ifsf:
            self.show()

class Suc_Window(QtWidgets.QWidget, Suc.Ui_Form):
    def __init__(self):
        super(Suc_Window,self).__init__()
        self.setupUi(self)

    def closewin(self):
        self.close()

    def ifshow(self):
        if ifsf:
            self.show()


if __name__ == '__main__':
 app = QtWidgets.QApplication(sys.argv)
 SW = Sign_Window(Fail_Window)
 FW = Fail_Window()
 SucW = Suc_Window()
 SW.show()
 # SW.SignBtn.clicked.connect(lambda: compare(SW.emailLine.toPlainText(), SW.pwLine.toPlainText()))
 # print(ifsf)

 SW.SignBtn.clicked.connect(SW.closewin)
 # SW.msignal.sendmsg.connect(SucW.show)
 # SW.SignBtn.clicked.connect(FW.ifshow)
 # SW.SignBtn.clicked.connect(SucW.ifshow)
 #
 #
 # FW.RTBtn.clicked.connect(FW.closewin)

 sys.exit(app.exec_())