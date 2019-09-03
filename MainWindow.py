# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(731, 518)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.normailBtn = QtWidgets.QToolButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.normailBtn.sizePolicy().hasHeightForWidth())
        self.normailBtn.setSizePolicy(sizePolicy)
        self.normailBtn.setObjectName("normailBtn")
        self.gridLayout_3.addWidget(self.normailBtn, 0, 0, 1, 1)
        self.whiteBtn = QtWidgets.QToolButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.whiteBtn.sizePolicy().hasHeightForWidth())
        self.whiteBtn.setSizePolicy(sizePolicy)
        self.whiteBtn.setObjectName("whiteBtn")
        self.gridLayout_3.addWidget(self.whiteBtn, 0, 1, 1, 1)
        self.conBtn = QtWidgets.QToolButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.conBtn.sizePolicy().hasHeightForWidth())
        self.conBtn.setSizePolicy(sizePolicy)
        self.conBtn.setObjectName("conBtn")
        self.gridLayout_3.addWidget(self.conBtn, 0, 2, 1, 1)
        self.lgmailBtn = QtWidgets.QToolButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lgmailBtn.sizePolicy().hasHeightForWidth())
        self.lgmailBtn.setSizePolicy(sizePolicy)
        self.lgmailBtn.setObjectName("lgmailBtn")
        self.gridLayout_3.addWidget(self.lgmailBtn, 1, 0, 1, 1)
        self.blackBtn = QtWidgets.QToolButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.blackBtn.sizePolicy().hasHeightForWidth())
        self.blackBtn.setSizePolicy(sizePolicy)
        self.blackBtn.setObjectName("blackBtn")
        self.gridLayout_3.addWidget(self.blackBtn, 1, 1, 1, 1)
        self.c = QtWidgets.QToolButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.c.sizePolicy().hasHeightForWidth())
        self.c.setSizePolicy(sizePolicy)
        self.c.setObjectName("c")
        self.gridLayout_3.addWidget(self.c, 1, 2, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout_3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.normailBtn.setText(_translate("MainWindow", "正"))
        self.whiteBtn.setText(_translate("MainWindow", "白"))
        self.conBtn.setText(_translate("MainWindow", "联"))
        self.lgmailBtn.setText(_translate("MainWindow", "垃"))
        self.blackBtn.setText(_translate("MainWindow", "黑"))
        self.c.setText(_translate("MainWindow", "心"))
