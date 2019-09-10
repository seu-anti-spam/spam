# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Setting.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import imap

class SettingUi(QDialog):
    def __init__(self, user):
        super(SettingUi, self).__init__()
        self.str = imap.save_path
        self.user = user
        self.setObjectName("Dialog")
        self.resize(400, 550)
        self.setWindowOpacity(0.9)
        self.setWindowFlags(Qt.FramelessWindowHint)  # 无边框

        self.setStyleSheet('''
                                QDialog{
                                        background:#E8E8E8;
                                        font-family: "Microsoft Yahei";}         
                                ''')

        # 关闭按钮
        self.pushButton_close = QPushButton(self)
        self.pushButton_close.setGeometry(QRect(370, 10, 15, 15))
        self.pushButton_close.setToolTip('退出')
        self.pushButton_close.setObjectName("pushButton_close")
        self.pushButton_close.setStyleSheet('''
                                         QPushButton{
                                            border-image:url(images/grayclose.png);}
                                         QPushButton:hover{
                                            border-image:url(images/redclose.png);}
                                                    ''')

        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(30, 80, 72, 15))
        self.label.setObjectName("label")
        self.label.setFont(QFont("Microsoft Yahei"))

        self.dlEdit = QtWidgets.QLineEdit(self)
        self.dlEdit.setGeometry(QtCore.QRect(50, 110, 231, 31))
        self.dlEdit.setObjectName("dlEdit")
        self.dlEdit.setStyleSheet('''
                            QLineEdit{
                                color:#4F4F4F;
                                font-family:"Segoe UI";
                                background:transparent;
                                border:1px solid #A9A9A9;
                                border-radius: 4px;}
                                ''')

        self.notEdit = QtWidgets.QLineEdit(self)
        self.notEdit.setGeometry(QtCore.QRect(140, 250, 221, 31))
        self.notEdit.setObjectName("notEdit")
        self.notEdit.setStyleSheet('''
                            QLineEdit{
                                color:#4F4F4F;
                                font-family:"Segoe UI";
                                background:transparent;
                                border:1px solid #A9A9A9;
                                border-radius: 4px;}
                                ''')

        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setGeometry(QtCore.QRect(30, 200, 101, 16))
        self.label_2.setObjectName("label_2")
        self.label_2.setFont(QFont("Microsoft Yahei"))

        self.label_3 = QtWidgets.QLabel(self)
        self.label_3.setGeometry(QtCore.QRect(60, 260, 72, 15))
        self.label_3.setObjectName("label_3")
        self.label_3.setFont(QFont("Microsoft Yahei"))

        self.label_4 = QtWidgets.QLabel(self)
        self.label_4.setGeometry(QtCore.QRect(60, 310, 72, 15))
        self.label_4.setObjectName("label_4")
        self.label_4.setFont(QFont("Microsoft Yahei"))

        self.lgEdit = QtWidgets.QLineEdit(self)
        self.lgEdit.setGeometry(QtCore.QRect(140, 300, 221, 31))
        self.lgEdit.setObjectName("lgEdit")
        self.lgEdit.setStyleSheet('''
                            QLineEdit{
                                color:#4F4F4F;
                                font-family:"Segoe UI";
                                background:transparent;
                                border:1px solid #A9A9A9;
                                border-radius: 4px;}
                                ''')

        btStlSheet = '''QPushButton
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
                                 font : 14px;}'''
        self.scanBtn = QtWidgets.QPushButton(self)
        self.scanBtn.setGeometry(QtCore.QRect(290, 110, 71, 31))
        self.scanBtn.setObjectName("scanBtn")
        self.scanBtn.setStyleSheet(btStlSheet)

        self.sureBtn = QtWidgets.QPushButton(self)
        self.sureBtn.setGeometry(QtCore.QRect(210, 490, 71, 31))
        self.sureBtn.setObjectName("sureBtn")
        self.sureBtn.setStyleSheet(btStlSheet)

        self.cancelBtn = QtWidgets.QPushButton(self)
        self.cancelBtn.setGeometry(QtCore.QRect(290, 490, 71, 31))
        self.cancelBtn.setObjectName("cancelBtn")
        self.cancelBtn.setStyleSheet(btStlSheet)

        self.changelabel = QLabel(self)
        self.changelabel.setGeometry(30, 400, 100, 15)
        self.changelabel.setText("换个皮肤吧：")
        self.changelabel.setFont(QFont("Microsoft Yahei"))

        self.combox = QComboBox(self)
        self.combox.resize(200, 31)
        self.combox.move(140, 390)
        self.combox.addItem('星空')
        self.combox.addItem('清新')
        # self.combox.setStyleSheet(btStlSheet)


        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)

        self.initUI()

    def initUI(self):
        self.dlEdit.setText(self.str)
        self.scanBtn.clicked.connect(self.onBtnScan)
        self.sureBtn.clicked.connect(self.onBtnSure)
        self.cancelBtn.clicked.connect(self.onBtnCancel)
        self.pushButton_close.clicked.connect(self.onBtnCancel)

    def onBtnScan(self):
        download_path = QtWidgets.QFileDialog.getExistingDirectory(self,
                                                                   "浏览",
                                                                   self.str)
        self.dlEdit.setText(download_path)

    def onBtnSure(self):
        self.str = self.dlEdit.text()
        imap.save_path = self.str
        self.close()

    def onBtnCancel(self):
        self.close()


    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "设置"))
        self.label.setText(_translate("Dialog", "下载路径："))
        self.label_2.setText(_translate("Dialog", "自动回复内容："))
        self.label_3.setText(_translate("Dialog", "正常邮件："))
        self.label_4.setText(_translate("Dialog", "垃圾邮件："))
        self.scanBtn.setText(_translate("Dialog", "浏览"))
        self.sureBtn.setText(_translate("Dialog", "更改"))
        self.cancelBtn.setText(_translate("Dialog", "取消"))

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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    str = 'D:\workplace'
    dialag = SettingUi(str)
    dialag.show()
    sys.exit(app.exec_())