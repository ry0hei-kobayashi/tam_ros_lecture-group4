import rospy
from std_msgs.msg import Int64
from cv_bridge import CvBridge
import cv2

def edge_detection(image):
  bridge = CvBridge()
  image = bridge.imgmsg_to_cv2(image, "bgr8")
  image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  result1=0
  result2=0
  for i in range(0, image.shape[0]-2, 3):
    for j in range(0, image.shape[1]-2, 3):
      # print(image[i+1][j+1], image[i+2][j+2])
      # print(image[i+2][j+1], image[i+1][j+2])
      result1 += (-0.005 <image[i][j]-2 * image[i+1][j+1]+image[i+2][j+2] < 0.005)
      result2 += (-0.005 < image[i+2][j]-2 * image[i+1][j+1]+image[i][j+2] < 0.005)
      rospy.loginfo("edge_detection")
      rospy.loginfo(result1 / result2)
  return (result1 / result2)

def sign_detection():
    rospy.init_node('sign_detection', anonymous=True)
    rospy.Subscriber('/camera/color/image_rect_color', image)
    pub = rospy.Publisher("/chatter/Int64", Int64, queue_size=1)
    bridge = CvBridge()
    image = bridge.imgmsg_to_cv2(image, "bgr8")
    image = cv2.resize(image, (160, 90, 3))
    color = [0, 0, 0]
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            color += check_data[i, j, :]
    # 黄色を検知した場合
    if(0.92 < color[3] / color[1] < 1.08 and 1.28 < color[1] / color[0] and 1.28 < color[3] / color[0]):
        if(1. < edge_detection(image)):
            # 上り坂
            rospy.loginfo("found ascent.")
            pub.publish(2)
        if(edge_detection(image) < 1.):
            rospy.loginfo("found descent.")
            rospy.loginfo(3)
            pub.publish(3)
    # 赤を検知した場合
    if(1.3 < color[2] / color[1] and 0.92 <color[1] / color[0] < 1.08 and 1.3 < color[2] / color[0]):
        rospy.loginfo("found stop.")
        pub.publish(1)
if __name__ == '__main__':
    sign_detection()