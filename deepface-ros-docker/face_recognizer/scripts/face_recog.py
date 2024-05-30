#!/usr/bin/env python3
# coding:UTF-8

import os
import traceback

from deepface import DeepFace
from retinaface import RetinaFace
import face_recognition

import cv2
from cv_bridge import CvBridge
import numpy as np

import rospy
#import ros_numpy

from geometry_msgs.msg import Point
from sensor_msgs.msg import PointCloud2, Image

from rospkg import RosPack
rospack = RosPack()
known_face_image_path = rospack.get_path('face_recognizer')+'/io/face_images/known_faces'
detected_face_image_path = rospack.get_path('face_recognizer')+'/io/face_images/detected_faces'
print(known_face_image_path)

koba_image = face_recognition.load_image_file("kobayashi.png")
koba_face_encoding = face_recognition.face_encodings(koba_image)[0]

hira_image = face_recognition.load_image_file("hirayae.png")
hira_face_encoding = face_recognition.face_encodings(hira_image)[0]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

known_face_encodings = [
    koba_face_encoding,
    hira_face_encoding
]
known_face_names = [
    "kobayashi",
    "hirayae"
]

class FaceRecogServer():


    def __init__(self):

        rospy.init_node('face_recognizer', anonymous=True)

        #debugging for realsense 
        rospy.Subscriber('/camera/color/image_rect_color', Image, self.callback)

        self.bridge = CvBridge()
    
    def callback(self, image):

        #try:
        msg2img = self.bridge.imgmsg_to_cv2(image, "bgr8")
        #faces = RetinaFace.detect_faces(msg2img)

        if process_this_frame:
            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(msg2img, (0, 0), fx=0.25, fy=0.25)

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]
            
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                # # If a match was found in known_face_encodings, just use the first one.
                # if True in matches:
                #     first_match_index = matches.index(True)
                #     name = known_face_names[first_match_index]

                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

                face_names.append(name)

        process_this_frame = not process_this_frame


        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(msg2img, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        cv2.imshow('show_image' , msg2img)


if __name__ == '__main__':
   try:
       rospy.logwarn("Start FaceRec Server")
       facerec = FaceRecogServer()
       rate = rospy.Rate(30)

       while not rospy.is_shutdown():
           rate.sleep()
   except rospy.ROSInterruptException:
       pass


# This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# other example, but it includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

# Get a reference to webcam #0 (the default one)


# Create arrays of known face encodings and their names
