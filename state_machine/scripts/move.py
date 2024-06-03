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


class Move(smach.state):

    def __init__(self):
        rospy.init_node('navigation_sample')
        #move_base client declaration
        self.cli = actionlib.SimpleActionClient('/move_base', MoveBaseAction)

        smach.State.__init__(self,
                             outcomes=['outcomeA', 'outcomeB', 'outcomeC', 'timeout', 'failere'],
                             input_keys=['goal_x', 'goal_y', 'goal_yaw', 'goal_place_in'],
                             output_keys=['goal_place_out'])


    def excuse(self, userdata):
        if not self.cli.wait_for_server(20.0) :
            rospy.logwarn("Server timed out!")
            userdata.goal_place_out = userdata.goal_place_in
            return 'timeout'

        timeout_time = rospy.Time.now() + rospy.Duration(30.0)

        rospy.loginfo('Executing state MOVE')
        rospy.sleep(3)

        pose = PoseStamped()
        pose.header.stamp = rospy.Time.now()
        #Declaration of the reference frame
        pose.header.frame_id = "map"
        #Declaration of coordinates of target point
        pose.pose.position = Point(userdata.goal_x, userdata.goal_y, 0)
        #Declaration of orientation when arriving to the target point
        quat = tf.transformations.quaternion_from_euler(0, 0, userdata.goal_yaw)
        pose.pose.orientation = Quaternion(*quat)
        #Declaration of class for move base target value
        goal = MoveBaseGoal()
        goal.target_pose = pose

        self.cli.send_goal(goal)
        # self.cli.wait_for_result()

        while not self.cli.wait_for_result(rospy.Duration(1.0)):
            # Force return if timeout occurs
            if rospy.Time.now() > timeout_time:
                rospy.logwarn("Excuse method timed out!")
                return 'timeout'

        action_state = self.cli.get_state()
        
        if action_state == GoalStatus.SUCCEEDED:
            rospy.loginfo("Navigation Succeeded.")
            if userdata.goal_place_in == 'STORE':
                return 'outcomeA'
            elif userdata.goal_place_in == 'SLOPE':
                return 'outcomeB'
            elif userdata.goal_place_in == 'FACE':
                return 'outcomeC'
            else:
                rospy.loginfo("Where is goal?")
                exit

        else:
            userdata.goal_place_out = userdata.goal_place_in
            return 'failere'


# remapping={'goal_x' :'pose_x',
#            'goal_y' : 'pose_y',
#            'goal_yaw': 'pose_yaw',
#            'goal_place_in' : 'nexr_place',
#            'goal_place_out' : 'next_place'}

