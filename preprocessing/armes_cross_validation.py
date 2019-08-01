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

overlap = "non-overlap"
armes_type = ["armes_only", "armes_all"]
split_date = "190704"
train_date = "190709"
ann_folder = '/raid/HuToM/201906_Gastric/annotation_190628/' + overlap + '/'
#trim_path = '/raid/HuToM/201906_Gastric/ARMES_' + date + '/' + overlap + '/trim'
trim_path = '/raid/HuToM/201906_Gastric/ARMES/' + overlap + '/trim'
train_path = '/raid/HuToM/201906_Gastric/ARMES/training_' + train_date + '/'
trim_sec = 2.0
frame_rate = 30.0
train_rate = 0.8

trim_path = trim_path + '_' + str(trim_sec) + '/'

armes_only_classes = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', 
				'11', '12', '13', '14', '15', '16', '17', '18', '19',
				'20', '21']
armes_all_classes = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', 
				'11', '12', '13', '14', '15', '16', '17', '18', '19',
				'20', '21', '30', '31', '32', '33', '34','35']

#armes_stat = [0] * len(armes_classes)

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

#annotators_vid = os.listdir(ann_vid)
vid_list = []
for armes in armes_all_classes:
	vid_path = trim_path + armes + '/'
	vids = os.listdir(vid_path)

	for vid in vids:
		if not 'R0' in vid:
			vids.remove(vid)
			continue
		split_vid = vid.split('_')
		if not split_vid[0] in vid_list:
			vid_list.append(split_vid[0])
vid_list.sort()
n_vids = len(vid_list)
random.shuffle(vid_list)
train_videos = vid_list[0:int(train_rate * n_vids)]
val_videos = vid_list[int(train_rate * n_vids):]

for armes in armes_only_classes:
	vid_path = trim_path + armes + '/'
	vids = os.listdir(vid_path)

	for vid in vids:
		if not 'R0' in vid:
			vids.remove(vid)
			continue
		split_vid = vid.split('_')
		if split_vid[0] in train_videos:
			src = vid_path + vid
			dst_folder = train_path + str(trim_sec) + '/' + armes_type[0] + '/' + "train/" + armes + "/"
			dst = dst_folder + vid
			disp = "Copying from [" + src + "] to [" + dst + "]" 
			print(disp)
			copy_vid(src, dst, dst_folder)
		if split_vid[0] in val_videos:
			src = vid_path + vid
			dst_folder = train_path + str(trim_sec) + '/' + armes_type[0] + '/' + "validation/" + armes + "/"
			dst = dst_folder + vid
			disp = "Copying from [" + src + "] to [" + dst + "]" 
			print(disp)
			copy_vid(src, dst, dst_folder)

for armes in armes_all_classes:
	vid_path = trim_path + armes + '/'
	vids = os.listdir(vid_path)

	for vid in vids:
		if not 'R0' in vid:
			vids.remove(vid)
			continue
		split_vid = vid.split('_')
		if split_vid[0] in train_videos:
			src = vid_path + vid
			dst_folder = train_path + str(trim_sec) + '/' + armes_type[1] + '/' + "train/" + armes + "/"
			dst = dst_folder + vid
			disp = "Copying from [" + src + "] to [" + dst + "]" 
			print(disp)
			copy_vid(src, dst, dst_folder)
		if split_vid[0] in val_videos:
			src = vid_path + vid
			dst_folder = train_path + str(trim_sec) + '/' + armes_type[1] + '/' + "validation/" + armes + "/"
			dst = dst_folder + vid
			disp = "Copying from [" + src + "] to [" + dst + "]" 
			print(disp)
			copy_vid(src, dst, dst_folder)
			
print("Cross valdidation for ARMES")
print("Training videos")
print(train_videos)
print("Validation videos")
print(val_videos)