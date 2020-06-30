import rospy
import threading
from robo_nodes.msg import nav2smach
from robo_nodes.msg import cv2smach
from robo_nodes.msg import controls2smach
from robo_nodes.msg import weapons2smach

topic_to_datatype = {'nav2smach':nav2smach, 'cv2smach':cv2smach,
		     'controls2smach':controls2smach, 'weapons2smach':weapons2smach}

class Subscribe_to():
	def __init__(self, topic):
		self.mutex = threading.Lock()
		self.foo = rospy.Subscriber(topic, topic_to_datatype[topic], self.callback)
		self.data = topic_to_datatype[topic]()
		self.data_sent = False

	def callback(self, cb_data):	#Gets data from publisher
		self.mutex.acquire()
		self.data = cb_data
		self.data_sent = True
		self.mutex.release()

	def get_data(self):		#Gives you the most recent data got
		self.mutex.acquire()
		self.final_data = self.data
		self.mutex.release()
		return self.final_data

	def was_data_sent(self):	#Tells you if data was acquired yet
		self.mutex.acquire()
		self.check = self.data_sent
		self.mutex.release()
		return self.check
