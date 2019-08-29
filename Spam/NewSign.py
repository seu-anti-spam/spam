import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import time
import MainWindow_UI
import imap
import Normail
import Lgmail
import WhiteList
import BlackList
import pickle
import Setting
import filter2

from socket import *
from PyQt5.QtGui import *

received_mails = {'垃圾邮件': [], '正常邮件': []}  # 存储往期邮件
flag = 0
################################################
#######创建主窗口
################################################


class BackendThread(QThread):

    def __init__(self, im):
        super().__init__()
        self.im = im
        self.result = list()
        self.im.init()
    update_email = pyqtSignal(dict)

    def run(self):
        global received_mails
        global flag

        #  连接服务器
        address = '42.159.155.29'
        port = 8000
        buffsize = 1024
        s = socket(AF_INET, SOCK_STREAM)
        try:
            print(s.connect((address, port)))
        except TimeoutError as e:
            print(e)
            normDict, spamDict = filter2.Get_Dict('normal.txt', 'spam.txt')
            pickle_file = open('health_dic.pkl', 'rb')
            health_dic = pickle.load(pickle_file)
            pickle_file.close()
            pickle_file = open('health_dic.pkl', 'rb')
            spam_dic = pickle.load(pickle_file)
        finally:
            received_mails = self.im.get_all_mails(normDict, spamDict, health_dic, spam_dic, 11850459, 10244975)
            # 断开连接
            flag = 1
            while True:
                self.result = self.im.get_new_mail(normDict, spamDict, health_dic, spam_dic, 11850459, 10244975)
                if self.result is not None:
                    for each in self.result:
                        if each['垃圾'] == 1:
                            self.update_email.emit(each)
                            received_mails['垃圾邮件'].append(each)
                        else:
                            received_mails['正常邮件'].append(each)
                    time.sleep(1)
                time.sleep(2)

class MainWindow(QMainWindow, MainWindow_UI.Ui_MainWindow):
    windowList = []

    def __init__(self, im, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowTitle('主界面')
        self.im = im
        self.backend = None
        self.printAction1 = None
        self.printAction2 = None
        self.printMenu = None

        pickle_file_2 = open('extra_list.pkl', 'rb')
        Lgmail.extra_list = pickle.load(pickle_file_2)

        # 添加设置按钮
        self.setting = QPushButton(self)
        # self.setting.setText("设置")
        self.setting.setGeometry(360, 480, 25, 25)
        self.setting.clicked.connect(lambda: self.onBtn_Setting(self.im.user))
        self.setting.setStyleSheet('''
                                    QPushButton{
                                        border-image:url(images/set1.png);}
                                    QPushButton:hover{
                                        border-image:url(images/set.png);}
                                    ''')

        # 添加最小化按钮
        self.pushButton_min = QPushButton(self)
        self.pushButton_min.setGeometry(315, 20, 15, 15)
        self.pushButton_min.setToolTip('最小化')
        self.pushButton_min.setObjectName("pushButton_min")
        self.pushButton_min.setStyleSheet('''
                                                        QPushButton{
                                                            border-image:url(images/graymin.png);}
                                                        QPushButton:hover{
                                                            border-image:url(images/redmin.png);}
                                                        ''')

        # 添加注销按钮
        self.pushButton_logout = QPushButton(self)
        self.pushButton_logout.setGeometry(QRect(340, 18, 20, 20))
        self.pushButton_logout.setToolTip('注销')
        self.pushButton_logout.setObjectName("pushButton_logout")
        self.pushButton_logout.setStyleSheet('''
                                                 QPushButton{
                                                    border-image:url(images/graycircle.png);}
                                                QPushButton:hover{
                                                    border-image:url(images/redcircle.png);}
                                                            ''')

        # 添加关闭按钮
        self.pushButton_close = QPushButton(self)
        self.pushButton_close.setGeometry(QRect(370, 20, 15, 15))
        self.pushButton_close.setToolTip('退出')
        self.pushButton_close.setObjectName("pushButton_close")
        self.pushButton_close.setStyleSheet('''
                                                 QPushButton{
                                                    border-image:url(images/grayclose.png);}
                                                QPushButton:hover{
                                                    border-image:url(images/redclose.png);}
                                                            ''')

        # 绑定按钮监听事件
        self.pushButton_min.clicked.connect(self.minimized)
        self.pushButton_logout.clicked.connect(self.on_printAction1_triggered)
        self.pushButton_close.clicked.connect(self.on_printAction2_triggered)

        # 创建菜单栏
        # self.createMenus()
        # 后台监控邮件
        self.initMonitor()
        self.pushButton.clicked.connect(self.onBtn_Normail)
        self.pushButton_2.clicked.connect(self.onBtn_Lgmail)
        self.pushButton_3.clicked.connect(self.onBtn_WhiteList)
        self.pushButton_4.clicked.connect(self.onBtn_BlackList)

    def minimized(self):
        self.showMinimized()

    def onBtn_Setting(self, str):
        set = Setting.SettingUi(str)
        set.exec()

    def initMonitor(self):
        self.backend = BackendThread(self.im)
        self.backend.update_email.connect(self.handleDisplay)
        self.backend.start()

    def handleDisplay(self, content):
        topic = content['主题']
        send = content['发件人']
        send_time = content['时间']
        mainContent = content['主要内容']
        ip = content['IP地址']
        message = ('您收到1封垃圾邮件\n' + '主题：' + topic + '\n' + '发件人：' + send +
                   '\n' + 'ip地址：' + ip + '\n' + '时间：' + send_time + '\n' + '主要内容：\n' +
                   mainContent[:20] + '\n是否需要删除该邮件？')
        temp = QMessageBox.warning(self, "提示", message, QMessageBox.Yes | QMessageBox.No)
        if temp == QMessageBox.Yes:
            self.im.delete_mail(content['邮件'])
        else:
            pass

    def createMenus(self):
        # # 创建动作 注销
        # self.printAction1 = QAction(self.tr("注销"), self)
        # self.printAction1.triggered.connect(self.on_printAction1_triggered)
        #
        # # 创建动作 退出
        # self.printAction2 = QAction(self.tr("退出"), self)
        # self.printAction2.triggered.connect(self.on_printAction2_triggered)

        # 创建菜单，添加动作

        # self.printMenu = self.menuBar().addMenu(self.tr("注销和退出"))
        # self.printMenu.addAction(self.printAction1)
        # self.printMenu.addAction(self.printAction2)
        self.pushButton_logout.clicked.connect(self.on_printAction1_triggered)
        self.pushButton_close.clicked.connect(self.on_printAction2_triggered)

    def onBtn_Normail(self):
        global received_mails
        if flag == 1:
            normail = Normail.NormailUi(self.im, received_mails)
            normail.exec()
        else:
            reply = QMessageBox.warning(self, '!', '往期邮件扫描未完成', QMessageBox.Yes)

    def onBtn_Lgmail(self):
        global received_mails
        if flag == 1:
            lgmail = Lgmail.LgmailUi(self.im, Lgmail.extra_list, received_mails)
            lgmail.exec()
        else:
            reply = QMessageBox.warning(self, '!', '往期邮件扫描未完成', QMessageBox.Yes)

    def onBtn_WhiteList(self):
        wdialog = WhiteList.WhiteListUi()
        wdialog.exec()

    def onBtn_BlackList(self):
        bdialog = BlackList.BlackListUi()
        bdialog.exec()

    # 动作一：注销
    def on_printAction1_triggered(self):
        global received_mails
        received_mails['正常邮件'].clear()
        received_mails['垃圾邮件'].clear()
        self.backend.terminate()
        self.close()
        dialog = logindialog(mode=1)
        if dialog.exec_() == QDialog.Accepted:
            the_window = MainWindow(self.im)
            self.windowList.append(the_window)  # 这句一定要写，不然无法重新登录
            the_window.show()

    # 动作二：退出
    def on_printAction2_triggered(self):
        self.backend.terminate()
        self.close()

    # 关闭界面触发事件
    def closeEvent(self, event):
        pass


################################################
#######对话框
################################################


class logindialog(QDialog):
    def __init__(self, mode=0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.im = imap.Imapmail()
        self.mode = mode
        self.setWindowTitle('登录界面')
        self.resize(520, 300)
        self.setFixedSize(self.width(), self.height())
        # self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowFlags(Qt.FramelessWindowHint)
        ###### 设置界面控件
        self.frame = QFrame(self)
        self.frame.resize(400, 300)
        self.frame.move(110, 0)
        # self.verticalLayout = QVBoxLayout(self.frame)
        # background - image: url('timg.jpg');
        self.setWindowOpacity(0.9)  # 设置窗口透明度 yy
        # self.setAttribute(Qt.WA_TranslucentBackground)  # 设置窗口背景透明 yy
        # self.setStyleSheet(
        #     '''
        #     QFrame{
        #         width: 200px;
        #         height: 240px;
        #         border-radius:10%;}
        #     ''')

        self.lineEdit_account = QLineEdit(self.frame)
        self.lineEdit_account.setPlaceholderText("请输入账号")
        # self.verticalLayout.addWidget(self.lineEdit_account)
        self.lineEdit_account.setGeometry(40, 80, 221, 30)

        self.lineEdit_password = QLineEdit(self.frame)
        self.lineEdit_password.setPlaceholderText("请输入密码")
        # self.verticalLayout.addWidget(self.lineEdit_password)
        self.lineEdit_password.setEchoMode(QLineEdit.Password)
        self.lineEdit_password.setGeometry(40, 120, 221, 30)
        # Times New Roman
        self.lineEdit_account.setStyleSheet('''
                    QLineEdit{
                        color:#4F4F4F;
                        font-family:"Segoe UI";
                        border:solid;
                        background:white;
                        border-radius:10px;
                        padding:2px 4px;}
                        
                        
                        ''')

        self.lineEdit_password.setStyleSheet('''
                    QLineEdit{
                        color:#4F4F4F;
                        border:solid;
                        background:white;
                        border-radius:10px;}
                        ''')

        self.checkBox_remeberpassword = QCheckBox(self.frame)
        self.checkBox_remeberpassword.setText("记住密码")
        # self.verticalLayout.addWidget(self.checkBox_remeberpassword)
        self.checkBox_remeberpassword.setGeometry(40, 165, 91, 20)

        self.checkBox_autologin = QCheckBox(self.frame)
        self.checkBox_autologin.setText("自动登录")
        # self.verticalLayout.addWidget(self.checkBox_autologin)
        self.checkBox_autologin.setGeometry(160, 165, 91, 20)
        # border: solid;border-radius:10px;
        self.checkBox_remeberpassword.setStyleSheet('''
                        QCheckBox{
                            font-family:幼圆;}
                        QCheckBox::indicator { 
                            width: 20px;
                            height: 20px;}
                        QCheckBox::indicator::checked{
                            image:url(images/checked.png);}
                        QCheckBox::indicator::unchecked{
                            image:url(images/unchecked.png);}
                        ''')

        self.checkBox_autologin.setStyleSheet('''
                        QCheckBox{
                            font-family:幼圆;}
                        QCheckBox::indicator { 
                            width: 20px;
                            height: 20px;}
                        QCheckBox::indicator::checked{
                            image:url(images/checked.png);}
                        QCheckBox::indicator::unchecked{
                            image:url(images/unchecked.png);}
                        ''')
        # yy 关闭按钮
        # QPushButton
        # {background:  # F0F8FF;
        #      border - width: 2
        # px;
        # border - radius: 8
        # px;
        # }
        # QPushButton: hover
        # {background:  # ADD8E6;}
        self.pushButton_close = QPushButton(self)
        self.pushButton_close.setGeometry(QRect(490, 25, 15, 15))
        self.pushButton_close.setToolTip('退出')
        self.pushButton_close.setObjectName("pushButton_close")
        self.pushButton_close.setStyleSheet('''
                                 QPushButton{
                                    border-image:url(images/close.png);}
                                QPushButton:hover{
                                    border-image:url(images/redclose.png);}
                                            ''')
        # yy 最小化按钮
        self.pushButton_min = QPushButton(self)
        self.pushButton_min.setGeometry(460, 25, 15, 15)
        self.pushButton_min.setToolTip('最小化')
        self.pushButton_min.setObjectName("pushButton_min")
        self.pushButton_min.setStyleSheet('''
                                                QPushButton{
                                                    border-image:url(images/graymin.png);}
                                                QPushButton:hover{
                                                    border-image:url(images/redmin.png);}
                                                ''')

        self.pushButton_enter = QPushButton(self.frame)
        self.pushButton_enter.setText("确定")
        # self.verticalLayout.addWidget(self.pushButton_enter)
        self.pushButton_enter.setGeometry(40, 200, 101, 31)

        stlsheet = '''QPushButton
                                             {text-align : center;
                                             background-color : white;
                                             font: bold;
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

        self.pushButton_enter.setStyleSheet(stlsheet)

        self.pushButton_quit = QPushButton(self.frame)
        self.pushButton_quit.setText("取消")
        # self.verticalLayout.addWidget(self.pushButton_quit)
        self.pushButton_quit.setGeometry(160, 200, 101, 31)

        self.pushButton_quit.setStyleSheet(stlsheet)

        # 绑定按钮事件
        self.pushButton_enter.clicked.connect(self.on_pushButton_enter_clicked)
        self.pushButton_quit.clicked.connect(QCoreApplication.instance().quit)
        self.pushButton_close.clicked.connect(QCoreApplication.instance().quit)
        self.pushButton_min.clicked.connect(self.minimized)

        # 初始化登录信息
        self.init_login_info()

        # 自动登录
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.goto_autologin)
        self.timer.setSingleShot(True)
        self.timer.start(1000)

    # 登录界面背景 yy

    def minimized(self):
        self.showMinimized()

    def paintEvent(self, event):  # set background_img
        painter = QPainter(self)
        painter.drawRect(self.rect())
        pixmap = QPixmap("images/background1.jpg")  # 换成自己的图片的相对路径
        painter.drawPixmap(self.rect(), pixmap)

    # 自动登录
    def goto_autologin(self):
        if self.checkBox_autologin.isChecked() == True and self.mode == 0:
            self.on_pushButton_enter_clicked()

    # 验证登录信息
    def on_pushButton_enter_clicked(self):
        # 账号判断
        self.im.client()
        self.im.user = self.lineEdit_account.text()
        self.im.password = self.lineEdit_password.text()
        self.im.server_address = 'imap.' + self.im.user.split('@')[-1]  # 邮箱地址
        if self.im.user.split('@')[-1] in ['163.com', 'qq.com', '126.com']:
            self.im.client()
            e = self.im.login()
            if e == 0:
                password_replay = QMessageBox.warning(self, "!", "账号或密码输入错误", QMessageBox.Yes)
            else:
                self.save_login_info()
                # 通过验证，关闭对话框并返回1

                self.accept()
        else:
            format_replay = QMessageBox.warning(self, "!", "邮箱格式不正确", QMessageBox.Yes)
            print('邮箱格式不正确')

    def get_imap(self):
        return self.im

    # 保存登录信息
    def save_login_info(self):
        settings = QSettings("config.ini", QSettings.IniFormat)  # 方法1：使用配置文件
        settings.setValue("account", self.lineEdit_account.text())
        settings.setValue("password", self.lineEdit_password.text())
        settings.setValue("remeberpassword", self.checkBox_remeberpassword.isChecked())
        settings.setValue("autologin", self.checkBox_autologin.isChecked())

    # 初始化登录信息
    def init_login_info(self):
        settings = QSettings("config.ini", QSettings.IniFormat)  # 方法1：使用配置文件
        the_account = settings.value("account")
        the_password = settings.value("password")
        the_remeberpassword = settings.value("remeberpassword")
        the_autologin = settings.value("autologin")
        ########
        self.lineEdit_account.setText(the_account)
        if the_remeberpassword == "true" or the_remeberpassword == True:
            self.checkBox_remeberpassword.setChecked(True)
            self.lineEdit_password.setText(the_password)

        if the_autologin == "true" or the_autologin == True:
            self.checkBox_autologin.setChecked(True)

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


################################################
#######程序入口
################################################
if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = logindialog(mode=0)
    im = dialog.get_imap()
    if dialog.exec_() == QDialog.Accepted:
        the_window = MainWindow(im)
        the_window.paintEngine()
        the_window.show()
        sys.exit(app.exec_())
