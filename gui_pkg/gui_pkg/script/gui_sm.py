#!/usr/bin/env python3
# -*-encoding:utf-8-*-
import rospy
import smach
import smach_ros
from std_msgs.msg import String
from gui_pkg.msg import Order
from enum import Enum

person_goal = {'A':[],'B':[],'C':[]}
menu_goal = {'中華':[], '洋食':[],'和食',[]}

class gui_sm(smach.State):

    def __init__(self):
        smach.State.__init__(self)
        self.ui =

    def execute(self):
        self.order_data  = rospy.wait_for_message('topic_order',Order,timeout=None )
        print(f"{self.order_data.person_name}, {self.order_data.menu_name}")
    
    def 

   
    


if __name__=='__main__':
    rospy.init_node('gui_lis', anonymous=True)
    sm = gui_sm()
    sm.execute()
    rate = rospy.Rate(10)

        
        

        
