# Form implementation generated from reading ui file 'client_gui.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(645, 554)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(parent=self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 641, 511))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.input = QtWidgets.QLineEdit(parent=self.verticalLayoutWidget)
        self.input.setObjectName("input")
        self.gridLayout.addWidget(self.input, 3, 3, 1, 1)
        self.send_button = QtWidgets.QPushButton(parent=self.verticalLayoutWidget)
        self.send_button.setObjectName("send_button")
        self.gridLayout.addWidget(self.send_button, 3, 4, 1, 1)
        self.output = QtWidgets.QTextEdit(parent=self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.output.setFont(font)
        self.output.setReadOnly(True)
        self.output.setObjectName("output")
        self.gridLayout.addWidget(self.output, 0, 3, 1, 2)
        self.verticalLayout.addLayout(self.gridLayout)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.second = QtWidgets.QPushButton(parent=self.verticalLayoutWidget)
        self.second.setObjectName("second")
        self.gridLayout_2.addWidget(self.second, 3, 1, 1, 1)
        self.first = QtWidgets.QPushButton(parent=self.verticalLayoutWidget)
        self.first.setObjectName("first")
        self.gridLayout_2.addWidget(self.first, 3, 0, 1, 1)
        self.third = QtWidgets.QPushButton(parent=self.verticalLayoutWidget)
        self.third.setObjectName("third")
        self.gridLayout_2.addWidget(self.third, 3, 2, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 645, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.send_button.setText(_translate("MainWindow", "send"))
        self.second.setText(_translate("MainWindow", "2"))
        self.first.setText(_translate("MainWindow", "1"))
        self.third.setText(_translate("MainWindow", "3"))
