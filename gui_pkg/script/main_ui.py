#! /usr/bin/python3
#-*-encoding:UTF8-*-

#GUI
import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from turtle_eats import Ui_MainWindow

## ROS
import rospy
from std_msgs.msg import String


class Test(QMainWindow):
    def __init__(self,parent=None):
        #GUI
        super(Test, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.orderflg = 0
        self.person = String()
        self.person.data = "A"
        self.menu = String()
        self.menu.data = "中華"
        Test.status_show(self)
        self.pub_person = rospy.Publisher('topic_person',String, queue_size=1)
        self.pub_menu = rospy.Publisher('topic_menu',String, queue_size=1)
    
    def clicked_order(self):
	    #print(f"{self.menu},{self.person}")
        self.orderflg = 1
        Test.status_show(self)
        self.pub_person.publish(self.person)
        self.pub_menu.publish(self.menu)

    def activated_person(self):
	    self.person.data = self.ui.comboBox_person.currentText()
	    #print(person)

    def activated_menu(self):
        self.menu.data = self.ui.comboBox_menu.currentText()
        #print(menu)

    def status_show(self):
        if (self.orderflg == 0):
            self.ui.label_status.setText("注文ボタンを押してください")       
        elif (self.orderflg == 1) :
            self.ui.label_status.setText(f"注文が完了しました．\n商品到着までお待ちください．\n届ける人：{self.person.data}\n商品：{self.menu.data}")
        else :
            self.ui.label_status.setText("error")
            


if __name__=='__main__':
    rospy.init_node('ui_talker', anonymous=True)
    rate = rospy.Rate(10)
    app = QApplication(sys.argv)
    window = Test()
    window.show()
    sys.exit(app.exec_())
