import numpy as np
import pandas as pd
import math
import json
import os
import sys
import shutil
import errno

import cv2

from moviepy.video.io.VideoFileClip import VideoFileClip

overlap = "non-overlap"
training_types = ["train", "validation"]
date = "190704"
ann_folder = '/raid/HuToM/201906_Gastric/annotation_190628/' + overlap + '/'
trim_path = '/raid/HuToM/201906_Gastric/bleeding_' + date + '/' + overlap + '/trim'
train_path = '/raid/HuToM/201906_Gastric/bleeding/training/'
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
    for training_type in training_types:
        vid_path = train_path + str(trim_sec) + '/armes_all/' + training_type + '/' + armes + '/'
        if os.path.exists(vid_path) == False:
            continue
        vids = os.listdir(vid_path)

        for vid in vids:
            if not 'R0' in vid:
                vids.remove(vid)
                continue
            load_vid_path = vid_path + vid
            capture = cv2.VideoCapture(load_vid_path)
            frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
            frame_width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
            frame_height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
            #print(load_vid_path, frame_count, frame_width, frame_height)
            if frame_height < 1 or frame_width < 1 or frame_count < 5:
                print("----------------------Error-----------------------")
                print(vid, frame_count, frame_width, frame_height)
                os.remove(load_vid_path)
                print("Removed")

            # with VideoFileClip(src) as video:
            #     v_duration = video.duration
            #     if end > v_duration:
            #         break
            #     trim = video.subclip(start, end)
            #     trim.write_videofile(dst)

    
