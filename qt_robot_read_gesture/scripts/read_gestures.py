#!/usr/bin/env python

import rospy
from std_msgs.msg import String
import numpy as np
import sys
import os
import xml.etree.ElementTree as ET

class ReadGestures:

    def __init__(self, pi, nuc):
        self.pi_topic = pi
	self.nuc_topic = nuc
	self.gestures_duration = []
	self.gestures_name = []
        rospy.init_node("read_gestures_node")
        self.qt_gestures_pub = rospy.Publisher('/qt_robot/gestures/list', String, queue_size=10)
	rospy.Timer(rospy.Duration(0.5), self.read_gestures)
	rospy.spin()

    def get_files(self, dirName):
    	# create a list of file and sub directories 
    	# names in the given directory 
    	listOfFile = os.listdir(dirName)
    	allFiles = list()
    	# Iterate over all the entries
    	for entry in listOfFile:
        	# Create full path
        	fullPath = os.path.join(dirName, entry)
        	# If entry is a directory then get the list of files in this directory 
        	if os.path.isdir(fullPath):
            		allFiles = allFiles + self.get_files(fullPath)
        	else:
            		allFiles.append(fullPath)            
    	return allFiles  


    def read_gestures(self, timer):
        path = '/home/qtrobot/robot/data/gestures'
	all_files = self.get_files(path)
	gesture_list = []
        for filename in all_files:
            if not filename.endswith('.xml'): continue
            fullname = filename
            tree = ET.parse(fullname)
            root = tree.getroot()
            for child in root:
                if child.tag == 'duration':
                    self.gestures_duration.append(child.text)
                elif child.tag == 'name':
                    self.gestures_name.append(child.text)    
	for index, el in enumerate(self.gestures_name):
		gesture_list.append({'name': str(el), 'duration': self.gestures_duration[index] })
	self.qt_gestures_pub.publish(str(gesture_list))


if __name__ == '__main__':
	pi = "qt_robot"
	nuc = "qtpc"
    	ReadGestures(pi, nuc)

