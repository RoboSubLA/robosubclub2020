'''Comms is in charge of connecting the publishers and subscribers
data packages and method usage can be changed here without affecting the overall project to a
major extent'''

import rospy
import threading
from csula_robosub_2020.msg import cv_objects, nav_imu, nav_barometer

#dictionary detailing the various custom msgs and their key
type_list = {'cv_objects':cv_objects, 'nav_barometer':nav_barometer, 'nav_imu':nav_imu}

#all subscribers will return the most recent object of the assosciated type upon construction
class Subscriber():
    def __init__(self, topic):

        self.sub = rospy.Subscriber(topic, type_list[topic], self.callback)
        self.mutex = threading.Lock()

        self.data = None

    def callback(self, data):
        self.mutex.acquire()
        self.data = data
        self.mutex.release()

    def get_data(self):
        return self.object_data


class Publisher():
    def __init__(self, topic):
        self.pub = rospy.Publisher(topic, type_list[topic], queue_size=1)
        pub_type = {'cv_objects':self.cv_object_pub, 'nav_barometer':self.nav_barometer_pub, 'nav_imu': self.nav_imu_pub}
        self.publish = pub_type[data_type]

    def cv_object_pub(self, gate=False, dice=False):
        self.data.gate = gate
        self.data.dice = dice

    def nav_imu_pub(self, var1=0, var2=0):
        self.data.var1 = var1
        self.data.var2 = var2

    def nav_barometer(self, depth):
        self.data.depth = depth