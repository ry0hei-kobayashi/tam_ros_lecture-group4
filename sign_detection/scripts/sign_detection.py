import rospy
from PIL import Image
import numpy as np
from std_msgs.msg import Int64

def edge_detection(image):
  image = Image.fromarray(image)
  image = image.convert('L')
  image = np.array(image)
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

def sign_detection(image):
     rospy.init_node('sign_detection', anonymous=True)
     pub = rospy.Publisher("/chatter/Int64", Int64, queue_size=1)
    # imageをnumpy配列に変更?
    image = image.resize((160, 90, 4))
    color = [0, 0, 0]
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            color += check_data[i, j, :]
    # 黄色を検知した場合
    if(0.92 < color[0] / color[1] < 1.08 and 1.28 < color[1] / color[2] and 1.28 < color[0] / color[2]):
        if(1. < edge_detection(image)):
            # 上り坂
            rospy.loginfo("found ascent.")
            pub.publish(2)
        if(edge_detection(image) < 1.):
            rospy.loginfo("found descent.")
            rospy.loginfo(3)
            pub.publish(3)
    # 赤を検知した場合
    if(1.3 < color[0] / color[1] and 0.92 <color[1] / color[2] < 1.08 and 1.3 < color[0] / color[2]):
        rospy.loginfo("found stop.")
        pub.publish(1)
if __name__ == '__main__':
    sign_detection()