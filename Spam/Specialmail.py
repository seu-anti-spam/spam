from PyQt5.QtWidgets import *
from PyQt5 import QtCore
import Infor
import Normail



class SpecialmailUi(QDialog):
    def __init__(self, name, im, mails):
        super(SpecialmailUi, self).__init__()
        self.name = name
        self.received_mails = mails
        self.im = im
        self.initUI()

    def initUI(self):
        self.setWindowTitle("特别关心邮件")
        self.resize(600, 527)
        self.setWindowOpacity(0.9)
        self.setStyleSheet('''
                                QDialog{
                                        background:#F5F5F5;
                                        font-family: "Microsoft Yahei";}         
                                ''')
        layout = QVBoxLayout()
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(4)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setVisible(False)
        self.tableWidget.setShowGrid(False)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setColumnWidth(0, 150)
        self.tableWidget.setColumnWidth(1, 250)
        self.tableWidget.setColumnWidth(2, 85)
        self.tableWidget.setColumnWidth(3, 85)
        self.tableWidget.setStyleSheet('''
                                    QTableWidget{
                                                text-align: center;
                                                background: transparent;
                                                font-family: SimHei;}            
                                    ''')
        self.row_count = 0
        self.mails = list()
        i = 0
        for each in self.received_mails['正常邮件']:
            if each['发件人'] == self.name:
                self.mails.append(each)
                self.addLine(self.name, each['主题'], i)
                i += 1

        layout.addWidget(self.tableWidget)
        self.setLayout(layout)

    # 动态添加一行信息
    def addLine(self, name, text, id):
        # 添加一空白行
        self.row_count = self.tableWidget.rowCount()
        self.tableWidget.insertRow(self.row_count)

        # 发件人
        sender = QLineEdit()
        sender.setFocusPolicy(QtCore.Qt.NoFocus)
        sender.setText(name)
        sender.setToolTip(name)
        sender.setStyleSheet('''
                                    QLineEdit{
                                        color:#4F4F4F;
                                        font-family:"Segoe UI";
                                        background: #F5F5F5;
                                        border:none;}
                                        ''')

        # 邮件内容
        infor = QLineEdit()
        infor.setFocusPolicy(QtCore.Qt.NoFocus)
        infor.setText(text)
        infor.setToolTip(text)
        infor.setStyleSheet('''
                            QLineEdit{
                                color:#4F4F4F;
                                font-family:"Segoe UI";
                                background: transparent;
                                border:none;}
                                ''')
        # 打开按钮
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

        # 下载按钮
        dlBtn = QPushButton("下载附件")
        dlBtn.clicked.connect(lambda: self.onBtnDL(id))
        if not self.mails[id]['附件']:
            dlBtn.setEnabled(False)
        dlBtn.setStyleSheet(btStlSheet)

        self.tableWidget.setCellWidget(self.row_count, 0, sender)
        self.tableWidget.setCellWidget(self.row_count, 1, infor)
        self.tableWidget.setCellWidget(self.row_count, 2, openBtn)
        self.tableWidget.setCellWidget(self.row_count, 3, dlBtn)

    def onBtnOpen(self, id):
        dialog = Infor.InforUi(self.mails[id])
        dialog.exec()

    def onBtnDL(self, id):
        Btn = self.sender()
        Btn.setEnabled(False)
        Btn.setText("正在下载...")
        self.download = Normail.DownLoadThread(self.im, id, self.mails, Btn)
        self.download.start()



