import numpy as np
import pandas as pd
import math
import json
import os
import sys
import csv

from moviepy.video.io.VideoFileClip import VideoFileClip

def load_json(file):
    with open(file) as json_file:
        data = json.load(json_file)
        return data

data_path = '/nas/Public/M2CAI_Workflow/2019/'
ann_folder = data_path + 'annotations/'
vid_folder = data_path + 'video/'
trim_path = '/raid/MICCAI_phase/trim'

video_prefix = 'Hei-Chole'
n_vid = 12
vext = '.avi'

ann_type = 'Phase'
phase_classes = ['Preparation', 'Calot triangle dissection', 'Clipping and cutting', 'Galbladder dissection', 'Galbladder packaging', 'Cleaning and coagulation', 'Galbladder retraction']
phase_stat = [0] * len(phase_classes)
ann_ext = '.csv'
video_ext = '.avi'
trim_sec = 10.0
trim_interval = 1.0
min_length = 1.0
rate = 30.0
trim_path = trim_path + '_' + str(trim_sec) + '_' + str(trim_interval) + '/'

for n in range(n_vid):
	vid_name = vid_folder + video_prefix + str(n+1) + video_ext
	ann_name = ann_folder + video_prefix + str(n+1) + '_Annotation_' + ann_type + ann_ext
	print(ann_name)

	f = open(ann_name, 'r')
	rdr = csv.reader(f)

	row_count = sum(1 for row in rdr)
	f.close()

	pre = None
	temporal_boundary = []
	start = None
	end = None
	flag = 0

	f = open(ann_name, 'r')
	rdr = csv.reader(f)

	for line in rdr:
		fnum = float(line[0])
		curr = line[1]

		if pre != curr:
			if flag == 0:
				start = fnum
				flag = 1
				curr_class = phase_classes[int(curr)]
				pre = curr
			else:
				end = fnum
				temporal_boundary.append([start/rate, end/rate, curr_class, end/rate-start/rate])
				flag = 0
				#pre = curr

		if fnum == row_count-1:
			print(int(fnum), row_count-1)
			end = fnum
			temporal_boundary.append([start/rate, end/rate, curr_class, end/rate-start/rate])
			flag = 0	
	print(temporal_boundary)

	for phase in temporal_boundary:
		s_time = phase[0]
		e_time = phase[1]
		segment_time = e_time - s_time
		n_segments = int(math.ceil(segment_time/trim_interval))

		phase_stat[phase_classes.index(phase[2])] = phase_stat[phase_classes.index(phase[2])] + segment_time

		src = vid_name
		dst_path = trim_path + phase[2] + '/'

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

			dst = dst_path + video_prefix + str(n+1) + '_' + str(i) + '.mp4'

			print("Trimming training set from [" + src + "] to [" + dst + "], time[" + str(start) + 
					":" + str(end) + "], duration[" + str(duration) + "], Type[" + str(phase[2]) + "]")
		
			with VideoFileClip(src) as video:
				v_duration = video.duration
				if end > v_duration:
					break
				trim = video.subclip(start, end)
				trim.write_videofile(dst)
	f.close()

print("Phase statistics")
print(phase_classes)
print(phase_stat)
