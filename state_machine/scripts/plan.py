import rospy
import smach
import smach_ros

class Plan(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['success'], input_keys=['person_name', 'menu_name'], output_keys=['nav2person', 'nav2store'])

    def execute(self, userdata):
        if userdata.person_name == 'hirayae' and userdata.menu_name == 'ChineseFood':
            rospy.loginfo('plan')
            userdata.nav2person = [1, 1, 1 ]# x, y, yaw
            userdata.nav2store = [1, 1, 1 ]# x, y, yaw
            userdata.nav2slope = [1, 1, 1 ]# x, y, yaw

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

        
