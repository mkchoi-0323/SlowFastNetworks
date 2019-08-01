import errno
import os
import shutil
import json
import sys

from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.video.io.VideoFileClip import VideoFileClip

rep = '/raid/'
ann_file = rep + 'aNet/activity_net.v1-3.min.json'
train_path = rep + 'aNet_trim/train/'
val_path = rep + 'aNet_trim/validation/'
test_path = rep + 'aNet_trim/test/'
data_path = rep + 'ActivityNet/Videos/'
#train_split = 'trainlist01.txt'
#test_split = 'testlist01.txt'

with open(ann_file, "r") as fobj:
    anet_v_1_3 = json.load(fobj)
    all_vids = anet_v_1_3["database"].keys() 
    db = anet_v_1_3["database"]
    taxonomy = anet_v_1_3["taxonomy"]

## Leaf node extraction
tax_list = []
leaf_list = []
parent_ids = []
for item in taxonomy:
    if item["parentId"] not in parent_ids:
        parent_ids.append(item["parentId"])

for item in taxonomy:
    if item["nodeId"] not in parent_ids:
        leaf_list.append(item["nodeName"])

leaf_list.sort()

train_list = []
n_train = 0
val_list = []
n_val = 0
test_list = []
n_test = 0

for key in all_vids:
    if db[key]['subset'] == 'training':
        n_train = n_train + 1
        instance = [key, db[key]['annotations'][0]['label'], db[key]['annotations'][0]['segment']]
        train_list.append(instance)
    if db[key]['subset'] == 'validation':
        n_val = n_val + 1
        instance = [key, db[key]['annotations'][0]['label'], db[key]['annotations'][0]['segment']]
        val_list.append(instance)
    if db[key]['subset'] == 'testing':
        n_test = n_test + 1
        test_list.append(key)

ext = '.mp4'

for item in train_list:
    video = 'v_' + item[0] + ext
    src = data_path + video

    n_segments = len(db[item[0]]['annotations'])

    #all_vids = anet_v_1_3["database"].keys()
    #if n_segments > 1:

    dst_path = train_path + item[1] + '/'

    if not os.path.isdir(dst_path):
        os.makedirs(dst_path)

    seg_idx = 0
    for segment in db[item[0]]['annotations']:
        start = segment['segment'][0]
        end = segment['segment'][1]
        duration = end - start
        if duration == 0:
            continue
        
        dst = dst_path + 'v_' + item[0] + '_' + str(seg_idx) + ext

        print("Trimming training set from [" + src + "]" + " to " + "[" + dst + "], " + 
            "time[" + str(start) + ":" + str(end) + "], " + "duration[" + str(end-start) + "]")

        if start > end:
            print("Sement time error from " + src)
            print("time[" + str(start) + ":" + str(end) + "], " + "duration[" + str(end-start) + "]")

        with VideoFileClip(src) as video:
            v_duration = video.duration
            if end > v_duration:
                end = v_duration-0.01
        
        ffmpeg_extract_subclip(src, start, end, targetname=dst)
        # with VideoFileClip(src) as video:
        #     trim = video.subclip(start, end)
        #     trim.write_videofile(dst)

        seg_idx = seg_idx + 1

for item in val_list:
    video = 'v_' + item[0] + ext
    src = data_path + video
    
    n_segments = len(db[item[0]]['annotations'])

    #all_vids = anet_v_1_3["database"].keys()
    #if n_segments > 1:

    dst_path = val_path + item[1] + '/'

    if not os.path.isdir(dst_path):
        os.makedirs(dst_path)

    seg_idx = 0
    for segment in db[item[0]]['annotations']:
        start = segment['segment'][0]
        end = segment['segment'][1]
        duration = end - start
        if duration == 0:
            continue
        
        dst = dst_path + 'v_' + item[0] + '_' + str(seg_idx) + ext

        print("Trimming validation set from [" + src + "]" + " to " + "[" + dst + "], " + 
            "time[" + str(start) + ":" + str(end) + "], " + "duration[" + str(end-start) + "]")

        if start > end:
            print("Sement time error from " + src)
            print("time[" + str(start) + ":" + str(end) + "], " + "duration[" + str(end-start) + "]")

        with VideoFileClip(src) as video:
            v_duration = video.duration
            if end > v_duration:
                end = v_duration-0.01
        
        ffmpeg_extract_subclip(src, start, end, targetname=dst)
        # with VideoFileClip(src) as video:
        #     trim = video.subclip(start, end)
        #     trim.write_videofile(dst)

        seg_idx = seg_idx + 1