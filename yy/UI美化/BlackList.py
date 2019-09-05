import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore
import AddBlackList
import imap
import os

# 获取绝对路径
url_father = os.path.dirname(os.path.abspath(__file__))

# 因为styleSheet里正斜杠才管用，我要把反斜杠转化为正斜杠
url = ""
for i in url_father:
    if (i == "\\"):
        url = url + "/"
    else:
        url = url + i

class BlackListUi(QDialog):

    def __init__(self):
        super(BlackListUi, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("黑名单")
        # self.setWindowIcon(QIcon(url + 'images/LOGO.png'))
        self.resize(290, 530)
        self.setFixedSize(self.width(), self.height())
        # layout = QVBoxLayout()
        self.setWindowOpacity(0.9)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet('''
                QDialog{
                        background:#DCDCDC;
                        font-family: "Microsoft Yahei";}         
        ''')

        # 窗口图标
        self.icon = QPushButton(self)
        self.icon.setGeometry(10, 5, 30, 30)
        # pix = QPixmap("images/nlogo.png")
        # pix.scaled(QSize(20, 20), Qt.KeepAspectRatio)
        # self.icon.setAlignment(Qt.AlignCenter)
        # self.icon.setPixmap(pix)

        # 合成新的路径并使用
        print(url)
        self.icon.setStyleSheet("border-image:url(" + url + "/images/nlogo.png)")
        # self.icon.setStyleSheet('''
        #
        #                             border-image: url(images/nlogo.png);}''')

        # 窗口名称
        self.title = QLabel(self)
        self.title.setGeometry(40, 12, 80, 20)
        self.title.setText("黑名单")
        self.title.setStyleSheet('''
                        QLabel{
                                font-family: "Microsoft Yahei";}
                                ''')

        # 添加关闭按钮
        self.pushButton_close = QPushButton(self)
        self.pushButton_close.setGeometry(QRect(260, 15, 15, 15))
        self.pushButton_close.setToolTip('退出')
        self.pushButton_close.setObjectName("pushButton_close")
        self.pushButton_close.setStyleSheet('''
                                                         QPushButton{
                                                            border-image:url(images/grayclose.png);}
                                                        QPushButton:hover{
                                                            border-image:url(images/redclose.png);}
                                                                    ''')
        self.pushButton_close.clicked.connect(self.close)

        self.addBtn = QPushButton("添加", self)
        self.addBtn.setGeometry(10, 490, 270, 30)
        self.addBtn.clicked.connect(self.onBtnAdd)
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

        self.tableWidget = QTableWidget(self)
        self.tableWidget.setGeometry(10, 40, 270, 440)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setVisible(False)
        self.tableWidget.setShowGrid(False)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setColumnWidth(0, 170)
        self.tableWidget.setColumnWidth(1, 80)
        self.row_count = 0


        self.tableWidget.setStyleSheet('''
                    QTableWidget{
                                text-align: center;
                                background: transparent;
                                font-family: SimHei;}            
        ''')
        #  建立连接

        #  断开连接
        for each in imap.black_list:
            self.addLine(each)

        # layout.addWidget(self.tableWidget)
        # layout.addWidget(self.addBtn)
        # self.setLayout(layout)

    # # 添加背景
    # def paintEvent(self, event):
    #     painter = QPainter(self)
    #     painter.drawRect(self.rect())
    #     pixmap = QPixmap("timg1.jpg")  # 换成自己的图片的相对路径
    #     painter.drawPixmap(self.rect(), pixmap)

    def onBtnAdd(self):
        dialog = AddBlackList.AddBlackListUi()
        dialog.addBtn.clicked.connect(lambda: self.addLine(dialog.memberEdit.text()))
        dialog.exec()

    #### 动态添加一行信息
    def addLine(self, name):
        if '@' in name:
            # 添加一空白行
            self.row_count = self.tableWidget.rowCount()
            self.tableWidget.insertRow(self.row_count)

            # 联系人
            member = QLineEdit()
            member.setFocusPolicy(QtCore.Qt.NoFocus)
            member.setText(name)
            member.setStyleSheet('''
                            QLineEdit{
                                color:#4F4F4F;
                                font-family:"Segoe UI";
                                background: #DCDCDC;
                                border:none}
                                ''')

            # 移除按钮
            reMovBtn = QPushButton("delete")
            row = self.row_count
            reMovBtn.clicked.connect(lambda: self.onBtnReMov(name))
            reMovBtn.setStyleSheet('''QPushButton
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

            # self.tableWidget.setItem(self.row_count, 0, QTableWidgetItem(name))
            self.tableWidget.setCellWidget(self.row_count, 0, member)
            self.tableWidget.setCellWidget(self.row_count, 1, reMovBtn)


    def onBtnReMov(self, name):
        button = self.sender()
        if button:
            r = self.tableWidget.indexAt(button.pos()).row()
            row = int(r)
            self.tableWidget.removeRow(row)
            self.row_count = self.row_count - 1
            imap.black_list.remove(name)

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
    dialag = BlackListUi()
    dialag.show()
    sys.exit(app.exec_())