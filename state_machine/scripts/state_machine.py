#!/usr/bin python3

import rospy
import smach
import smach_ros
from plan import Plan
from move import Move
from slope import VelControl
from face_recog import FaceRecog
 
from turtle_eats_gui.get_order import GetOrder

def create_sm():
    sm = smach.StateMachine(outcomes=['success','timeout','failure'])

    sm.userdata.person_name = None
    sm.userdata.menu_name = None
    sm.userdata.nav2store = None
    sm.userdata.nav2slope = None
    sm.userdata.nav2person = None

    with sm:

        smach.StateMachine.add('ORDER', GetOrder(),
                               transitions={'success':'ORDER'})
        
        smach.StateMachine.add('PLAN', Plan(),
                               transitions={'success':'Move2Store'})
                                                            
        smach.StateMachine.add('MOVE2Store', Move(nav_point_array = sm.userdata.nav2store),
                                transitions={'success': 'Move2Slope',
                                              'timeout': 'MOVE2Store',
                                              'failure': 'MOVE2Store'})
        
        smach.StateMachine.add('Move2Slope', Move(nav_point_array = sm.userdata.nav2slope),
                                transitions={'success': 'SLOPE',
                                             'timeout': 'Move2Slope',
                                             'failure': 'Move2Slope'})
        
        
        smach.StateMachine.add('SLOPE', VelControl(),
                               transitions={'success': 'MOVE2Person',
                                             'timeout': 'SLOPE',
                                             'failure': 'SLOPE'})
        
        smach.StateMachine.add('MOVE2Person', Move(nav_point_array = sm.userdata.nav2person),
                               transitions={'success': 'FACE',
                                             'timeout': 'MOVE2Person',
                                             'failure': 'MOVE2Person'})
        
        smach.StateMachine.add('FACE', FaceRecog(),
                               transitions={'success': 'success',
                                             'timeout': 'FACE',
                                             'failure': 'FACE'})

        
    return sm

if __name__ == "__main__":
    rospy.init_node('turtle_eats_state_machine_node', anonymous=True)

    sm = create_sm()
    outcome = sm.execute()
    if outcome == 'success':
        rospy.loginfo('I finished the task.')
    else:
        rospy.signal_shutdown('Some error occured.')
