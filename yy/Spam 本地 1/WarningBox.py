from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys

class WarningBox(QWidget):

    def __init__(self, txt):
        super(WarningBox, self).__init__()
        self.txt = txt
        self.initUI()

    def initUI(self):
        self.setWindowOpacity(0.8)
        self.resize(250, 180)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet('''
                                QWidget{
                                        background:white;
                                        font-family: "Microsoft Yahei";
                                        border-radius: 15px;}
                        ''')

        self.pushButton_close = QPushButton(self)
        self.pushButton_close.setGeometry(QRect(220, 10, 15, 15))
        self.pushButton_close.setToolTip('退出')
        self.pushButton_close.setObjectName("pushButton_close")
        self.pushButton_close.setStyleSheet('''
                                         QPushButton{
                                            border-image:url(images/grayclose.png);}
                                        QPushButton:hover{
                                            border-image:url(images/redclose.png);}
                                                    ''')

        self.inforText = QLabel(self)
        self.inforText.setGeometry(0, 30, 250, 100)
        self.inforText.setText(self.txt)
        # self.inforText.setAlignment(Qt.AlignCenter)
        self.inforText.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

        self.button = QPushButton("OK", self)
        self.button.setGeometry(100, 130, 50, 30)
        self.button.setStyleSheet('''QPushButton
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
        self.button.clicked.connect(self.close)
        self.pushButton_close.clicked.connect(self.close)

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
#     app = QApplication(sys.argv)
#
#     main = WarningBox("hello")
#     main.show()
#
#     sys.exit(app.exec_())