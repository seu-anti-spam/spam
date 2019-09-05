# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *


class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(500, 390)
        # MainWindow.resize(731, 518)
        # MainWindow.resize(750, 550)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setWindowFlags(Qt.FramelessWindowHint)
        MainWindow.setWindowOpacity(0.9)
        # MainWindow.setStyleSheet('''
        #                 QWidget{
        #                         border-radius:10px;
        #                         }
        #         ''')


        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(5, 35, 490, 330))
        self.widget.setObjectName("widget")

        self.gridLayout_3 = QtWidgets.QGridLayout(self.widget)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")

        # 调整大小
        # self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        # self.horizontalLayout.setObjectName("horizontalLayout")
        # self.gridLayout_3 = QtWidgets.QGridLayout()
        # self.gridLayout_3.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        # self.gridLayout_3.setObjectName("gridLayout_3")

        self.normailBtn = QtWidgets.QToolButton(self.widget)
        # self.normailBtn = QtWidgets.QToolButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.normailBtn.sizePolicy().hasHeightForWidth())
        self.normailBtn.setSizePolicy(sizePolicy)
        self.normailBtn.setObjectName("normailBtn")
        self.gridLayout_3.addWidget(self.normailBtn, 0, 0, 1, 1)

        # self.whiteBtn = QtWidgets.QToolButton(self.centralwidget)
        self.whiteBtn = QtWidgets.QToolButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.whiteBtn.sizePolicy().hasHeightForWidth())
        self.whiteBtn.setSizePolicy(sizePolicy)
        self.whiteBtn.setObjectName("whiteBtn")
        self.gridLayout_3.addWidget(self.whiteBtn, 0, 1, 1, 1)

        # self.conBtn = QtWidgets.QToolButton(self.centralwidget)
        self.conBtn = QtWidgets.QToolButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.conBtn.sizePolicy().hasHeightForWidth())
        self.conBtn.setSizePolicy(sizePolicy)
        self.conBtn.setObjectName("conBtn")
        self.gridLayout_3.addWidget(self.conBtn, 0, 2, 1, 1)

        # self.lgmailBtn = QtWidgets.QToolButton(self.centralwidget)
        self.lgmailBtn = QtWidgets.QToolButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lgmailBtn.sizePolicy().hasHeightForWidth())
        self.lgmailBtn.setSizePolicy(sizePolicy)
        self.lgmailBtn.setObjectName("lgmailBtn")
        self.gridLayout_3.addWidget(self.lgmailBtn, 1, 0, 1, 1)

        # self.blackBtn = QtWidgets.QToolButton(self.centralwidget)
        self.blackBtn = QtWidgets.QToolButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.blackBtn.sizePolicy().hasHeightForWidth())
        self.blackBtn.setSizePolicy(sizePolicy)
        self.blackBtn.setObjectName("blackBtn")
        self.gridLayout_3.addWidget(self.blackBtn, 1, 1, 1, 1)

        # self.c = QtWidgets.QToolButton(self.centralwidget)
        self.c = QtWidgets.QToolButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.c.sizePolicy().hasHeightForWidth())
        self.c.setSizePolicy(sizePolicy)
        self.c.setObjectName("c")
        self.gridLayout_3.addWidget(self.c, 1, 2, 1, 1)

        # self.horizontalLayout.addLayout(self.gridLayout_3)
        MainWindow.setCentralWidget(self.centralwidget)
        # self.statusbar = QtWidgets.QStatusBar(MainWindow)
        # self.statusbar.setObjectName("statusbar")
        # MainWindow.setStatusBar(self.statusbar)

        # 皮肤风格
        # self.UIStyle1(MainWindow)
        self.UIStyle1(MainWindow)

        # self.retranslateUi(MainWindow)
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

    # 界面背景
    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.drawRect(self.rect())
        # pixmap = QtGui.QPixmap("images/gray/3.jpg")  # 换成自己的图片的相对路径
        pixmap = QtGui.QPixmap("images/blue/background2.jpg")
        painter.drawPixmap(self.rect(), pixmap)

    # 鼠标拖动
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QtGui.QCursor(Qt.OpenHandCursor))  # 更改鼠标图标

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_flag:
            self.move(QMouseEvent.globalPos() - self.m_Position)  # 更改窗口位置
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag = False
        self.setCursor(QtGui.QCursor(Qt.ArrowCursor))

    def UIStyle1(self, MainWindow):
        # 美化
        self.normailBtn.setIcon(QtGui.QIcon("images/gray/white1.png"))
        self.normailBtn.setIconSize(QSize(80, 80))
        op = QtWidgets.QGraphicsOpacityEffect()  # 控件透明度
        op.setOpacity(0.8)
        self.normailBtn.setGraphicsEffect(op)
        self.normailBtn.setStyleSheet('''
                               QToolButton{
                                    background-color: transparent;
                                    border-radius: 10px;
                                    border: 2px outset #666666;
                                    padding:1px;}
                                QToolButton:hover{
                                    background-color: transparent;
                                    border-radius: 10px;
                                    border: 2px outset #888888;
                                    padding:1px;}
                    ''')

        # 美化
        self.whiteBtn.setIcon(QtGui.QIcon("images/gray/gray3.png"))
        self.whiteBtn.setIconSize(QSize(80, 80))
        op = QtWidgets.QGraphicsOpacityEffect()
        op.setOpacity(0.8)
        self.whiteBtn.setGraphicsEffect(op)
        self.whiteBtn.setStyleSheet('''
                                       QToolButton{
                                            background-color: transparent;
                                            border-radius: 10px;
                                            border: 2px outset #666666;
                                            padding:1px;}
                                        QToolButton:hover{
                                            background-color: transparent;
                                            border-radius: 10px;
                                            border: 2px outset #888888;
                                            padding:1px;}
                            ''')

        # 美化
        self.conBtn.setIcon(QtGui.QIcon("images/gray/gray5.png"))
        self.conBtn.setIconSize(QSize(80, 80))
        op = QtWidgets.QGraphicsOpacityEffect()
        op.setOpacity(0.8)
        self.conBtn.setGraphicsEffect(op)
        self.conBtn.setStyleSheet('''
                                               QToolButton{
                                                    background-color: transparent;
                                                    border-radius: 10px;
                                                    border: 2px outset #666666;
                                                    padding:1px;}
                                                QToolButton:hover{
                                                    background-color: transparent;
                                                    border-radius: 10px;
                                                    border: 2px outset #888888;
                                                    padding:1px;}
                                    ''')

        # 美化
        self.lgmailBtn.setIcon(QtGui.QIcon("images/gray/gray2.png"))
        self.lgmailBtn.setIconSize(QSize(80, 80))
        op = QtWidgets.QGraphicsOpacityEffect()
        op.setOpacity(0.8)
        self.lgmailBtn.setGraphicsEffect(op)
        self.lgmailBtn.setStyleSheet('''
                                               QToolButton{
                                                    background-color: transparent;
                                                    border-radius: 10px;
                                                    border: 2px outset #666666;
                                                    padding:1px;}
                                                QToolButton:hover{
                                                    background-color: transparent;
                                                    border-radius: 10px;
                                                    border: 2px outset #888888;
                                                    padding:1px;}
                                    ''')

        # 美化
        self.blackBtn.setIcon(QtGui.QIcon("images/gray/gray4.png"))
        self.blackBtn.setIconSize(QSize(80, 80))
        op = QtWidgets.QGraphicsOpacityEffect()
        op.setOpacity(0.8)
        self.blackBtn.setGraphicsEffect(op)
        self.blackBtn.setStyleSheet('''
                                               QToolButton{
                                                    background-color: transparent;
                                                    border-radius: 10px;
                                                    border: 2px outset #666666;
                                                    padding:1px;}
                                                QToolButton:hover{
                                                    background-color: transparent;
                                                    border-radius: 10px;
                                                    border: 2px outset #888888;
                                                    padding:1px;}
                                    ''')

        # 美化
        self.c.setIcon(QtGui.QIcon("images/gray/gray6.png"))
        self.c.setIconSize(QSize(80, 80))
        op = QtWidgets.QGraphicsOpacityEffect()
        op.setOpacity(0.8)
        self.c.setGraphicsEffect(op)
        self.c.setStyleSheet('''
                                               QToolButton{
                                                    background-color: transparent;
                                                    border-radius: 10px;
                                                    border: 2px outset #666666;
                                                    padding:1px;}
                                                QToolButton:hover{
                                                    background-color: transparent;
                                                    border-radius: 10px;
                                                    border: 2px outset #888888;
                                                    padding:1px;}
                                    ''')
