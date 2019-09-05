from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtCore import *
import AddAssociateList
import ComfireMail
import imap
import sys
import WarningBox
import time
from PyQt5.QtGui import *
from socket import *
import os


s = socket(AF_INET, SOCK_STREAM)



# 获取绝对路径
url_father = os.path.dirname(os.path.abspath(__file__))

# 因为styleSheet里正斜杠才管用，我要把反斜杠转化为正斜杠
url = ""
for i in url_father:
    if (i == "\\"):
        url = url + "/"
    else:
        url = url + i

class AssoThread(QThread):
    def __init__(self):
        super().__init__()
        self.result = list()

    def set_im(self,im):
        self.im = im
        self.im.init()

    def run(self):
        while True:
            self.result = self.im.get_new_mail()
            if self.result is not None:
                for each in self.result:
                    print(each['垃圾'])
                    if each['垃圾'] == 2:
                        self.update_email.emit(each)
                        imap.received_mails['正常邮件'].append(each)
                    elif each['垃圾'] == 1:
                        self.update_email.emit(each)
                        imap.received_mails['垃圾邮件'].append(each)
                    else:
                        imap.received_mails['正常邮件'].append(each)
                    time.sleep(1)
            time.sleep(2)

class AssociateListUi(QDialog):
    def __init__(self, if_login, count, AThread):
        super(AssociateListUi, self).__init__()
        self.AThreads = [AThread]
        self.AThreads_2 = dict()
        self.index = 0
        self.index_2 = 0
        self.if_login = if_login
        self.count = count
        self.initUI()


    def initUI(self):
        self.setWindowTitle("关联邮箱")
        self.setWindowIcon(QIcon('images/LOGO.png'))
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
        self.icon = QLabel(self)
        self.icon.setGeometry(10, 5, 30, 30)
        # pal = self.palette()
        # pix = QPixmap("images/nlogo.png")
        # pix.scaled(QSize(20, 20), Qt.KeepAspectRatio)
        # self.icon.setAlignment(Qt.AlignCenter)
        # self.icon.setPixmap(pix)
        # pal.setBrush(self.icon.backgroundRole(),
        #              QBrush(pix.scaled(self.icon.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)))
        # self.icon.setPalette(pal)

        # 合成新的路径并使用
        self.icon.setStyleSheet("border-image:url(" + url + "/images/nlogo.png)")

        # 窗口名称
        self.title = QLabel(self)
        self.title.setGeometry(40, 12, 80, 20)
        self.title.setText("关联邮箱")
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
        self.tableWidget.setColumnCount(3)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setVisible(False)
        self.tableWidget.setShowGrid(False)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setColumnWidth(0, 170)
        self.tableWidget.setColumnWidth(1, 80)
        self.tableWidget.setColumnWidth(2, 80)
        self.row_count = 0
        self.tableWidget.setStyleSheet('''
                    QTableWidget{
                                text-align: center;
                                background: transparent;
                                font-family: SimHei;}            
        ''')
        for each in imap.associate_list[1:]:
            self.AThreads_2.update({each : self.AThreads[self.index]})
            if self.count[0] == 0:
                self.if_login.update({each: 1})
            self.index += 1
            self.addLine(each)
        self.count[0] = 1
    def onBtnAdd(self):
        dialog = AddAssociateList.AddAssociateListUi(self.if_login)
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

            # 登录按钮
            self.sign = QPushButton()
            if self.if_login[name] == 1:
                self.sign.setText("登录")
            else:
                self.sign.setText("登出")
            self.sign.clicked.connect(lambda: self.onBtnSign(name))
            self.sign.setStyleSheet('''QPushButton
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

            # 移除按钮
            self.reMovBtn = QPushButton("删除")
            if self.if_login[name]==1:
                self.reMovBtn.setEnabled(True)
            else:
                self.reMovBtn.setEnabled(False)
            row = self.row_count
            self.reMovBtn.clicked.connect(lambda: self.onBtnReMov(name))
            self.reMovBtn.setStyleSheet('''QPushButton
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

            self.tableWidget.setCellWidget(self.row_count, 0, member)
            self.tableWidget.setCellWidget(self.row_count, 1, self.sign)
            self.tableWidget.setCellWidget(self.row_count, 2, self.reMovBtn)


    def onBtnSign(self, name):
        if self.sign.text() == "登录":
            self.dialog = ComfireMail.ComfireMailUi()
            self.dialog.addBtn.clicked.connect(lambda: self.login(name))
            self.dialog.exec()

        elif self.sign.text() == "登出":
            self.reMovBtn.setEnabled(True)
            self.sign.setText("登录")
            self.AThreads_2[name].terminate()
            self.if_login[name] = 1

    def login(self, name):
        associate_im = imap.Imapmail()
        associate_im.user = name
        associate_im.password = self.dialog.passwordEdit.text()
        associate_im.server_address = 'imap.' + associate_im.user.split('@')[-1]  # 邮箱地址
        if associate_im.user.split('@')[-1] in ['163.com', 'qq.com', '126.com']:
            associate_im.client()
            e = associate_im.login()
            if e == 0:
                reply = WarningBox.WarningBox('账号或密码输入错误')
                reply.exec()
            else:
                self.if_login[name] = 2
                self.AThreads[self.index_2].set_im(associate_im)
                self.AThreads[self.index_2].start()
                self.AThreads_2.update({name : self.AThreads[self.index_2]})
                self.dialog.close()
                # self.sign.setEnabled(False)
                self.sign.setText("登出")
                self.reMovBtn.setEnabled(False)

        else:
            reply = WarningBox.WarningBox('邮箱格式不正确')
            reply.exec()

    def onBtnReMov(self, name):
        button = self.sender()
        if button:
            r = self.tableWidget.indexAt(button.pos()).row()
            row = int(r)
            self.tableWidget.removeRow(row)
            self.row_count = self.row_count - 1
            imap.associate_list.remove(name)

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
    dialag = AssociateListUi()
    dialag.show()
    sys.exit(app.exec_())

