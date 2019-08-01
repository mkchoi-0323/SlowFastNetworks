import numpy as np
import pandas as pd
import math
import json
import os
import sys

from moviepy.video.io.VideoFileClip import VideoFileClip

def load_json(file):
    with open(file) as json_file:
        data = json.load(json_file)
        return data

overlap = "non-overlap"
ann_folder = '/raid/HuToM/201906_Gastric/annotation_190628/' + overlap + '/'
video_path = '/raid/HuToM/201906_Gastric/videos/'
trim_path = '/raid/HuToM/201906_Gastric/ARMES/' + overlap + '/trim'

annotators = ['ahmed', 'anwar', 'edmund', 'bernice']
#armes_types = ['p_armes']
armes_classes = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', 
				'11', '12', '13', '14', '15', '16', '17', '18', '19',
				'20', '21', '30', '31', '32', '33', '34','35']
armes_stat = [0] * len(armes_classes)
ann_ext = '.json'
video_ext = '.mp4'
trim_sec = 5.0
trim_interval = 0.2
min_length = 1.0
rate = 30.0
trim_path = trim_path + '_' + str(trim_sec) + '_' + str(trim_interval) + '/'

vids = os.listdir(video_path)

for vid in vids:
	if not 'R0' in vid:
		continue

	ann_vid = ann_folder + vid + '/'
	if os.path.exists(ann_vid) == False:
		continue
	annotators_vid = os.listdir(ann_vid)

	for annotator in annotators_vid:
		if not annotator in annotators:
			continue

		ann_path = ann_folder + vid + '/' + annotator + '/'		

		print("Processing [" + ann_path + "]")

		json_header = ann_path + vid + '_pb_' + 'header' + '_' + annotator + ann_ext
		header = load_json(json_header)
		json_data = ann_path + vid + '_pb' + '_' + annotator + ann_ext
		data = load_json(json_data)

		if not os.path.isfile(json_data):
			continue
		
		for armes in data['data']['p_armes']:
			if armes['p_armes_class'] < 0:
				continue

			part = armes['part']
			s_frame = armes['start_frame']
			e_frame = armes['stop_frame']
			segment_frame = e_frame - s_frame
			s_time = s_frame/rate
			e_time = e_frame/rate
			segment_time = e_time - s_time
			#n_segments = int(math.ceil(segment_time/trim_sec))
			n_segments = int(math.ceil(segment_time/trim_interval))

			armes_stat[armes_classes.index(str(armes['p_armes_class']))] = armes_stat[armes_classes.index(str(armes['p_armes_class']))] + segment_frame

			video = header['part'][part]
			if video == "":
				continue
			
			src = video_path + vid + '/' + video
			dst_path = trim_path  + str(armes['p_armes_class']) + '/'

			if not os.path.isdir(dst_path):
				os.makedirs(dst_path)

			c_time = s_time
			for i in range(n_segments):
				start = c_time
				#end = c_time + trim_sec
				end = c_time + trim_sec
				c_time = c_time + trim_interval

				if end > e_time:
					end = e_time

				duration = end-start
				
				if duration < min_length:
			 		break

				dst = dst_path + vid + '_' + str(i) +  video_ext

				print("Trimming training set from [" + src + "] to [" + dst + "], time[" + str(start) + 
						":" + str(end) + "], duration[" + str(duration) + "], Annotator[" + annotator + 
						"], Type[" + str(armes['p_armes_class']) + "]")
	      
				with VideoFileClip(src) as video:
					v_duration = video.duration
					if end > v_duration:
						break
					trim = video.subclip(start, end)
					trim.write_videofile(dst)

	#print("armes statitics with [" + annotator + "]")
	#print(armes_classes)
	#print(armes_stat)	

print("ARMES statistics")
print(armes_classes)
print(armes_stat)
