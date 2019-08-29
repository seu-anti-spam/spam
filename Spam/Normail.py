import sys

from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtGui import *
import Infor
import Lgmail
import NewSign
import pickle


class DownLoadThread(QThread):

    def __init__(self, im, id, mails, btn):
        super().__init__()
        self.im = im
        self.result = list()
        self.id = id
        self.mails = mails
        self.btn = btn

    def run(self):
        self.im.get_attach(self.mails['正常邮件'][self.id]['邮件'])
        self.btn.setText("完成")

class NormailUi(QDialog):
    def __init__(self, im, mail):
        super(NormailUi, self).__init__()
        self.mails = mail
        self.im = im
        self.initUI()
        self.download = None

    def initUI(self):
        self.setWindowTitle("正常邮件")
        self.resize(680, 527)
        layout = QHBoxLayout()
        self.setWindowOpacity(0.9)
        self.setStyleSheet('''
                        QDialog{
                                background:#F5F5F5;
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
                                        background: transparent;
                                        font-family: SimHei;}            
                            ''')

        self.row_count = 0
        i = 0
        for each in self.mails['正常邮件']:
            self.addLine(each['发件人'], each['主题'], i)
            i += 1
        layout.addWidget(self.tableWidget)
        self.setLayout(layout)

    #### 动态添加一行信息
    def addLine(self, name, text, id):
        # 添加一空白行
        self.row_count = self.tableWidget.rowCount()
        self.tableWidget.insertRow(self.row_count)

        # 发件人
        sender = QLabel()
        sender.setFocusPolicy(QtCore.Qt.NoFocus)
        sender.setText(name)
        sender.setToolTip(name)
        sender.setFont(QFont("Segoe UI"))
        # sender.setStyleSheet('''
        #                     QLabel{
        #                         dont-family:"Segoe UI";
        #                         background:white;
        #                         border:none;}
        #                         ''')

        # 邮件内容
        infor = QLineEdit()
        infor.setFocusPolicy(QtCore.Qt.NoFocus)
        infor.setText(text)
        infor.setStyleSheet('''
                            QLineEdit{
                                color:#4F4F4F;
                                font-family:"Segoe UI";
                                background: transparent;
                                border:none;}
                                ''')

        # 打开按钮
        # print(self.mails['正常邮件'][id-1])
        openBtn = QPushButton("打开")
        openBtn.clicked.connect(lambda: self.onBtnOpen(id))
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
        openBtn.setStyleSheet(btStlSheet)

        # 关闭按钮
        delBtn = QPushButton("删除")
        row = self.row_count
        # delBtn.clicked.connect(lambda: self.onBtnDel(row))
        delBtn.setStyleSheet(btStlSheet)

        # 下载按钮
        dlBtn = QPushButton("下载附件")
        dlBtn.clicked.connect(lambda: self.onBtnDL(id))
        if not self.mails['正常邮件'][id]['附件']:
            dlBtn.setEnabled(False)
        dlBtn.setStyleSheet(btStlSheet)


        delBtn.clicked.connect(lambda: self.onBtnDel(id))

        # self.tableWidget.setItem(self.row_count, 0, QTableWidgetItem(name))
        self.tableWidget.setCellWidget(self.row_count, 0, sender)
        self.tableWidget.setCellWidget(self.row_count, 1, infor)
        self.tableWidget.setCellWidget(self.row_count, 2, openBtn)
        self.tableWidget.setCellWidget(self.row_count, 3, delBtn)
        self.tableWidget.setCellWidget(self.row_count, 4, dlBtn)

    def onBtnDL(self, id):
        Btn = self.sender()
        Btn.setEnabled(False)
        Btn.setText("正在下载...")
        self.download = DownLoadThread(self.im, id, self.mails, Btn)
        self.download.start()

    def onBtnOpen(self, id):
        dialog = Infor.InforUi(self.mails['正常邮件'][id])
        dialog.exec()

    def onBtnDel(self, id):
        button = self.sender()
        if button:
            r = self.tableWidget.indexAt(button.pos()).row()
            row = int(r)
            self.tableWidget.removeRow(row)
            self.row_count = self.row_count - 1
            # self.im.delete_mail(self.mails['正常邮件'][id]['邮件'])

            for each in self.mails['正常邮件'][id + 1:]:
                each['邮件'] -= 1
            del self.mails['正常邮件'][id]

    def closeEvent(self, event):
        # pickle_file = open('received_mails.pkl', 'wb')  # 存储到本地文件
        # pickle.dump(self.mails, pickle_file)
        # pickle_file.close()
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialag = NormailUi()
    dialag.show()
    sys.exit(app.exec_())