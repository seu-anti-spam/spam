from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore
import AddAssociateList
import imap

class AssociateListUi(QDialog):
    def __init__(self):
        super(AssociateListUi, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("关联邮箱")
        self.setWindowIcon(QIcon('images/LOGO.png'))
        self.resize(290, 500)
        self.setFixedSize(self.width(), self.height())
        layout = QVBoxLayout()
        self.setWindowOpacity(0.9)
        self.setStyleSheet('''
                QDialog{
                        background:#DCDCDC;
                        font-family: "Microsoft Yahei";}         
        ''')

        self.addBtn = QPushButton("添加")
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

        self.tableWidget = QTableWidget()
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
        for each in imap.associate_list:
            self.addLine(each)

        layout.addWidget(self.tableWidget)
        layout.addWidget(self.addBtn)
        self.setLayout(layout)

    def onBtnAdd(self):
        dialog = AddAssociateList.AddAssociateListUi()
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

            self.tableWidget.setCellWidget(self.row_count, 0, member)
            self.tableWidget.setCellWidget(self.row_count, 1, reMovBtn)


    def onBtnReMov(self, name):
        button = self.sender()
        if button:
            r = self.tableWidget.indexAt(button.pos()).row()
            row = int(r)
            self.tableWidget.removeRow(row)
            self.row_count = self.row_count - 1
            imap.associate_list.remove(name)

