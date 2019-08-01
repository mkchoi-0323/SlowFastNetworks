import numpy as np
import pandas as pd
import math
import json
import os
import sys
import shutil
import errno

from moviepy.video.io.VideoFileClip import VideoFileClip

overlap = "non-overlap"
date = "190704"
ann_folder = '/raid/HuToM/201906_Gastric/annotation_190628/' + overlap + '/'
trim_path = '/raid/HuToM/201906_Gastric/bleeding_' + date + '/' + overlap + '/trim'
train_path = '/raid/HuToM/201906_Gastric/bleeding/training/'
trim_sec = 2.0
frame_rate = 30.0
train_rate = 0.8

trim_path = trim_path + '_' + str(trim_sec) + '/'

bg_classes = ['bg_normal', 'bg_blood_stained_tissue']
blood_collected_classes = ['bood_collected']
bleeding_classes = ['no_bleeding', 'bleeding_w_intervention', 'bleeding_wo_intervention']

#armes_stat = [0] * len(armes_classes)

bleeding_training = ['bleeding_w_intervention', 'bleeding_wo_intervention']
non_bleeding_traiing = ['bg_normal']

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
			dst_folder = train_path + str(trim_sec) + '/' + armes_type[0] + '/' + "validataion/" + armes + "/"
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
			

