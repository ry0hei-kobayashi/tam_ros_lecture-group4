#!/usr/bin/env python3
# coding:UTF-8

import os
import traceback

from deepface import DeepFace
from retinaface import RetinaFace

import cv2
from cv_bridge import CvBridge

import rospy
#import ros_numpy

from geometry_msgs.msg import Point
from sensor_msgs.msg import PointCloud2, Image

from rospkg import RosPack
rospack = RosPack()
known_face_image_path = rospack.get_path('face_recognizer')+'/io/face_images/known_faces'
detected_face_image_path = rospack.get_path('face_recognizer')+'/io/face_images/detected_faces'
print(known_face_image_path)


class FaceRecogServer():


    def __init__(self):

        rospy.init_node('face_recognizer', anonymous=True)

        #debugging for realsense 
        rospy.Subscriber('/camera/color/image_rect_color', Image, self.callback)

        self.bridge = CvBridge()
    
    def callback(self, image):

        #try:
        msg2img = self.bridge.imgmsg_to_cv2(image, "bgr8")
        faces = RetinaFace.detect_faces(msg2img)

        if isinstance(faces, dict):

            #face detection using with retinaface
            for key in faces:
                identity = faces[key]
                facial_area = identity["facial_area"]
                x1, y1, x2, y2 = facial_area

                bbox = cv2.rectangle(msg2img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                crop_face = bbox[y1:y2, x1:x2]
                

                #save tmp image for matching
                temp_face_path = os.path.join(detected_face_image_path, 'temp_face.jpg')
                cv2.imwrite(temp_face_path, crop_face)

                if not os.path.exists(temp_face_path):
                    print(f"Error: Temporary face image was not saved at {temp_face_path}")
                    continue


                try:
                    test_img = cv2.imread(temp_face_path)
                    if test_img is None:
                        print(f"Error: Could not read the saved temporary face image at {temp_face_path}")
                        continue
                except Exception as e:
                        continue

                
                #face recognition using with deepface
                known_face_detected = False
                for file in os.listdir(known_face_image_path):
                    known_face_path = os.path.join(known_face_image_path, file)
                    if os.path.isfile(known_face_path) and file.lower().endswith(('jpg', 'jpeg', 'png')):
                        
                        try:
                            #face recognition
                            recog = DeepFace.find(
                              img_path = temp_face_path,
                              db_path = known_face_image_path, 
                              model_name = 'DeepFace',
                              enforce_detection=False
                            )
                            if recog:
                                known_face_detect = True
                                match_ = file
                                rospy.loginfo(f"match found with {file}")
                                break

                            else:
                                rospy.loginfo(f"No match found")

                        except Exception as e:
                            print(f"Error processing {file}: {e}")
                            known_face_detect = False
                            import traceback
                            traceback.print_exc()

                match_file, _ = os.path.splitext(file)
                with_label = cv2.putText(bbox, match_file, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                cv2.imshow('FACE RECOGNITION NODE BY RYOHEISOFT', with_label)
                cv2.imshow('DETECTED FACE', crop_face)
                cv2.waitKey(50)

            if os.path.exists(temp_face_path):
                os.remove(temp_face_path)

if __name__ == '__main__':
   try:
       rospy.logwarn("Start FaceRec Server")
       facerec = FaceRecogServer()
       rate = rospy.Rate(30)

       while not rospy.is_shutdown():
           rate.sleep()
   except rospy.ROSInterruptException:
       pass

