import numpy as np
import pandas as pd
import math
import json
import os
import sys
import shutil
import errno
import random

from moviepy.video.io.VideoFileClip import VideoFileClip

data_path = '/nas/Public/M2CAI_Workflow/2019/'
ann_folder = data_path + 'annotations/'
vid_folder = data_path + 'video/'
train_date = '20190807'
video_prefix = 'Hei-Chole'

trim_path = '/raid/MICCAI_phase/trim'
trim_sec = 10.0
trim_interval = 1.0
frame_rate = 30.0
train_rate = 0.8
n_vids = 12
train_path = '/raid/MICCAI_phase/trainval_' + train_date + '_' + trim_sec + '_' + trim_interval + '/'

trim_path = trim_path + '_' + str(trim_sec) + '/'

phase_classes = ['Preparation', 'Calot triangle dissection', 'Clipping and cutting', 'Galbladder dissection', 'Galbladder packaging', 'Cleaning and coagulation', 'Galbladder retraction']
#phase_stat = [0] * len(armes_classes)

def copy_vid(src, dst, dst_folder):
	try:
		shutil.copy(src, dst)
	except IOError as e:
		# ENOENT(2): file does not exist, raised also on missing dest parent dir
		if e.errno != errno.ENOENT:
			raise
		# try creating parent directories
		os.makedirs(dst_folder)
		#os.makedirs(os.path.dirname(dst))
		shutil.copy(src, dst)

vid_list = range(n_vids)
for idx in range(len(vid_list)):
	vid_list[idx] = video_prefix + str(idx+1)

random.shuffle(vid_list)
train_prefix = vid_list[0:int(train_rate * n_vids)]
val_prefix = vid_list[int(train_rate * n_vids):]
train_vids = []
val_vids = []

for phase in phase_classes:
	vid_path = trim_path + phase + '/'
	vids = os.listdir(vid_path)

	for vid in vids:
		if not video_prefix in vid:
			vids.remove(vid)
			continue
		for train_vid in train_videos:
			if train_vid in vid:
				src = vid_path + vid
				dst_folder = train_path + "train/" + phase + "/"
				dst = dst_folder + vid
				disp = "Copying from [" + src + "] to [" + dst + "]" 
				print(disp)
				#copy_vid(src, dst, dst_folder)
		if val_vid in val_videos:
			if val_vid in vid:	
				src = vid_path + vid
				dst_folder = train_path + '/' + "validation/" + phase + "/"
				dst = dst_folder + vid
				disp = "Copying from [" + src + "] to [" + dst + "]" 
				print(disp)
				#copy_vid(src, dst, dst_folder)
			
print("Cross valdidation for ARMES")
print("Training videos")
print(train_videos)
print("Validation videos")
print(val_videos)