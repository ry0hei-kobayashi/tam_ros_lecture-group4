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
    sm = smach.StateMachine(outcomes=['success','failure'])

    sm.userdata.person_name = None
    sm.userdata.menu_name = None
    sm.userdata.nav2store =  [0.75,0.78,0.16]
    sm.userdata.nav2slope =  [1.4,0.75,0.19]
    sm.userdata.nav2person = [3.7,-0.46,0.15]

    with sm:

        smach.StateMachine.add('ORDER', GetOrder(),
                               transitions={'success':'PLAN'})
        
        smach.StateMachine.add('PLAN', Plan(),
                               transitions={'success':'Move2Store'})
                                                            
        smach.StateMachine.add('Move2Store', Move(nav_point_array = sm.userdata.nav2store),
                                transitions={'success': 'Move2Slope'})
                                              #'failure': 'Move2Store'})
        
        smach.StateMachine.add('Move2Slope', Move(nav_point_array = sm.userdata.nav2slope),
                                transitions={'success': 'SLOPE'})
                                             #'failure': 'Move2Slope'})
        
        
        smach.StateMachine.add('SLOPE', VelControl(),
                               transitions={'success': 'Move2Person'})
        
        smach.StateMachine.add('Move2Person', Move(nav_point_array = sm.userdata.nav2person),
                               transitions={'success': 'FACE'})
                                             #'failure': 'Move2Person'})
        
        smach.StateMachine.add('FACE', FaceRecog(),
                               transitions={'success': 'PLAN_2',
                                             'failure': 'FACE'})

        smach.StateMachine.add('PLAN_2', Plan(),
                               transitions={'success':'Move2Store_2'})
                                                            
        smach.StateMachine.add('Move2Store_2', Move(nav_point_array = sm.userdata.nav2store),
                                transitions={'success': 'Move2Slope_2'})
                                              #'failure': 'Move2Store'})
        
        smach.StateMachine.add('Move2Slope_2', Move(nav_point_array = sm.userdata.nav2slope),
                                transitions={'success': 'SLOPE_2'})
                                             #'failure': 'Move2Slope'})
        
        
        smach.StateMachine.add('SLOPE_2', VelControl(),
                               transitions={'success': 'Move2Person_2'})
        
        smach.StateMachine.add('Move2Person_2', Move(nav_point_array = sm.userdata.nav2person),
                               transitions={'success': 'FACE_2'})
                                             #'failure': 'Move2Person'})
        
        smach.StateMachine.add('FACE_2', FaceRecog(),
                               transitions={'success': 'success',
                                             'failure': 'FACE_2'})


        
    return sm

if __name__ == "__main__":
    rospy.init_node('turtle_eats_state_machine_node', anonymous=True)

    sm = create_sm()
    outcome = sm.execute()
    if outcome == 'success':
        rospy.loginfo('I finished the task.')
    else:
        rospy.signal_shutdown('Some error occured.')
