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
trim_path = '/raid/HuToM/201906_Gastric/bleeding/' + overlap + '/trim'

annotators = ['ahmed', 'anwar', 'edmund', 'bernice']
blood_types = ['b_background', 'b_collected', 'b_event_a', 'b_event_b', 'b_event_c']
bleeding_classes = ['bg_normal', 'bg_blood_stained_tissue', 'blood_collected', 
			'no_bleeding', 'bleeding_w_intervention', 'bleeding_wo_intervention']
bleeding_stat = [0] * len(bleeding_classes)
ann_ext = '.json'
video_ext = '.mp4'
trim_sec = 1.0
trim_interval = 0.1
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

		#print(data['data'].keys())
		
		for blood_type in blood_types:
			for bleeding in data['data'][blood_type]:
                                bleeding_class = blood_type + "_class"
				if bleeding[bleeding_class] < 0:
					continue

				part = bleeding['part']
				s_frame = bleeding['start_frame']
				e_frame = bleeding['stop_frame']
				segment_frame = e_frame - s_frame
				s_time = s_frame/rate
				e_time = e_frame/rate
				segment_time = e_time - s_time
				n_segments = int(math.ceil(segment_time/trim_sec))

				video = header['part'][part]
				if video == "":
					continue

				if blood_type == 'b_background':
					if bleeding[bleeding_class] == 1:
						#new_class = 'bg_normal'
						new_class = bleeding_classes[0]
						bleeding_stat[0] = bleeding_stat[0] + segment_frame
					if bleeding[bleeding_class] == 2:
						#new_class = 'bg_blood_stained_tissue'
						new_class = bleeding_classes[1]
						bleeding_stat[1] = bleeding_stat[1] + segment_frame
				if blood_type == 'b_collected':
					if bleeding[bleeding_class] == 1:
						#new_class = 'bood_collected'
						new_class = bleeding_classes[2]
						bleeding_stat[2] = bleeding_stat[2] + segment_frame
				if blood_type == 'b_event_a' or blood_type == 'b_event_b' or blood_type == 'b_event_c':
					if bleeding[bleeding_class] == 0:
						#new_class = 'no_bleeding'
						new_class = bleeding_classes[3]
						bleeding_stat[3] = bleeding_stat[3] + segment_frame
					if bleeding[bleeding_class] == 1:
						#new_class = 'bleeding_w_intervention'
						new_class = bleeding_classes[4]
						bleeding_stat[4] = bleeding_stat[4] + segment_frame
					if bleeding[bleeding_class] == 2:
						#new_class = 'bleeding_wo_intervention'
						new_class = bleeding_classes[5]
						bleeding_stat[5] = bleeding_stat[5] + segment_frame

				src = video_path + vid + '/' + video
				dst_path = trim_path + str(new_class) + '/'

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

					duration = end - start
					if duration < min_length:
						break

					dst = dst_path + vid + '_' + str(i) +  video_ext

					print("Trimming training set from [" + src + "] to [" + dst + "], time[" + str(start) + 
						":" + str(end) + "], duration[" + str(duration) + "], Annotator[" + annotator + 
						"], Type[" + new_class + "]")
		      
					with VideoFileClip(src) as video:
						v_duration = video.duration
						if end > v_duration:
							break
						trim = video.subclip(start, end)
						trim.write_videofile(dst)

	# print("Bleeding statitics with [" + annotator + "]")
	# print(bleeding_classes)
	# print(bleeding_stat)	

print("Bleeding statistics")
print(bleeding_classes)
print(bleeding_stat)
