#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import rospy
import smach
import smach_ros


from geometry_msgs.msg import Twist
from sensor_msgs.msg import Imu

#x = 0.05
#velocity = Twist()
#velocity.linear.x = x
#pub.publish(velocity)
#rospy.Rate(10).sleep()

class VelControl(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['success'])
        self.sub = rospy.Subscriber('/imu', Imu, self.callback)
        self.pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.x = 0.05
        self.alpha = 0.0
        self.Rate = rospy.Rate(10)
        self.success_threshold = 2.5

    def callback(self, data):
        self.alpha = data.linear_acceleration.x

    def execute(self, userdata):
        
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

            if abs(self.alpha) >= self.success_threshold:
                return 'success'
    
if __name__ == '__main__':
    rospy.init_node('turtlebot_controller', anonymous=True)

    sm = smach.StateMachine(outcomes=['success'])

    with sm:
        smach.StateMachine.add('DEBUG', VelControl(),
                            transitions = {'success': 'DEBUG'})
    outcome = sm.execute()
    rospy.spin()





