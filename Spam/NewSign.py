import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import time
import MainWindow_UI
import imap

from PyQt5.QtGui import *
import threading
################################################
#######创建主窗口
################################################
class BackendThread(QThread):
    def __init__(self, im):
        super().__init__()
        self.im=im
        self.result=list()
    update_email = pyqtSignal(dict)

    def run(self):
        self.im.init()
        while True:
            self.result=self.im.get_new_mail()
            if self.result is not None:
                for each in self.result:
                    if each['垃圾'] == 1:
                        self.update_email.emit(each)
                    else:
                        pass
                time.sleep(1)
            time.sleep(5)
class MainWindow(QMainWindow,MainWindow_UI.Ui_MainWindow):
    windowList = []

    def __init__(self, im,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowTitle('主界面')
       # self.showMaximized()
        self.im=im
        self.backend = None
        self.printAction1 = None
        self.printAction2 = None
        self.printMenu = None
        # 创建菜单栏
        self.createMenus()
        # 后台监控邮件
        self.initMonitor()

    def initMonitor(self):
        self.backend = BackendThread(self.im)
        self.backend.update_email.connect(self.handleDisplay)

        self.backend.start()

    def handleDisplay(self, content):
        topic = content['主题']
        send = content['发件人']
        send_time = content['时间']
        mainContent = content['主要内容']
        message=('您收到1封垃圾邮件\n'+'主题：'+topic+'\n'+'发件人：'+send+
                 '\n'+'时间：'+send_time+'\n'+'主要内容：\n'+mainContent)
        temp = QMessageBox.warning(self, "提示", message, QMessageBox.Yes)

    def createMenus(self):
        # 创建动作 注销
        self.printAction1 = QAction(self.tr("注销"), self)
        self.printAction1.triggered.connect(self.on_printAction1_triggered)

        # 创建动作 退出
        self.printAction2 = QAction(self.tr("退出"), self)
        self.printAction2.triggered.connect(self.on_printAction2_triggered)

        # 创建菜单，添加动作
        self.printMenu = self.menuBar().addMenu(self.tr("注销和退出"))
        self.printMenu.addAction(self.printAction1)
        self.printMenu.addAction(self.printAction2)

    # 动作一：注销
    def on_printAction1_triggered(self):
        self.close()
        dialog = logindialog(mode=1)
        if dialog.exec_() == QDialog.Accepted:
            the_window = MainWindow()
            self.windowList.append(the_window)    #这句一定要写，不然无法重新登录
            the_window.show()

    # 动作二：退出
    def on_printAction2_triggered(self):
        self.close()

    # 关闭界面触发事件
    def closeEvent(self, event):
        self.im.close()
        pass

################################################
#######对话框
################################################
class logindialog(QDialog):
    def __init__(self,mode=0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.im = imap.Imapmail()
        self.mode = mode
        self.setWindowTitle('登录界面')
        self.resize(200, 200)
        self.setFixedSize(self.width(), self.height())
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        ###### 设置界面控件
        self.frame = QFrame(self)
        self.verticalLayout = QVBoxLayout(self.frame)

        self.lineEdit_account = QLineEdit()
        self.lineEdit_account.setPlaceholderText("请输入账号")
        self.verticalLayout.addWidget(self.lineEdit_account)

        self.lineEdit_password = QLineEdit()
        self.lineEdit_password.setPlaceholderText("请输入密码")
        self.verticalLayout.addWidget(self.lineEdit_password)

        self.checkBox_remeberpassword = QCheckBox()
        self.checkBox_remeberpassword.setText("记住密码")
        self.verticalLayout.addWidget(self.checkBox_remeberpassword)

        self.checkBox_autologin = QCheckBox()
        self.checkBox_autologin.setText("自动登录")
        self.verticalLayout.addWidget(self.checkBox_autologin)


        self.pushButton_enter = QPushButton()
        self.pushButton_enter.setText("确定")
        self.verticalLayout.addWidget(self.pushButton_enter)

        self.pushButton_quit = QPushButton()
        self.pushButton_quit.setText("取消")
        self.verticalLayout.addWidget(self.pushButton_quit)

        ###### 绑定按钮事件
        self.pushButton_enter.clicked.connect(self.on_pushButton_enter_clicked)
        self.pushButton_quit.clicked.connect(QCoreApplication.instance().quit)


        ####初始化登录信息
        self.init_login_info()


        ####自动登录
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.goto_autologin)
        self.timer.setSingleShot(True)
        self.timer.start(1000)

    # 自动登录
    def goto_autologin(self):
        if self.checkBox_autologin.isChecked()==True and self.mode == 0 :
           self.on_pushButton_enter_clicked()

    # 验证登录信息
    def on_pushButton_enter_clicked(self):
        # 账号判断
        self.im.client()
        self.im.user=self.lineEdit_account.text()
        self.im.pass_wd=self.lineEdit_password.text()
        print(self.im.user)
        print(self.im.pass_wd)
        self.im.server_address = 'imap.' + self.im.user.split('@')[-1]  # 邮箱地址
        print(self.im.server_address)
        if self.im.user.split('@')[-1] in ['163.com', 'qq.com', '126.com']:
            self.im.client()
            e = self.im.login()
            if e == 0:
                password_replay = QMessageBox.warning(self, "!", "账号或密码输入错误", QMessageBox.Yes)
            else:
                #self.im.get_all_mails()

                #self.im.close()
                ####### 保存登录信息
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
        settings = QSettings("config.ini", QSettings.IniFormat)        #方法1：使用配置文件
        #settings = QSettings("mysoft","myapp")                        #方法2：使用注册表
        settings.setValue("account",self.lineEdit_account.text())
        settings.setValue("password", self.lineEdit_password.text())
        settings.setValue("remeberpassword", self.checkBox_remeberpassword.isChecked())
        settings.setValue("autologin", self.checkBox_autologin.isChecked())

    # 初始化登录信息
    def init_login_info(self):
        settings = QSettings("config.ini", QSettings.IniFormat)        #方法1：使用配置文件
        #settings = QSettings("mysoft","myapp")                        #方法2：使用注册表
        the_account =settings.value("account")
        the_password = settings.value("password")
        the_remeberpassword = settings.value("remeberpassword")
        the_autologin = settings.value("autologin")
        ########
        self.lineEdit_account.setText(the_account)
        if the_remeberpassword=="true" or  the_remeberpassword==True:
            self.checkBox_remeberpassword.setChecked(True)
            self.lineEdit_password.setText(the_password)

        if the_autologin=="true" or  the_autologin==True:
            self.checkBox_autologin.setChecked(True)


################################################
#######程序入口
################################################
if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = logindialog(mode=0)
    im=dialog.get_imap()
    if  dialog.exec_()==QDialog.Accepted:
        the_window = MainWindow(im)
        the_window.show()
        sys.exit(app.exec_())

