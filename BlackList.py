import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
import AddBlackList


class BlackListUi(QWidget):
    def __init__(self):
        super(BlackListUi, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("黑名单")
        self.resize(290, 527)
        self.setFixedSize(self.width(), self.height())
        layout = QVBoxLayout()

        self.addBtn = QPushButton("添加")
        self.addBtn.clicked.connect(self.onBtnAdd)

        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(2)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setVisible(False)
        self.tableWidget.setShowGrid(False)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setColumnWidth(0, 170)
        self.tableWidget.setColumnWidth(1, 80)
        self.row_count = 0

        self.addLine('1581261592@qq.com', 0)
        self.addLine('1782264946@qq.com', 1)
        self.addLine('1588546457@qq.com', 2)

        layout.addWidget(self.tableWidget)
        layout.addWidget(self.addBtn)
        self.setLayout(layout)

    def onBtnAdd(self):
        dialog = AddBlackList.AddBlackListUi()
        dialog.exec()

    #### 动态添加一行信息
    def addLine(self, name, id):
        # 添加一空白行
        self.row_count = self.tableWidget.rowCount()
        self.tableWidget.insertRow(self.row_count)


        # 联系人
        member = QLineEdit()
        member.setFocusPolicy(QtCore.Qt.NoFocus)
        member.setText(name)


        # 移除按钮
        reMovBtn = QPushButton("delete")
        row = self.row_count
        # delBtn.clicked.connect(lambda: self.onBtnDel(row))
        reMovBtn.clicked.connect(lambda: self.onBtnReMov(id))

        # self.tableWidget.setItem(self.row_count, 0, QTableWidgetItem(name))
        self.tableWidget.setCellWidget(self.row_count, 0, member)
        self.tableWidget.setCellWidget(self.row_count, 1, reMovBtn)




    def onBtnReMov(self, id):
        button = self.sender()
        if button:
            r = self.tableWidget.indexAt(button.pos()).row()
            row = int(r)
            self.tableWidget.removeRow(row)
            self.row_count = self.row_count - 1



if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialag = BlackListUi()
    dialag.show()
    sys.exit(app.exec_())