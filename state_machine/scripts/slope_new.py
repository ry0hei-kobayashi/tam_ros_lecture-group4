#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import rospy
import smach
import smach_ros


from geometry_msgs.msg import Twist
from sensor_msgs.msg import Imu

import tf


class Slope(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['success'])
        self.sub = rospy.Subscriber('/imu', Imu, self.callback)
        self.pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.x = 0.05
        self.alpha = 0.0
        self.Rate = rospy.Rate(10)
        #self.success_threshold = 2.5#消す
        self.flat = 0
        
        self.success_pos = 3.45#(終了座標,xのみでいいかも)
        self.ang = 0.0#(坂の向き)
        
        

    def callback(self, data):
        self.alpha = data.linear_acceleration.x

    def execute(self, userdata):
        #if userdata.slope_enable_flag == True:
        	#坂へ向き調整
        	'''
        	tfl = tf.TransformListener()
        	try:
            	(trans, rot) = tfl.lookupTransform('map', 'base_link', rospy.Time(0))
            except:
            	continue
            euler = tf.transformations.euler_from_quaternion(rot)
            rospy.loginfo('[' + rospy.get_name() + ']:\nx: ' + str(trans[0]) + '\ny: ' + str(trans[1]) + '\nyaw: ' + str(euler[2]))
            
        	#角度調整
            velocity = Twist()
            velocity.angular.z = self.ang - euler[2]#まっすぐにする
            self.pub.publish(velocity)
        	rospy.sleep(1)
        	velocity.angular.z = 0.0
            self.pub.publish(velocity)
        	'''
        	
        while not rospy.is_shutdown():
            velocity = Twist()
            if abs(self.alpha) > 0.7:
                velocity.linear.x = self.x - (self.alpha * 0.01)
                self.x = velocity.linear.x
            else:
                velocity.linear.x = self.x

            rospy.loginfo(self.alpha)
            rospy.loginfo(self.x)
            self.pub.publish(velocity)
            self.Rate.sleep()

            '''
            if abs(self.alpha) >= self.success_threshold: #坂終わり座標ならreturnに書き換え
                return 'success'
            
            '''
            try:
                (trans, rot) = tfl.lookupTransform('map', 'base_link', rospy.Time(0))
            except:
                continue
            euler = tf.transformations.euler_from_quaternion(rot)
            rospy.loginfo('[' + rospy.get_name() + ']:\nx: ' + str(trans[0]) + '\ny: ' + str(trans[1]) + '\nyaw: ' + str(euler[2]))
                
            if trans[0] >= self.success_pos: #坂終わり座標を超えたならreturn
                return 'success'
                
                #else:
                        #return 'success'


if __name__ == '__main__':
    rospy.init_node('turtlebot_controller', anonymous=True)

    sm = smach.StateMachine(outcomes=['success'])

    with sm:
        smach.StateMachine.add('DEBUG', VelControl(),
                            transitions = {'success': 'DEBUG'})
    outcome = sm.execute()
    rospy.spin()
