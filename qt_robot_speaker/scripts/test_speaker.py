#!/usr/bin/env python

import os
import rospy
import sys
import pyaudio
import wave
import struct
import json
import time
import random
import numpy as np
from std_msgs.msg import String
from audio_common_msgs.msg import AudioData
from qt_robot_speaker.srv import PlayAudio, PlayAudioRequest
#import soundfile as sf


WAV_HEADER_LENGTH = 24

class AudioData(object):
   		 def __init__(self, data):
		 	self.data = data

class Test():
	def __init__(self, pi, nuc):
		self.pi_topic = pi
		self.nuc_topic = nuc
		rospy.init_node("speaker_node", anonymous=True)
		rospy.wait_for_service('speaker_output')
		self.speaker_output_client = rospy.ServiceProxy('speaker_output', PlayAudio)	
		self.handle_tts_realtime()	
		
		rospy.spin()
	
	def handle_speaker_state(self, req):
		print(req.data)
		return
	
	
	
	def handle_tts_realtime(self):
		outdir = os.path.dirname(os.path.realpath(__file__))
		phraseID = "1"
		#data, samplerate = sf.read(outdir + '/'+phraseID+'.ogg')
		#sf.write(outdir + '/'+phraseID+'.wav', data, samplerate)
		samplerate = 22050
		file_handle =outdir + '/'+phraseID+'.wav'
		data = np.fromfile(file_handle, np.uint8)[WAV_HEADER_LENGTH:] #Loading wav file
		data_array = data.astype(np.uint8).tostring()
		audio_frame = int(np.int64(samplerate)) 
		response = self.speaker_output_client(audio_frame, data_array)
		print(response.speaker_state)
		

if __name__ == '__main__':
	pi =  "qt_robot"
	nuc = "qtpc"
    	Test(pi, nuc)
