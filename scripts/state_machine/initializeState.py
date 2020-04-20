#!/usr/bin/env python
import roslib
import rospy
import smach
import smach_ros
import time
from robo_nodes.msg import nav2smach
from robo_nodes.msg import cv2smach
from robo_nodes.msg import controls2smach
from robo_nodes.msg import weapons2smach
from Subscriber import Subscribe_to

class Initialize(smach.State):
	def __init__(self):
		print("starting")
		smach.State.__init__(self, outcomes=['Finished', 'Failed'])
		#Subscribe to all nodes that publish to smach
		self.nav_sub = Subscribe_to('nav2smach')
		self.cv_sub = Subscribe_to('cv2smach')
		self.controls_sub = Subscribe_to('controls2smach')
		self.weapons_sub = Subscribe_to('weapons2smach')
		self.counter = 0
		time.sleep(2)

	def execute(self, userdata):
		#Check if all nodes have published data
		nav_data_sent = self.nav_sub.was_data_sent()
		cv_data_sent = self.cv_sub.was_data_sent()
		controls_data_sent = self.controls_sub.was_data_sent()
		weapons_data_sent = self.weapons_sub.was_data_sent()

		print (nav_data_sent, cv_data_sent, controls_data_sent, weapons_data_sent)
		#If any of the nodes are not publishing, stay in this loop
		while ((nav_data_sent == False) or (cv_data_sent == False) or
			       (controls_data_sent == False) or (weapons_data_sent == False)):

			time.sleep(0.01)
			#Continue checking if all nodes have published data
			nav_data_sent = self.nav_sub.was_data_sent()
			cv_data_sent = self.cv_sub.was_data_sent()
			controls_data_sent = self.controls_sub.was_data_sent()
			weapons_data_sent = self.weapons_sub.was_data_sent()
			print (nav_data_sent, cv_data_sent, controls_data_sent, weapons_data_sent)
			#If any nodes have failed to publish after ~10 seconds, return Failed
			if (self.counter > 1000):
				return 'Failed'
			self.counter = self.counter + 1

		#When all nodes are publishing data, return Finished
		return 'Finished'

def code():
	rospy.init_node('sm')
	main = smach.StateMachine(outcomes=['Done', 'Not_Done'])
	with main:
		smach.StateMachine.add('Initialize', Initialize(), transitions={ 'Finished':'Done',
										'Failed':'Not_Done'})

	sis = smach_ros.IntrospectionServer('server', main, '/tester')
	sis.start()
	outcome = main.execute()
	sis.stop()
	rospy.spin()
	#sis.stop()

if __name__ == '__main__':
	code()


