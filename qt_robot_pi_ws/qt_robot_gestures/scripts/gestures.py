#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from qt_gesture_controller.srv import *
import numpy as np
import sys


class GesturesManager:

    def __init__(self, pi, nuc):
        self.pi_topic = pi
	self.nuc_topic = nuc
        rospy.init_node("gestures_node")
	rospy.Subscriber(self.pi_topic+"/gestures", String, self.handle_gestures)
        self.motor_act_pub = rospy.Publisher('/qt_robot/gesture/play', String, queue_size=10)
        self.gesture_service = rospy.ServiceProxy('qt_robot/gesture/play', gesture_play)
	rospy.spin()


    def angry(self, speed):
        resp = self.gesture_service("QT/emotions/angry", speed)
        return

    def point_front(self, speed):
        resp = self.gesture_service("QT/point_front", speed)
        return

    def bye_bye(self, speed):
        resp = self.gesture_service("QT/bye-bye", speed)
        return

    def bye(self, speed):
        resp = self.gesture_service("QT/bye", speed)
        return

    def send_kiss(self, speed):
        resp = self.gesture_service("QT/send_kiss", speed)
        return

    def show_QT(self, speed):
        resp = self.gesture_service("QT/show_QT", speed)
        return

    def show_tablet(self, speed):
        resp = self.gesture_service("QT/show_tablet", speed)
        return

    def yawn(self, speed):
        resp = self.gesture_service("QT/yawn", speed)
        return

    def afraid(self, speed):
        resp = self.gesture_service("QT/emotions/afraid", speed)
        return

    def calm(self, speed):
        resp = self.gesture_service("QT/emotions/calm ", speed)
        return

    def disgusted(self, speed):
        resp = self.gesture_service("QT/emotions/disgusted", speed)
        return

    def happy(self, speed):
        resp = self.gesture_service("QT/emotions/happy", speed)
        return

    def hoora(self, speed):
        resp = self.gesture_service("QT/emotions/hoora", speed)
        return
    

    def sad(self, speed):
        resp = self.gesture_service("QT/emotions/sad", speed)
        return

    def shy(self, speed):
        resp = self.gesture_service("QT/emotions/shy", speed)
        return

    def surprised(self, speed):
        resp = self.gesture_service("QT/emotions/surprised", speed)
        return


    def gesture_to_act(self, argument, speed):
        switcher = {
        "angry": self.angry(speed),
        "point_front": self.point_front(speed),
        "byebye": self.bye_bye(speed),
        "bye": self.bye(speed),
        "kiss": self.send_kiss(speed),
        "QT": self.show_QT(speed),
        "tablet": self.show_tablet(speed),
        "yawn": self.yawn(speed),
        "afraid": self.afraid(speed),
        "calm": self.calm(speed),
        "disgusted": self.disgusted(speed),
        "happy": self.happy(speed),
        "hoora": self.hoora(speed),
        "sad": self.sad(speed),
        "shy": self.shy(speed),
        "surprised": self.surprised(speed)
        }
        gesture_act = switcher.get(argument, lambda: "Invalid gestures")

    def handle_gestures(self, req):
        rospy.loginfo("Gesture to be acted is: " + req.data)
        gesture = req.data
        speed = 1
        self.gesture_to_act(gesture, speed)
        return


if __name__ == '__main__':
	pi = "qt_robot"
	nuc = "qtpc"
    	GesturesManager(pi, nuc)

