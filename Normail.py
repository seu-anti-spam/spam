import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
import Infor

class NormailUi(QWidget):
    def __init__(self):
        super(NormailUi, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("正常邮件")
        self.resize(600, 527)
        # sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        # # sizePolicy.setHeightForWidth(NormailUi.sizePolicy().hasHeightForWidth())
        # NormailUi.setSizePolicy(sizePolicy)
        layout = QVBoxLayout()
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

        self.addLine('1581261592@qq.com', 'test1', 0, True)
        self.addLine('17782264946@qq.com', 'test2', 1, True)
        self.addLine('qq.com', 'test3', 2, False)

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
    def addLine(self, name, text, id, sign):
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

        # 打开按钮
        openBtn = QPushButton("open")
        openBtn.clicked.connect(lambda: self.onBtnOpen(id))

        # 关闭按钮
        delBtn = QPushButton("delete")
        row = self.row_count
        # delBtn.clicked.connect(lambda: self.onBtnDel(row))
        delBtn.clicked.connect(self.onBtnDel)

        # 下载附件按钮
        dlBtn = QPushButton("下载附件")
        if not sign:
            dlBtn.setEnabled(False)
        dlBtn.clicked.connect(lambda: self.onBtnDL(sign))

        # self.tableWidget.setItem(self.row_count, 0, QTableWidgetItem(name))
        self.tableWidget.setCellWidget(self.row_count, 0, sender)
        self.tableWidget.setCellWidget(self.row_count, 1, infor)
        self.tableWidget.setCellWidget(self.row_count, 2, openBtn)
        self.tableWidget.setCellWidget(self.row_count, 3, delBtn)
        self.tableWidget.setCellWidget(self.row_count, 4, dlBtn)

    def addBlankLine(self):
        self.row_count = self.tableWidget.rowCount()
        self.tableWidget.insertRow(self.row_count)
        self.tableWidget.setItem(self.row_count, 0, QTableWidgetItem(" "))
        self.tableWidget.setItem(self.row_count, 1, QTableWidgetItem(" "))
        self.tableWidget.setItem(self.row_count, 2, QTableWidgetItem(" "))
        self.tableWidget.setItem(self.row_count, 3, QTableWidgetItem(" "))

    def onBtnOpen(self, id):
        dialog = Infor.InforUi()
        dialog.exec()


    #@QtCore.pyqtSlot()
    def onBtnDel(self):
        button = self.sender()
        if button:
            print(button)
            print("x")
            r = self.tableWidget.indexAt(button.pos()).row()
            row = int(r)
            print(row)
            self.tableWidget.removeRow(row)
            self.row_count = self.row_count - 1

    def onBtnDL(self, sign):
        pass



if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialag = NormailUi()
    dialag.show()
    sys.exit(app.exec_())