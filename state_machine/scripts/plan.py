import rospy
import smach
import smach_ros

class Plan(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['success'], input_keys=['person_name', 'menu_name','nav2person', 'nav2store', 'nav2slope'], output_keys=['nav2person', 'nav2store', 'nav2slope'])

    def execute(self, userdata):
        if userdata.person_name == 'hirayae' :
            userdata.nav2person = [3.73, -0.462, 0.151]# x, y, yaw
        elif userdata.person_name == 'kawahara':
            userdata.nav2person = [4.19, 1.35, 0.193]# x, y, yaw

        if userdata.menu_name ==  'ChineseFood':
            userdata.nav2store = [0.752, 0.785, 0.169]# x, y, yaw
            userdata.nav2slope = [1.41,0.784,0.193]
        elif userdata.menu_name == 'ItalianFood':
            userdata.nav2store == [1, 1, 1]
            userdata.nav2slope = [1,1,1]

        return "success"


if __name__ == '__main__':
    rospy.init_node('plan', anonymous=True)
    sm = smach.StateMachine(outcomes=['success'])
    sm.userdata.person_name = 'hirayae'
    sm.userdata.menu_name = 'ChineseFood'
    with sm:
        smach.StateMachine.add('DEBUG', Plan(),
                transitions = {'success': 'success'})
    sm.execute()
    rospy.spin()

        
