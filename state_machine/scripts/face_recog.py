#!/usr/bin/env python3.9
# -*-encoding:utf-8-*-

#depends
#sudo apt install python3.9-dev
#python3.9 -m pip install scikit-learn==1.5.0
#python3.9 -m pip install opencv-python
#python3.9 -m pip install Pillow==10.3.0
#python3.9 -m pip install dlib==19.9.0
#python3.9 -m pip install face-recognition

import rospy
import smach
import smach_ros
from sensor_msgs.msg import Image

import cv2
from cv_bridge import CvBridge

import face_recognition

from sklearn import svm
import os
import pickle

print('load trained model')
with open('/home/roboworks/roslec_ws/src/tam_ros_lecture-group4/face_recog/model.pickle', mode='rb') as f:
    clf = pickle.load(f)

class FaceRecog(smach.State):

    def __init__(self):
        smach.State.__init__(self, outcomes=['success'], input_keys=['person_name', 'menu_name'])

        self.bridge = CvBridge()


    def execute(self, userdata):


        img_msg  = rospy.wait_for_message('/camera/rgb/image_raw', Image, timeout=None )
        cv_image = self.bridge.imgmsg_to_cv2(img_msg, "bgr8")
        rgb_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)

        #test_image = face_recognition.load_image_file(cv_image)
        
        face_locations = face_recognition.face_locations(rgb_image)
        no = len(face_locations)
        print("Number of faces detected: ", no)
        if no > 0 :
            print("Found:")

        for i in range(no):
            test_image_enc = face_recognition.face_encodings(rgb_image, known_face_locations=face_locations)[i]
            name = clf.predict([test_image_enc])
            print(*name)
        
        if userdata.person_name == name:
            return "success"
        else:
            return "failure"


if __name__=='__main__':
    rospy.init_node('face_recog', anonymous=True)

    sm = smach.StateMachine(outcomes=['success'])
    
    with sm:
        smach.StateMachine.add('DEBUG', FaceRecog(),
                               transitions = {'success': 'DEBUG'})
    sm.execute()
    rospy.spin()

        
        

        
