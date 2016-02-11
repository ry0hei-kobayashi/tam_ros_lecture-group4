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
#from gui_pkg.msg import Order
from turtle_eats_gui.msg import Order


class Test(QMainWindow):
    def __init__(self,parent=None):
        #GUI
        super(Test, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.orderflg = 0
        self.order = Order()
        self.order.person_name = None
        self.order.menu_name = None
        self.order.person_name = "hirayae"
        self.order.menu_name = "ChineseFood"
        Test.status_show(self)
        #self.pub_person = rospy.Publisher('topic_person',String, queue_size=1)
        #self.pub_menu = rospy.Publisher('topic_menu',String, queue_size=1)
        self.pub_order = rospy.Publisher('send_order',Order, queue_size=1)
    
    def clicked_order(self):
        self.orderflg = 1
        Test.status_show(self)
        #self.pub_person.publish(self.person)
        #self.pub_menu.publish(self.menu)
        self.pub_order.publish(self.order)

    def activated_person(self):
	    #self.person.data = self.ui.comboBox_person.currentText()
	    self.order.person_name = self.ui.comboBox_person.currentText()
	    #print(person)

    def activated_menu(self):
        #self.menu.data = self.ui.comboBox_menu.currentText()
	    self.order.menu_name = self.ui.comboBox_menu.currentText()
        #print(menu)

    def status_show(self):
        if (self.orderflg == 0):
            self.ui.label_status.setText("注文ボタンを押してください")       
        elif (self.orderflg == 1) :
            self.ui.label_status.setText(f"注文が完了しました．\n商品到着までお待ちください．\n届ける人：{self.order.person_name}\n商品：{self.order.menu_name}")
        else :
            self.ui.label_status.setText("error")
            


if __name__=='__main__':
    rospy.init_node('ui_talker', anonymous=True)
    rate = rospy.Rate(10)
    app = QApplication(sys.argv)
    window = Test()
    window.show()
    sys.exit(app.exec_())
