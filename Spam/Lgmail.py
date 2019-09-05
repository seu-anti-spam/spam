import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtGui import *
import Infor
import pickle
import NewSign

extra_list = ['0']


class LgmailUi(QDialog):
    def __init__(self, im, temp, mail):
        super(LgmailUi, self).__init__()
        global extra_list
        self.im = im
        self.mails = mail
        # pickle_file = open('received_mails.pkl', 'rb')
        # self.mails = pickle.load(pickle_file)
        extra_list = temp
        self.initUI()

    def initUI(self):
        self.setWindowTitle("垃圾邮件")
        self.resize(680, 527)
        layout = QHBoxLayout()
        self.setWindowOpacity(0.9)
        self.setStyleSheet('''
                                QDialog{
                                        background:#DCDCDC;
                                        font-family: "Microsoft Yahei";}         
                                ''')

        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(5)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setVisible(False)
        self.tableWidget.setShowGrid(False)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setColumnWidth(0, 150)
        self.tableWidget.setColumnWidth(1, 250)
        self.tableWidget.setColumnWidth(2, 85)
        self.tableWidget.setColumnWidth(3, 85)
        self.tableWidget.setColumnWidth(4, 85)
        self.tableWidget.setStyleSheet('''
                                    QTableWidget{
                                                text-align: center;
                                                background:transparent;
                                                font-family: SimHei;}            
                                    ''')
        self.row_count = 0
        i = 0
        for each in self.mails['垃圾邮件']:
            self.addLine(each['发件人'], each['主题'], i, 1)
            i += 1
        layout.addWidget(self.tableWidget)
        self.setLayout(layout)

    #### 动态添加一行信息
    def addLine(self, name, text, id, flag):
        # 添加一空白行
        self.row_count = self.tableWidget.rowCount()
        self.tableWidget.insertRow(self.row_count)

        # 发件人
        sender = QLabel()
        sender.setFocusPolicy(QtCore.Qt.NoFocus)
        sender.setText(name)
        sender.setToolTip(name)
        sender.setFont(QFont("Segoe UI"))

        # 邮件内容
        infor = QLineEdit()
        infor.setFocusPolicy(QtCore.Qt.NoFocus)
        infor.setText(text)
        infor.setStyleSheet('''
                                    QLineEdit{
                                        color:#4F4F4F;
                                        font-family:"Segoe UI";
                                        background:transparent;
                                        border:none;}
                                        ''')

        # 添加信任按钮
        moveBtn = QPushButton("移动")
        moveBtn.clicked.connect(lambda: self.onBtnMove(id))
        btStlSheet = '''QPushButton
                                                 {text-align : center;
                                                 background-color:white;
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
        moveBtn.setStyleSheet(btStlSheet)

        # 打开按钮
        openBtn = QPushButton("打开")
        openBtn.clicked.connect(lambda: self.onBtnOpen(id))
        openBtn.setStyleSheet(btStlSheet)

        # 关闭按钮
        delBtn = QPushButton("删除")
        row = self.row_count
        # delBtn.clicked.connect(lambda: self.onBtnDel(row))
        delBtn.clicked.connect(lambda: self.onBtnDel(id))
        delBtn.setStyleSheet(btStlSheet)

        # self.tableWidget.setItem(self.row_count, 0, QTableWidgetItem(name))
        self.tableWidget.setCellWidget(self.row_count, 0, sender)
        self.tableWidget.setCellWidget(self.row_count, 1, infor)
        self.tableWidget.setCellWidget(self.row_count, 2, moveBtn)
        self.tableWidget.setCellWidget(self.row_count, 3, openBtn)
        self.tableWidget.setCellWidget(self.row_count, 4, delBtn)

    def onBtnMove(self, id):
        button = self.sender()
        if button:
            r = self.tableWidget.indexAt(button.pos()).row()
            row = int(r)
            self.tableWidget.removeRow(row)
            self.row_count = self.row_count - 1
            temp = self.mails['垃圾邮件'][id].copy()
            self.mails['正常邮件'].append(self.mails['垃圾邮件'][id])
            del self.mails['垃圾邮件'][id]
            global extra_list
            temp.pop('邮件')
            temp.pop('垃圾')
            extra_list.append(temp)

    def onBtnOpen(self, id):
        dialog = Infor.InforUi(self.mails['垃圾邮件'][id])
        dialog.exec()

    def onBtnDel(self, id):
        button = self.sender()
        if button:
            r = self.tableWidget.indexAt(button.pos()).row()
            row = int(r)
            self.tableWidget.removeRow(row)
            self.row_count = self.row_count - 1
            self.im.delete_mail(self.mails['垃圾邮件'][id]['邮件'])
            for each in self.mails['垃圾邮件'][id + 1:]:
                each['邮件'] -= 1
            del self.mails['垃圾邮件'][id]

    def closeEvent(self, event):
        # pickle_file = open('received_mails.pkl', 'wb')  # 存储到本地文件
        # pickle.dump(self.mails, pickle_file)
        # pickle_file.close()
        pickle_file_2 = open('extra_list.pkl', 'wb')  # 存储到本地文件
        pickle.dump(extra_list, pickle_file_2)
        pickle_file_2.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialag = LgmailUi()
    dialag.show()
    sys.exit(app.exec_())