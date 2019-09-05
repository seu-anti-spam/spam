# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow_UI.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class Ui_MainWindow(object):

    # def __init__(self):
    #     super().__init__()
    #     self.ui = MainWindow()
    #     self.ui.setupUi(self)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(400, 520)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        # MainWindow.setWindowIcon(QIcon('LOGO.png'))
        MainWindow.setWindowOpacity(0.9)
        MainWindow.setWindowFlags(Qt.FramelessWindowHint)
        MainWindow.setStyleSheet('''
                QWidget{
                        border-radius:10px;}
        ''')
        # palette = QtGui.QPalette()
        # palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(QtGui.QPixmap("background2.jpg")))
        # self.setPalette(palette)

        # 按钮格式
        stlsheet = '''QPushButton
                             {text-align : center;
                             background-color : white;
                             font-weight: bold;
                             font-family: 幼圆;
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
                             font : 14px;}'''


        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QRect(130, 80, 151, 61))
        self.pushButton.setStyleSheet(stlsheet)
        self.pushButton.setObjectName("pushButton")

        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QRect(130, 180, 151, 61))
        self.pushButton_2.setStyleSheet(stlsheet)
        self.pushButton_2.setObjectName("pushButton_2")

        self.pushButton_3 = QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QRect(130, 280, 151, 61))
        self.pushButton_3.setStyleSheet(stlsheet)
        self.pushButton_3.setObjectName("pushButton_3")

        self.pushButton_4 = QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QRect(130, 380, 151, 61))
        self.pushButton_4.setStyleSheet(stlsheet)
        self.pushButton_4.setObjectName("pushButton_4")

        # 按钮透明度设置
        op = QGraphicsOpacityEffect()
        op.setOpacity(0.8)
        self.pushButton.setGraphicsEffect(op)
        op = QGraphicsOpacityEffect()
        op.setOpacity(0.8)
        self.pushButton_2.setGraphicsEffect(op)
        op = QGraphicsOpacityEffect()
        op.setOpacity(0.8)
        self.pushButton_3.setGraphicsEffect(op)
        op = QGraphicsOpacityEffect()
        op.setOpacity(0.8)
        self.pushButton_4.setGraphicsEffect(op)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawRect(self.rect())
        pixmap = QPixmap("images/background2.jpg")  # 换成自己的图片的相对路径
        painter.drawPixmap(self.rect(), pixmap)

    def retranslateUi(self, MainWindow):
        _translate = QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "正常邮件"))
        self.pushButton_2.setText(_translate("MainWindow", "垃圾邮件"))
        self.pushButton_3.setText(_translate("MainWindow", "白名单"))
        self.pushButton_4.setText(_translate("MainWindow", "黑名单"))

    # 鼠标拖动
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))  # 更改鼠标图标

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_flag:
            self.move(QMouseEvent.globalPos() - self.m_Position)  # 更改窗口位置
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag = False
        self.setCursor(QCursor(Qt.ArrowCursor))

# if __name__ == "__main__":
#     app = QtWidgets.QApplication(sys.argv)
#     myshow = Ui_MainWindow()
#     myshow.show()
#     sys.exit(app.exec_())