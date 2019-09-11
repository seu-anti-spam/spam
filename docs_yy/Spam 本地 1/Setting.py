# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Setting.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
import imap
import pickle

class SettingUi(QDialog):
    def __init__(self, user):
        super(SettingUi, self).__init__()
        self.str = imap.save_paths[user]
        self.user = user
        self.setObjectName("Dialog")
        self.resize(400, 555)
        self.setWindowOpacity(0.9)
        self
        self.setStyleSheet('''
                                QDialog{
                                        background:#E8E8E8;
                                        font-family: "Microsoft Yahei";}         
                                ''')
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(30, 50, 72, 15))
        self.label.setObjectName("label")
        self.label.setFont(QFont("Microsoft Yahei"))

        self.dlEdit = QtWidgets.QLineEdit(self)
        self.dlEdit.setGeometry(QtCore.QRect(50, 80, 231, 31))
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
        self.notEdit.setGeometry(QtCore.QRect(140, 220, 221, 31))
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
        self.label_2.setGeometry(QtCore.QRect(30, 170, 101, 16))
        self.label_2.setObjectName("label_2")
        self.label_2.setFont(QFont("Microsoft Yahei"))

        self.label_3 = QtWidgets.QLabel(self)
        self.label_3.setGeometry(QtCore.QRect(60, 230, 72, 15))
        self.label_3.setObjectName("label_3")
        self.label_3.setFont(QFont("Microsoft Yahei"))

        self.label_4 = QtWidgets.QLabel(self)
        self.label_4.setGeometry(QtCore.QRect(60, 280, 72, 15))
        self.label_4.setObjectName("label_4")
        self.label_4.setFont(QFont("Microsoft Yahei"))

        self.lgEdit = QtWidgets.QLineEdit(self)
        self.lgEdit.setGeometry(QtCore.QRect(140, 270, 221, 31))
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
        self.scanBtn.setGeometry(QtCore.QRect(290, 80, 71, 31))
        self.scanBtn.setObjectName("scanBtn")
        self.scanBtn.setStyleSheet(btStlSheet)

        self.sureBtn = QtWidgets.QPushButton(self)
        self.sureBtn.setGeometry(QtCore.QRect(210, 460, 71, 31))
        self.sureBtn.setObjectName("sureBtn")
        self.sureBtn.setStyleSheet(btStlSheet)

        self.cancelBtn = QtWidgets.QPushButton(self)
        self.cancelBtn.setGeometry(QtCore.QRect(290, 460, 71, 31))
        self.cancelBtn.setObjectName("cancelBtn")
        self.cancelBtn.setStyleSheet(btStlSheet)

        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)

        self.initUI()

    def initUI(self):
        self.dlEdit.setText(self.str)
        self.scanBtn.clicked.connect(self.onBtnScan)
        self.sureBtn.clicked.connect(self.onBtnSure)
        self.cancelBtn.clicked.connect(self.onBtnCancel)

    def onBtnScan(self):
        download_path = QtWidgets.QFileDialog.getExistingDirectory(self,
                                                                   "浏览",
                                                                   self.str)
        self.dlEdit.setText(download_path)

    def onBtnSure(self):
        self.str = self.dlEdit.text()
        imap.save_paths[self.user] = self.str
        pickle_file = open('save_paths.pkl', 'wb')
        pickle.dump(imap.save_paths, pickle_file)
        pickle_file.close()
        self.close()

    def onBtnCancel(self):
        self.close()


    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "下载路径："))
        self.label_2.setText(_translate("Dialog", "自动回复内容："))
        self.label_3.setText(_translate("Dialog", "正常邮件："))
        self.label_4.setText(_translate("Dialog", "垃圾邮件："))
        self.scanBtn.setText(_translate("Dialog", "浏览"))
        self.sureBtn.setText(_translate("Dialog", "更改"))
        self.cancelBtn.setText(_translate("Dialog", "取消"))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    str = 'D:\workplace'
    dialag = SettingUi(str)
    dialag.show()
    sys.exit(app.exec_())