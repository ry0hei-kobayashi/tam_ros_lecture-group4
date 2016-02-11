#!/usr/bin python3.9

import rospy
import smach
import smach_ros
 
from face_recog import FaceRecog
from turtle_eats_gui.get_order import GetOrder

def create_sm():
    sm = smach.StateMachine(outcomes=['success', 'failure'])

    sm.userdata.person_name = None
    sm.userdata.menu_name = None

    with sm:

        smach.StateMachine.add('ORDER', GetOrder(),
                               transitions={'success':'FACE'})

        smach.StateMachine.add('FACE', FaceRecog(),
                               transitions={'success': 'success',
                                             'failure': 'FACE'})

        #smach.StateMachine.add('FINISH', ,
        #                       taransitions={'success': 'success'})

        
    return sm

if __name__ == "__main__":
    rospy.init_node('test_rec', anonymous=True)
    sm = create_sm()
    outcome = sm.execute()
    if outcome == 'success':
        rospy.loginfo('I finished the task.')
    else:
        rospy.signal_shutdown('Some error occured.')



