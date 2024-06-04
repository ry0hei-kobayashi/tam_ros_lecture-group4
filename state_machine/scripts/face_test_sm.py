#!/usr/bin python3

import rospy
import smach
import smach_ros
 
#from turtle_eats_gui.get_order import GetOrder
from turtle_eats_gui.get_order import GetOrder

def create_sm():
    sm = smach.StateMachine(outcomes=['success', 'failure','outcomeA','outcomeB','outcomeC'])

    sm.userdata.person_name = None
    sm.userdata.menu_name = None

    with sm:

        smach.StateMachine.add('ORDER', GetOrder(),
                               taransitions={'success':'FACE',
                                             'timeout':'ORDER',
                                             'failure':'ORDER'})

        @smach.cb_interface(outcomes=['success'])
        def move_select(userdata):
            print(sm.userdata_menu_name)
            print(sm.userdata_person_name)
            #if store1 or 2

            return 'success'
        #smach.StateMachine.add('MOVESELECT', smach.CBState(move_select),
        #                       transitions={'success':'ORDER'})

        #smach.StateMachine.add('MOVE', Move(1,1,0.15),
        #                       taransitions={'outcomeA':'STORE',
        #                                     'outcomeB':'SLOPE',
        #                                     'outcomeC':'FACE',
        #                                     'timeout': 'MOVE',
        #                                     'failure': 'MOVE'})
        #

        #smach.StateMachine.add('MOVE', Move(2,3,0.15),
        #                       taransitions={'outcomeA':'STORE',
        #                                     'outcomeB':'SLOPE',
        #                                     'outcomeC':'FACE',
        #                                     'timeout': 'MOVE',
        #                                     'failure': 'MOVE'})
        #

        #smach.StateMachine.add('STORE', Store(),
        #                       taransitions={'success': 'MOVE',
        #                                     'timeout': 'STORE',
        #                                     'failure': 'STORE'})
        #
        #smach.StateMachine.add('SLOPE', Slope(),
        #                       taransitions={'success': 'MOVE',
        #                                     'timeout': 'SLOPE',
        #                                     'failure': 'SLOPE'})
        #
        smach.StateMachine.add('FACE', FaceRecog(),
                               taransitions={'success': 'EXIT',
                                             'failure': 'FACE'})

        #smach.StateMachine.add('FINISH', ,
        #                       taransitions={'success': 'success'})

        
    return sm

#if __name__ == "__main__";
sm = create_sm()
outcome = sm.execute()
if outcome == 'success':
    rospy.loginfo('I finished the task.')
else:
    rospy.signal_shutdown('Some error occured.')
