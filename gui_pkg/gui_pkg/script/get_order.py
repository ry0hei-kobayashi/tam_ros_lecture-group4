#!/usr/bin/env python3
# -*-encoding:utf-8-*-
import rospy
import smach
import smach_ros
from std_msgs.msg import String
from gui_pkg.msg import Order

person_goal = {'A':[],'B':[],'C':[]}
menu_goal = {'ChineseFood':[], 'ItalianFood':[],'JapaneseFood':[]}

class GetOrder(smach.State):

    def __init__(self):
        smach.State.__init__(self, outcomes=['success'], input_keys=['person_name', 'menu_name'],
                                                         output_keys=['person_name', 'menu_name'])
    

    def execute(self, userdata):
        order_data  = rospy.wait_for_message('send_order', Order, timeout=None )

        userdata.person_name = order_data.person_name
        userdata.menu_name = order_data.menu_name

        print('person_name = ', userdata.person_name)
        print('menu_name = ', userdata.menu_name)

        return "success"

if __name__=='__main__':
    rospy.init_node('gui_lis', anonymous=True)

    sm = smach.StateMachine(outcomes=['success'])
    sm.userdata.person_name = None
    sm.userdata.menu_name = None
    
    with sm:
        smach.StateMachine.add('DEBUG', GetOrder(),
                               transitions = {'success': 'DEBUG'})
    sm.execute()
    rospy.spin()

        
        

        
