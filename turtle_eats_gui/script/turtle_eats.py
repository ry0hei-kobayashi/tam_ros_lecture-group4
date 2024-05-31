# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'turtle_eats.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(393, 528)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(10, 390, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_4.setFont(font)
        self.label_4.setTextFormat(QtCore.Qt.RichText)
        self.label_4.setObjectName("label_4")
        self.label_status = QtWidgets.QLabel(self.centralwidget)
        self.label_status.setGeometry(QtCore.QRect(130, 370, 231, 91))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_status.setFont(font)
        self.label_status.setText("")
        self.label_status.setObjectName("label_status")
        self.comboBox_menu = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_menu.setGeometry(QtCore.QRect(240, 150, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.comboBox_menu.setFont(font)
        self.comboBox_menu.setObjectName("comboBox_menu")
        self.comboBox_menu.addItem("")
        self.comboBox_menu.addItem("")
        self.comboBox_menu.addItem("")
        self.pushButton_order = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_order.setGeometry(QtCore.QRect(110, 220, 161, 121))
        font = QtGui.QFont()
        font.setPointSize(17)
        self.pushButton_order.setFont(font)
        self.pushButton_order.setObjectName("pushButton_order")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(250, 120, 101, 21))
        self.label_2.setObjectName("label_2")
        self.comboBox_person = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_person.setGeometry(QtCore.QRect(30, 150, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(17)
        self.comboBox_person.setFont(font)
        self.comboBox_person.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.comboBox_person.setStyleSheet("")
        self.comboBox_person.setEditable(False)
        self.comboBox_person.setObjectName("comboBox_person")
        self.comboBox_person.addItem("")
        self.comboBox_person.addItem("")
        self.comboBox_person.addItem("")
        self.comboBox_person.addItem("")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 120, 111, 31))
        self.label.setObjectName("label")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(100, 10, 191, 81))
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap("/home/ros/Documents/gui_ws/catkin_ws/src/gui_pkg/script/title.drawio.png"))
        self.label_3.setObjectName("label_3")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 393, 20))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.toolBar_2 = QtWidgets.QToolBar(MainWindow)
        self.toolBar_2.setObjectName("toolBar_2")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar_2)

        self.retranslateUi(MainWindow)
        self.comboBox_person.activated['QString'].connect(MainWindow.activated_person)
        self.comboBox_menu.activated['QString'].connect(MainWindow.activated_menu)
        self.pushButton_order.clicked.connect(MainWindow.clicked_order)
        self.label_status.windowTitleChanged['QString'].connect(MainWindow.status_show)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_4.setText(_translate("MainWindow", "ステータス："))
        #`self.comboBox_menu.setItemText(0, _translate("MainWindow", "中華"))
        #`self.comboBox_menu.setItemText(1, _translate("MainWindow", "洋食"))
        #`self.comboBox_menu.setItemText(2, _translate("MainWindow", "和食"))
        self.comboBox_menu.setItemText(0, _translate("MainWindow", "ChineseFood"))
        self.comboBox_menu.setItemText(1, _translate("MainWindow", "ItalianFood"))
        self.comboBox_menu.setItemText(2, _translate("MainWindow", "JapaneseFood"))
        self.pushButton_order.setText(_translate("MainWindow", "注文"))
        self.label_2.setText(_translate("MainWindow", "何を注文する？"))
        self.comboBox_person.setItemText(0, _translate("MainWindow", "A"))
        self.comboBox_person.setItemText(1, _translate("MainWindow", "B"))
        self.comboBox_person.setItemText(2, _translate("MainWindow", "C"))
        self.comboBox_person.setItemText(3, _translate("MainWindow", "D"))
        self.label.setText(_translate("MainWindow", "誰に届ける？"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.toolBar_2.setWindowTitle(_translate("MainWindow", "toolBar_2"))