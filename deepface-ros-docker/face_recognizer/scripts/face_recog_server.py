#!/usr/bin/env python3
# coding:UTF-8

import math
import numpy as np
import traceback

import tensorflow as tf
print('###########################################')
tf.test.is_gpu_available()
print('###########################################')


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
path_for_faces = rospack.get_path('face_recognizer')+'/io/faces_for_recognition/'
print(path_for_faces)

class FaceRecogServer():


    def __init__(self):

        rospy.init_node('face_recognizer', anonymous=True)
        #debugging for realsense 
        rospy.Subscriber('/camera/color/image_rect_color', Image, self.callback)
#        self.pub = rospy.Publisher('human_coordinates', HumanCoordinatesArray, queue_size=10)
        self.bridge = CvBridge()
        self.path_for_faces = path_for_faces
        self.ids = None
    
    def callback(self, image):

        msg2img = self.bridge.imgmsg_to_cv2(image, "bgr8")
        rospy.loginfo('bf')
        faces = RetinaFace.detect_faces(msg2img)

        if isinstance(faces, dict):
            for key in faces:
                identity = faces[key]
                facial_area = identity["facial_area"]
                x1, y1, x2, y2 = facial_area

                bbox = cv2.rectangle(msg2img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                
                cv2.imshow('RETINA FACERECOGNITION NODE BY RYOHEISOFT', bbox)
                cv2.waitKey(50)

        ##print ('got ',len(),'images')
        #images=[]
        #distances = []
        #Dstoface=[]
        #Angs=[]
        #names=[]

        #for i in range(len(req.in_.image_msgs)):
        #    images.append(bridge.imgmsg_to_cv2(req.in_.image_msgs[i]))
        #for image in images:
        #    print (image.shape)
        #    try:
        #        res=DeepFace.extract_faces(image )
        #        print ('face found h')
        #        dfs = DeepFace.find(image,path_for_faces)
        #        print('id->',dfs[0]['identity'].iloc[1].split('/')[-2])
        #        name=dfs[0]['identity'].iloc[1].split('/')[-2]
        #        names.append(name)
        #    except(ValueError):
        #        print('No Face h')
        #        Ds, Rots=Floats(),Floats()
        #                                ###DEFINITION RESPONSE
        #        strings=Strings()
        #        string_msg= String()
        #        string_msg.data= 'NO_FACE'
        #        strings.ids.append(string_msg)
        #        Dstoface.append(0.0)
        #        Ds.data= Dstoface
        #        Angs.append(0.0)
        #        Rots.data= Angs
        #        return RecognizeFaceResponse(Ds,Rots,strings)
 



        #img2msg = self.bridge.cv2_to_imgmsg(bgr2rgb, encoding="bgr8")
        



#
#
#    def callback(self, data):
#
#        pcl_data = ros_numpy.numpify(data)
#        pcl2img = pcl_data['rgb'].view((np.uint8, 4))[..., [2, 1, 0]]
#        bgr2rgb = cv2.cvtColor(pcl2img, cv2.COLOR_BGR2RGB)
#        people = self.proc_openpose2img(bgr2rgb)
#
#        if people is None:
#            return
#
#        try:
#
#            hca = HumanCoordinatesArray()
#            hca.header.stamp = rospy.Time.now()
#            hca.header.frame_id = data.header.frame_id
#            hca.number_of_people = len(people)
#
#            for person in people:
#                hc = HumanCoordinates()
#
#                for key, key_name in zip(person, PARTS.keys()):
#
#                    pix_x = int(key[0])
#                    pix_y = int(key[1])
#                    score = key[2]
#
#                    #PARTS[key_name]: pix_x, pix_y -> x, y, z, score
#                    PARTS[key_name] = pcl_data[pix_y][pix_x]
#
#                    if not math.isnan(pcl_data[pix_y][pix_x][0]) or not math.isnan(pcl_data[pix_y][pix_x][1]) or not math.isnan(pcl_data[pix_y][pix_x][2] ):
#                        x = pcl_data[pix_y][pix_x][0]
#                        y = pcl_data[pix_y][pix_x][1]
#                        z = pcl_data[pix_y][pix_x][2]
#                        if x > -4.0 and x < 4.0 and y > -1.3 and z > 0.4 and z < 10:
#                            kp = Keypoint()
#                            kp.name = key_name
#                            p = Point()
#                            p.x, p.y, p.z = x, y, z
#                            # kp.coordinate = p
#                            kp.point = p
#                            kp.score = score
#
#                            #hc is a whole body keypoints.
#                            hc.keypoints.append(kp)
#
#
#                            ###for bbox
#                            KEYPOINTS = {}
#                            for i, key in enumerate(PARTS.keys()):
#                                KEYPOINTS[key] = person[i][0], person[i][1], person[i][2]
#
#                            ###bbox###
#                            col_array = []
#                            row_array = []
#                            for i in range(len(person)):
#                               col_array.append(person[i][0]) 
#                               row_array.append(person[i][1]) 
#                            col_array = [i for i in col_array if i != 0]
#                            row_array = [i for i in row_array if i != 0]
#
#                            #hc is a person bbox.
#                            hc.x = int(max(col_array))
#                            hc.w = int(min(col_array))
#                            hc.y = int(max(row_array))
#                            hc.h = int(min(row_array))
#
#                            #print(col_max,col_min,row_max,row_min)
#                            #cv2.rectangle(bgr2rgb,(col_max,row_max),(col_min , row_min), (0,255,0),2)
#                            #img = self.bridge.cv2_to_imgmsg(bgr2rgb, encoding="bgr8")
#                            #self.detected_human_pub.publish(img)                         
#                            #cv2.imshow("WAVINGHAND DETECTED",bgr2rgb)
#                            #cv2.waitKey(50)
#
#                    else:
#                        continue
#
#                #hca has multiple person's keypoints
#                hca.human_coordinates_array.append(hc)
#
#            rospy.loginfo(hca)
#            self.pub.publish(hca)
#            
#        except IndexError:
#            pass
#        except:
#            traceback.print_exc()
#
#
#    def proc_openpose2img(self, image):
#        datum = op.Datum()
#        imageToProcess = image
#        datum.cvInputData = imageToProcess
#        self.opWrapper.emplaceAndPop(op.VectorDatum([datum]))
#        try:
#            cv2.imshow("HUMAN POSE DETECTOR BY RYOHEISOFT", datum.cvOutputData)
#            cv2.waitKey(1)
#
#        except:
#            traceback.print_exc()
#        return datum.poseKeypoints
#
#
if __name__ == '__main__':
   try:
       rospy.logwarn("Start FaceRec Server")
       facerec = FaceRecogServer()
       rate = rospy.Rate(30)

       while not rospy.is_shutdown():
           rate.sleep()
   except rospy.ROSInterruptException:
       pass

