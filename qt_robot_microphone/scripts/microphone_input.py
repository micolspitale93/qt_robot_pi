#!/usr/bin/env python

import rospy
from audio_common_msgs.msg import AudioData
from std_msgs.msg import String
from std_msgs.msg import Bool
import pyaudio
import audioop
import numpy as np
import math
from collections import deque
import sys


class VoiceInput:
    p = pyaudio.PyAudio()
    audio_format = pyaudio.paInt16
    audio_format_width = 2
    chunk_size = 1024*2
    total_channels = 1
    audio_rate = 16000
    silence_limit_seconds = 1
    previous_audio_seconds = 2
    total_silence_samples = 100
    silence_threshold = 1000
    
    def __init__(self, node_name):
        rospy.init_node(node_name)
        rospy.loginfo("Initializing  %s" % node_name)
        self.node_name = node_name
        self.stream = None
        self.input_device_index = None
        self.output_device_index = None
	self.state = "Start"
        self.audio_publisher = rospy.Publisher("/cordial/microphone/audio", AudioData, queue_size=5)
	self.listening_done_publisher = rospy.Publisher("/cordial/listening/done", Bool, queue_size = 1)
	rospy.Subscriber("/cordial/listening", Bool, self.handle_listening)
	rospy.Subscriber("/cordial/recording/audio", Bool, self.handle_recording)

    def handle_recording(self, req):
	if req.data:
		print("Start Recording")	

    def handle_listening(self,request):
	self.listening = request.data
	if self.listening:
		self.state = "Idle"
		self.started = False
		self.stream.start_stream()
		state = self.state

    def open_stream(self):
        self.close_stream()
        rospy.loginfo("Opening audio input stream")
        self.stream = self.p.open(format=self.audio_format,
                             channels=self.total_channels,
                             rate=self.audio_rate,
                             input=True,
                             input_device_index=self.input_device_index,
                             frames_per_buffer=self.chunk_size)

    def close_stream(self):
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None

    def listen(self):
        self.open_stream()
        rospy.loginfo("%s listening" % self.node_name)
        current_audio = ''
        chunks_per_second = int(self.audio_rate / self.chunk_size)
        sliding_window = deque(maxlen=self.silence_limit_seconds * chunks_per_second)
        prev_audio = deque(maxlen=self.previous_audio_seconds * chunks_per_second)
        self.started = False

        while not rospy.is_shutdown():
	    if not self.stream.is_stopped():
	    	latest_audio_data = self.stream.read(self.chunk_size, exception_on_overflow = False)
	    if not self.state == "Speaking":
	       	    sliding_window.append(math.sqrt(abs(audioop.avg(latest_audio_data, self.audio_format_width))))
		    rospy.loginfo("Lenght of sliding window:" + str(len(sliding_window))) 
		    if any([x > self.silence_threshold for x in sliding_window]):
		        if not self.started :
		            rospy.loginfo("Sound detected... Recording")
			    self.state = "Listening"
			    state = self.state
		            self.started = True
			    # Here just command the QTrobot with specific commands for the Recording Starts
		        current_audio += latest_audio_data
		    elif self.started:
		        rospy.loginfo("Finished")
			self.state = "Speaking"
			state = self.state
		        all_audio_data = ''.join(prev_audio) + current_audio
		        self.stream.stop_stream()
		        audio_bitstream = np.fromstring(all_audio_data, np.uint8)
		        audio = audio_bitstream.tolist()
		        self.audio_publisher.publish(audio)
		        sliding_window.clear()
		        prev_audio.clear()
		        current_audio = ''
			self.listening_done_publisher.publish(True)
			if self.state == "Speaking":
				self.started = True
		    else:
		        prev_audio.append(latest_audio_data)

    def audio_int(self):
        self.get_record_device_index()
        self.determine_silence_threshold()

    def determine_silence_threshold(self):
        """ Calculates the threshold of when the audio input is loud enough to trigger a recording
            It does this by collecting 50 samples of the background noise and using the
            average of the top 20% as the threshold
        """
        loudest_sound_cohort_size = 0.2  # Top 20% are counted in the loudest sound group.
        silence_threshold_multiplier = 1.6  # Sounds must be at least 1.6x as loud as the loudest silence

        rospy.loginfo("Getting intensity values from mic.")
        #self.open_stream()
        #tss = self.total_silence_samples
        #values = [math.sqrt(abs(audioop.avg(self.stream.read(self.chunk_size), self.audio_format_width)))
        #          for _ in range(tss)]
        #values = sorted(values, reverse=True)
        #sum_of_loudest_sounds = sum(values[:int(tss * loudest_sound_cohort_size)])
        #total_samples_in_cohort = int(tss * loudest_sound_cohort_size)
        #average_of_loudest_sounds = sum_of_loudest_sounds / total_samples_in_cohort
	average_of_loudest_sounds = 2
        rospy.loginfo("Average audio intensity is %d" % average_of_loudest_sounds)
        self.silence_threshold = average_of_loudest_sounds * silence_threshold_multiplier
        rospy.loginfo("Silence threshold set to %d " % self.silence_threshold)
        #self.close_stream()

    
 
    def get_record_device_index(self):
        """ Finds the audio device named 'record' configured in ~/.asoundrc.
            If this device is not found, returns None and pyaudio will use
            your machines default device
        """
        #rospy.loginfo("Attempting to find device named 'record'")
        for i in range(self.p.get_device_count()):
            device = self.p.get_device_info_by_index(i)
	    print(device['name'])
            if device['name'] =='ReSpeaker 4 Mic Array (UAC1.0): USB Audio (hw:1,0)':
                rospy.loginfo("Found device 'record' at index %d" % i)
                self.input_device_index = i
                return
        #rospy.loginfo("Could not find device named 'record', falling back to default recording device")


def main():
    try:
        voice_input = VoiceInput(node_name="microphone_node")
	voice_input.audio_int()
	voice_input.listen()
    except rospy.ROSInterruptException:
        pass


if __name__ == '__main__':
    main()
