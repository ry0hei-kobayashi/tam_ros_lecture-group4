import rospy
import smach
import smach_ros

class Plan(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['success'], input_keys=['person_name', 'menu_name','nav2person', 'nav2store', 'nav2slope'], output_keys=['nav2person', 'nav2store', 'nav2slope'])

    def execute(self, userdata):
        if userdata.person_name == 'hirayae' :
            userdata.nav2person = [1.775, 4.824, 1.419]# x, y, yaw
        elif userdata.person_name == 'kawahara':
            userdata.nav2person = [0.2251, 5.0060, 1.561]# x, y, yaw

        if userdata.menu_name ==  'ChineseFood':
            userdata.nav2store = [2.11, 3.35, 0.943]# x, y, yaw
            userdata.nav2slope = [1.41,0.784,0.193]
        else:
            userdata.nav2store == [0.2415, 2.0024, 1.907]
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

        
