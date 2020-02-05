#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from std_msgs.msg import Bool
from qt_robot_speaker.srv import PlayAudio, PlayAudioResponse
from qt_robot_speaker.msg import PlayRequest
import pyaudio
import numpy as np
import sys
import time
import ast

class SpeakerOutput:

    def __init__(self):
        rospy.init_node("speaker_node")
	#speaker_service = rospy.Service('speaker_output', PlayAudio, self.handle_play)
	self.speak_sub = rospy.Subscriber("/cordial/speaker/playing", PlayRequest, self.handle_play, queue_size=1)
	self.speak_pub = rospy.Publisher("/cordial/speaker/done", Bool, queue_size=1)        
	self.output_device_index = None
        self.get_output_device_index()
	rospy.spin()
      

    def handle_play(self, req):
	print('Pi Received request')
        data = req.data
	audio_rate = req.audio_frame
	#print(audio_rate)
        p = pyaudio.PyAudio()
        audio_format = pyaudio.paInt16
        chunk_size = 512
        self.stream = p.open(format=audio_format,
                        channels=1,
                        rate=audio_rate,
                        input=False,
                        output=True,
                        output_device_index=self.output_device_index,
                        frames_per_buffer=chunk_size)
	self.stream.write(data)	
	time.sleep(1)
	self.stream.stop_stream()
	self.stream.close()
	speaker_state = True
	self.speak_pub.publish(speaker_state)
	

    def get_output_device_index(self):
        """ Finds the audio device named 'play' configured in ~/.asoundrc.
            If this device is not found, returns None and pyaudio will use
            your machines default device
        """
        p = pyaudio.PyAudio()
        rospy.loginfo("Pi Attempting to find device named 'QTSpeaker'")
        for i in range(p.get_device_count()):
            device = p.get_device_info_by_index(i)
	    print(device['name'])
            if device['name'] == 'sysdefault':
                self.output_device_index = i
                return


if __name__ == '__main__':
    	SpeakerOutput()

