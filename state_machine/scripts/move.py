#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import actionlib
from actionlib_msgs.msg import GoalStatus
#Messages related to coordinates and angle of rotation
from geometry_msgs.msg import Point, PoseStamped, Quaternion
#Messages related to move_base
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import rospy
import smach.state
import tf.transformations

import smach
import smach_ros

class Move(smach.State):
    def __init__(self, nav_point_array=[0,0,0]):
        rospy.loginfo('start move') 
        #move_base client declaration
        self.cli = actionlib.SimpleActionClient('/move_base', MoveBaseAction)
        #self.goal_point = nav_point_array[0], nav_point_array[1], nav_point_array[2]
        
        smach.State.__init__(self,
                             outcomes=['success'],
                             input_keys=['nav2person','nav2store','nav2slope','seq'],
                             output_keys=['nav2person','nav2store','nav2slope','seq'])


    def execute(self, userdata):
        action_state = None
        #if not self.cli.wait_for_server(30.0) :
        #    rospy.logwarn("Server timed out!")
        #    return 'timeout'

        #timeout_time = rospy.Time.now() + rospy.Duration(30.0)
        

        rospy.loginfo('Executing state MOVE')


        if userdata.seq == 0:
            self.goal_point = userdata.nav2store
            userdata.seq = 1
        elif userdata.seq == 1:
            self.goal_point = userdata.nav2person
            userdata.seq = 0

        rospy.loginfo(f'goal point:{self.goal_point}')
        rospy.sleep(3)

        pose = PoseStamped()
        pose.header.stamp = rospy.Time.now()
        #Declaration of the reference frame
        pose.header.frame_id = "map"
        #Declaration of coordinates of target point
        pose.pose.position = Point(self.goal_point[0], self.goal_point[1], 0)
        #Declaration of orientation when arriving to the target point
        quat = tf.transformations.quaternion_from_euler(0, 0, self.goal_point[2])
        pose.pose.orientation = Quaternion(*quat)
        #Declaration of class for move base target value
        goal = MoveBaseGoal()
        goal.target_pose = pose
        rospy.loginfo(goal)

        #while not rospy.is_shutdown():
        
        #while not self.cli.wait_for_result(rospy.Duration(1.0)):
        self.cli.send_goal(goal)
        self.cli.wait_for_result()
        # self.cli.wait_for_result()

            # Force return if timeout occurs
            #if rospy.Time.now() > timeout_time:
            #    rospy.logwarn("Excuse method timed out!")
            #    return 'timeout'

        action_state = self.cli.get_state()
        
        if action_state == GoalStatus.SUCCEEDED:
            rospy.loginfo("Navigation Succeeded.")
        return 'success'
        





if __name__ == '__main__':
    rospy.init_node('move_to_goal', anonymous=True)
    sm = smach.StateMachine(outcomes=['success','failure', 'timeout'])
    sm.userdata.person_name = 'hirayae'
    sm.userdata.menu_name = 'ChineseFood'
    sm.userdata.nav2person = [1,0.5,0]
    with sm:
        smach.StateMachine.add('DEBUG', Move(nav_point_array = sm.userdata.nav2person),
                transitions = {'success': 'success',
                                'failure': 'failure'})
    sm.execute()
    rospy.spin()
