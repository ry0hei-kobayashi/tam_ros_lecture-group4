import rospy
import smach
import smach_ros

class Plan(smach.state):
    def __init__(self):
        smach.State.__init__(self, outcomes=['success'], input_keys=['p_name', 'm_name'],
                                                        output_keys=['nav2person', 'nav2store'])
    def execute(self, userdata):
        if person_name == 'abc' and menu_name == 'Japanesefoof':
            userdata.nav2person = 1, 1, 1 # x, y, yaw
            userdata.nav2store = 1, 1, 1 # x, y, yaw

            return success

if __name__ == '__main__':
    rospy.init_node('plan', anonymous=True)
    sm = smach.StateMachine(outcomes=['success'])
    with sm:
        smach.StateMachine.add('DEBUG', Plan(),
                               transitions = {'success': 'DEBUG'})
    sm.execute()
    rospy.spin()

        