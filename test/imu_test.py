#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Imu

def imu_callback(data):
    linear_acceleration = data.linear_acceleration
    acceleration_x = linear_acceleration.x
    acceleration_y = linear_acceleration.y
    acceleration_z = linear_acceleration.z

    rospy.loginfo("Acceleration (m/s^2): x=%f, y=%f, z=%f", acceleration_x, acceleration_y, acceleration_z)

def imu_listener():
    rospy.init_node('imu_test', anonymous=True)
    rospy.Subscriber("/imu/data_raw", Imu, imu_callback)

    rospy.spin()

if __name__ == '__main__':
    imu_listener()

