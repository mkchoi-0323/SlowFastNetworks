import numpy as np
import pandas as pd
import math
import json
import os
import sys
import csv

from moviepy.video.io.VideoFileClip import VideoFileClip

data_path = '/nas/Public/M2CAI_Workflow/2019/'
ann_folder = data_path + 'annotations/'
vid_folder = data_path + 'video/'
trim_path = '/raid/MICCAI_phase/trim'

prefix = 'Hei-Chole'
n_vid = 12

ann_types = ['Action', 'Phase', 'Instrument']
ann_ext = '.csv'

actions = ['Grasp', 'Hold', 'Cut', 'Clip']
action_stat = [0]*len(actions)

tools = ['Curved atraumatic grasper', 'Toothed grasper', 'Fenestrated toothed grasper', 'Atraumatic grasper', 'Overholt', 'LigaSure', 'Electric hook', 'Scissors', 
		'Clip-applier (metal)', 'Clip-applier (Hem-O-Lok)', 'Swab grasper', 'Argon beamer', 'Suction-irrigation', 'Specimen bag', 'Tiger mouth forceps', 'Claw forceps', 'Undefined']
tool_stat = [0]*len(tools)

phases = ['Preparation', 'Calot triangle dissection', 'Clipping and cutting', 'Galbladder dissection', 'Galbladder packaging', 'Cleaning and coagulation', 'Galbladder retraction']
phase_stat = [0]*len(phases)

for n in range(n_vid):
    vid_action_stat = [0]*len(actions)
    vid_tool_stat = [0]*len(tools)
    vid_phase_stat = [0]*len(phases)
    for ann_type in ann_types:
        ann = ann_folder + prefix + str(n+1) + '_Annotation_' + ann_type + ann_ext
        print(ann)
        f = open(ann, 'r')
        rdr = csv.reader(f)

        for line in rdr:
            line_item = []
            fnum = int(line[0])
            line = line[1:]
            line = [int(i) for i in line]
            if ann_type == 'Action':
                for idx in range(len(action_stat)):
                    action_stat[idx] = action_stat[idx] + line[idx]
                    vid_action_stat[idx] = vid_action_stat[idx] + line[idx]
            if ann_type == 'Instrument':
                for idx in range(len(tool_stat)):
                    tool_stat[idx] = tool_stat[idx] + line[idx]
                    vid_tool_stat[idx] = vid_tool_stat[idx] + line[idx]
                if line[20] == 1:
                    tool_stat[-1] = tool_stat[-1] + 1
                    vid_tool_stat[-1] = vid_tool_stat[-1] + 1
            if ann_type == 'Phase':
                phase_stat[line[0]] = phase_stat[line[0]] + 1
                vid_phase_stat[line[0]] = vid_phase_stat[line[0]] + 1
    print('Action statistics')
    print(actions)
    #print(vid_action_stat)
    for action in vid_action_stat:
        print(action)
    print('Phase statistics')
    print(phases)
    #print(vid_phase_stat)
    for phase in vid_phase_stat:
        print(phase)
    print('Instrument statistics')
    print(tools)
    for tool in vid_tool_stat:
        print(tool)
    #print(vid_tool_stat)

print('Action statistics')
print(actions)
#print(action_stat)
for action in action_stat:
    print(action)
print('Phase statistics')
print(phases)
#print(phase_stat)
for phase in phase_stat:
    print(phase)
print('Instrument statistics')
print(tools)
#print(tool_stat)
for tool in tool_stat:
        print(tool)

