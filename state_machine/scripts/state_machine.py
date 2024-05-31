#!/usr/bin python3

import rospy
import smach
import smach_ros
 
#from turtle_eats_gui.get_order import GetOrder

def create_sm():
    sm = smach.StateMachine(outcomes=['success', 'failure','outcomeA','outcomeB','outcomeC'])

    sm.userdata.menu = []

    with sm:

        smach.StateMachine.add('ORDER', GetOrder(),
                               taransitions={'success':'MOVE',
                                             'timeout':'ORDER',
                                             'failure':'ORDER'})

        smach.StateMachine.add('MOVE', Move(),
                               taransitions={'outcomeA':'STORE',
                                             'outcomeB':'SLOPE',
                                             'outcomeC':'FACE',
                                             'timeout': 'MOVE',
                                             'failure': 'MOVE'})
        
        smach.StateMachine.add('STORE', Store(),
                               taransitions={'success': 'MOVE',
                                             'timeout': 'STORE',
                                             'failure': 'STORE'})
        
        smach.StateMachine.add('SLOPE', Slope(),
                               taransitions={'success': 'MOVE',
                                             'timeout': 'SLOPE',
                                             'failure': 'SLOPE'})
        
        smach.StateMachine.add('FACE', Face(),
                               taransitions={'success': 'EXIT',
                                             'timeout': 'FACE',
                                             'failure': 'FACE'})


        #@smach.cb_interface(outcomes=['success'])
        #def record_start_time(userdata):
        #    return 'success'
        #smach.StateMachine.add('RECORD_START_TIME', smach.CBState(record_start_time),
        #                       transitions={'success':'LISTEN_ORDER'})
        
    return sm

#if __name__ == "__main__";
sm = create_sm()
outcome = sm.execute()
if outcome == 'success':
    rospy.loginfo('I finished the task.')
else:
    rospy.signal_shutdown('Some error occured.')
