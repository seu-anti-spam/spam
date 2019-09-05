import sys
import imap
import WarningBox

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class AddBlackListUi(QDialog):
    def __init__(self):
        super(AddBlackListUi, self).__init__()
        self.address = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle("添加")
        self.setWindowIcon(QIcon('images/LOGO.png'))
        self.resize(270, 150)
        self.setWindowOpacity(0.9)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setFixedSize(self.width(), self.height())

        self.memberEdit = QLineEdit(self)
        self.memberEdit.setGeometry(30, 50, 211, 31)

        self.addBtn = QPushButton("添加", self)
        self.addBtn.setGeometry(90, 100, 81, 31)
        self.addBtn.clicked.connect(self.onBtnAdd)
        self.memberEdit.setPlaceholderText("请输入对方邮箱")
        self.accept()

        # 添加关闭按钮
        self.pushButton_close = QPushButton(self)
        self.pushButton_close.setGeometry(QRect(240, 15, 15, 15))
        self.pushButton_close.setToolTip('退出')
        self.pushButton_close.setObjectName("pushButton_close")
        self.pushButton_close.setStyleSheet('''
                                                                 QPushButton{
                                                                    border-image:url(images/grayclose.png);}
                                                                QPushButton:hover{
                                                                    border-image:url(images/redclose.png);}
                                                                            ''')
        self.pushButton_close.clicked.connect(self.close)

        # 美化
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
            if self.address not in imap.black_list:
                imap.black_list.append(self.address)
                self.close()
            else:
                self.reply = WarningBox.WarningBox('黑名单已存在该联系人')
                self.reply.show()
        else:
            self.reply = WarningBox.WarningBox('邮箱格式不正确')
            self.reply.show()

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
    dialag = AddBlackListUi()
    dialag.show()
    sys.exit(app.exec_())
    sys.exit(app.exec_())