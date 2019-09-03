import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
import Infor

class LgmailUi(QWidget):
    def __init__(self):
        super(LgmailUi, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("垃圾邮件")
        self.resize(600, 527)
        # sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        # # sizePolicy.setHeightForWidth(NormailUi.sizePolicy().hasHeightForWidth())
        # NormailUi.setSizePolicy(sizePolicy)
        layout = QHBoxLayout()
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(5)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setVisible(False)
        self.tableWidget.setShowGrid(False)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setColumnWidth(0, 100)
        self.tableWidget.setColumnWidth(1, 300)
        self.tableWidget.setColumnWidth(2, 85)
        self.tableWidget.setColumnWidth(3, 85)
        self.tableWidget.setColumnWidth(4, 85)
        self.row_count = 0

        self.addLine('1581261592@qq.com', 'test1', 0)
        self.addLine('17782264946@qq.com', 'test2', 1)
        self.addLine('qq.com', 'test3', 2)

        # row_count = self.tableWidget.rowCount()
        # self.tableWidget.insertRow(row_count)
        # infor = QLineEdit()
        # infor.setText("test")
        # openBtn = QPushButton("open")
        # delBtn = QPushButton("delete")
        # self.tableWidget.setItem(row_count,0,QTableWidgetItem('one'))
        # self.tableWidget.setCellWidget(row_count,1,infor)
        # self.tableWidget.setCellWidget(row_count,2,openBtn)
        # self.tableWidget.setCellWidget(row_count,3,delBtn)

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

        # 邮件内容
        infor = QLineEdit()
        infor.setFocusPolicy(QtCore.Qt.NoFocus)
        infor.setText(text)

        # 添加信任按钮
        moveBtn = QPushButton("move")
        moveBtn.clicked.connect(lambda: self.onBtnMove(id))

        # 打开按钮
        openBtn = QPushButton("open")
        openBtn.clicked.connect(lambda: self.onBtnOpen(id))

        # 关闭按钮
        delBtn = QPushButton("delete")
        row = self.row_count
        # delBtn.clicked.connect(lambda: self.onBtnDel(row))
        delBtn.clicked.connect(lambda: self.onBtnDel(id))

        # self.tableWidget.setItem(self.row_count, 0, QTableWidgetItem(name))
        self.tableWidget.setCellWidget(self.row_count, 0, sender)
        self.tableWidget.setCellWidget(self.row_count, 1, infor)
        self.tableWidget.setCellWidget(self.row_count, 2, moveBtn)
        self.tableWidget.setCellWidget(self.row_count, 3, openBtn)
        self.tableWidget.setCellWidget(self.row_count, 4, delBtn)

    def onBtnMove(self, id):
        button = self.sender()
        if button:
            print(button)
            r = self.tableWidget.indexAt(button.pos()).row()
            row = int(r)
            self.tableWidget.removeRow(row)
            self.row_count = self.row_count - 1
        pass

    def onBtnOpen(self, id):
        dialog = Infor.InforUi()
        dialog.exec()

        pass

    #@QtCore.pyqtSlot()
    def onBtnDel(self, id):
        button = self.sender()
        if button:
            print(button)
            r = self.tableWidget.indexAt(button.pos()).row()
            row = int(r)
            self.tableWidget.removeRow(row)
            self.row_count = self.row_count - 1



if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialag = LgmailUi()
    dialag.show()
    sys.exit(app.exec_())