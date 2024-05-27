#! /usr/bin/python3
#-*- coding: utf-8 -*-

#GUI
import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from turtle_eats import Ui_MainWindow

class Test(QMainWindow):
    def __init__(self,parent=None):
        #GUI
        super(Test, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
    
    def clicked_order(self):
        pass
    
    def activated_person(self):
        pass

    def activated_menu(self):
        pass
    
    def status_show(self):
        pass


if __name__=='__main__':
    app = QApplication(sys.argv)
    window = Test()
    window.show()
    sys.exit(app.exec_())