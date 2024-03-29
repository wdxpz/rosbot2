
#!/usr/bin/env python

'''
Copyright (c) 2015, Mark Silliman
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''

# TurtleBot must have minimal.launch & amcl_demo.launch
# running prior to starting this script
# For simulation: launch gazebo world & amcl_demo prior to run this script

import rospy
import tf
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import actionlib
from actionlib_msgs.msg import *
from geometry_msgs.msg import Pose, Point, Quaternion

from init import PoseIniter
from logger import getLogger
logger = getLogger('GoToPose')

position = [(-0.2, 0.0), (0.0, 0.3), (0.1, 0.5), (0.3, 0.7), (0.0, 0.3), (0.0, 0.0)]


class GoToPose():
    def __init__(self):

        self.goal_sent = False
	# What to do if shut down (e.g. Ctrl-C or failure)
        rospy.on_shutdown(self.shutdown)

	# Tell the action client that we want to spin a thread by default
        self.move_base = actionlib.SimpleActionClient("rosbot1/move_base", MoveBaseAction)
        logger.info("Wait for the action server to come up")

	# Allow up to 5 seconds for the action server to come up
        self.move_base.wait_for_server(rospy.Duration(5))

    def goto(self, pos, quat):

        # Send a goal
        ## navigation(x,y) = map(y, -x)
        self.goal_sent = True
        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = 'map'
        goal.target_pose.header.stamp = rospy.Time(0)
        goal.target_pose.pose = Pose(Point(pos[1], -pos[0], 0.000),
                                     Quaternion(quat['r1'], quat['r2'], quat['r3'], quat['r4']))
        logger.info(goal)

	# Start moving
        self.move_base.send_goal(goal)

	# Allow TurtleBot up to 60 seconds to complete task
        success = self.move_base.wait_for_result(rospy.Duration(60))

        state = self.move_base.get_state()
        result = False

        if success and state == GoalStatus.SUCCEEDED:
            # We made it!
            logger.info("arrived!!!") 
            result = True
        else:
            self.move_base.cancel_goal()

        self.goal_sent = False
        return result

    def getMapLocation(self):

        listener = tf.TransformListener()
        try:
            listener.waitForTransform("/map", "rosbot1/base_link", rospy.Time(0), rospy.Duration(10.0))
            trans, rot = listener.lookupTransform("/map", "rosbot1/base_link", rospy.Time(0))
            ##map(x, y) =  trans(-y, x)
            robot_x, robot_y = -trans[1], trans[0]
            logger.info('current position -- x:{}, y:{}'.format(robot_x, robot_y))
        except Exception as e:
            logger.error('getMapLocation Error of robot')
            return


    def shutdown(self):
        if self.goal_sent:
            self.move_base.cancel_goal()
        logger.info("stop goto")
        rospy.sleep(1)

if __name__ == '__main__':
    try:
        rospy.init_node('nav_test', anonymous=False)

        initer = PoseIniter('rosbot1', 0, 0, 0)
        initer.set_pose()

        navigator = GoToPose()

        # Customize the following values so they are appropriate for your location
        #position = {'x': 0.3, 'y' : 1.5}
        quaternion = {'r1' : 0.000, 'r2' : 0.000, 'r3' : 0.000, 'r4' : 1.000}

        for pos in position:
            rospy.loginfo("Go to (%s, %s) pose", pos[0], pos[1])
            success = navigator.goto(pos, quaternion)

            if success:
                rospy.loginfo("Hooray, reached the desired pose")
                navigator.getMapLocation()
            else:
                rospy.loginfo("The base failed to reach the desired pose")

            # Sleep to give the last log messages time to be sent
            rospy.sleep(1)

    except rospy.ROSInterruptException:
        rospy.loginfo("Ctrl-C caught. Quitting")


