import os
import sys
from pathlib import Path

import cv2
import numpy as np
import csv
from torch.utils.data import DataLoader, Dataset

prefix = 'Hei-Chole'
dpath = '/data/MICCAI/'
vpath = dpath + 'video/'
n_vid = 12
vext = '.avi'

apath = dpath + 'annotations/'
atypes = ['Action', 'Phase', 'Instrument']
aext = '.csv'
actions = ['Grasp', 'Hold', 'Cut', 'Clip']
action_stat = [None]*len(actions)
tools = ['Curved atraumatic grasper', 'Toothed grasper', 'Fenestrated toothed grasper', 'Atraumatic grasper', 'Overholt', 'LigaSure', 'Electric hook', 'Scissors', 
		'Clip-applier (metal)', 'Clip-applier (Hem-O-Lok)', 'Swab grasper', 'Argon beamer', 'Suction-irrigation', 'Specimen bag', 'Tiger mouth forceps', 'Claw forceps']
tool_stat = [None]*len(tools)
steps = ['Preparation', 'Calot triangle dissection', 'Clipping and cutting', 'Galbladder dissection', 'Galbladder packaging', 'Cleaning and coagulation', 'Galbladder retraction']
step_stat = [None]*len(steps)

count = 0
vid_num = 1
part = 2
for n in range(n_vid):
	count = count + 1
	if not count == vid_num:
		continue
	vname = vpath + prefix + str(n+1) + vext
	action_list = []
	phase_list = []
	inst_list = []

	for atype in atypes:
		aname = apath + prefix + str(n+1) + '_Annotation_' + atype + aext
		print(aname)
		f = open(aname, 'r')
		rdr = csv.reader(f)

		for line in rdr:
			line_item = []
			fnum = int(line[0])
			line = line[1:]
			line_item.append(fnum)

			if atype == 'Action':
				hit = [i for i, e in enumerate(line) if e == '1']
				if not hit:
					action = 'None'
					line_item.append(action)
				else:
					for i in hit:
						action = actions[int(i)]
						line_item.append(action)
				action_list.append(line_item)
			
			if atype == 'Phase':
				step = steps[int(line[0])]
				line_item.append(step)
				phase_list.append(line_item)
				
			if atype == 'Instrument':
				hit = [i for i, e in enumerate(line) if e == '1']
				if not hit:
					tool = 'None'
					line_item.append(tool)
				else:
					for i in hit:
						if i == 20:
							tool = 'Undefined'
							line_item.append(tool)
						else:
							tool = tools[int(i)]
							line_item.append(tool)
				inst_list.append(line_item)
		f.close()

	print(len(action_list), len(phase_list), len(inst_list))
	frame_array = []
	cap = cv2.VideoCapture(vname)
	frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
	frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
	frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
	print(vname, frame_width, frame_height, frame_count)
	first = int(frame_count/3)
	second = first*2

	if part == 1:
		for i in range(first):
			cap.set(cv2.CAP_PROP_POS_FRAMES,i)
			#cap.set(1,fnum)
			ret, frame = cap.read()

			font = cv2.FONT_HERSHEY_SIMPLEX
			action_items = action_list[i]
			action_items = action_items[1:]
			phase_items = phase_list[i]
			phase_items = phase_items[1:]
			inst_items = inst_list[i]
			inst_items = inst_items[1:]
			text_gap = 25
			height = 0
			text_start = 300
			
			height = height + text_gap
			cv2.putText(frame, 'Action', (frame_width-text_start, height), font, 0.7, (255, 0, 0), 2, cv2.LINE_AA)
			for action in action_items:
				#print(action)
				height = height + text_gap	
				cv2.putText(frame, action, (frame_width-text_start, height), font, 0.7, (255, 0, 0), 2, cv2.LINE_AA)

			height = height + text_gap
			cv2.putText(frame, 'Phase', (frame_width-text_start, height), font, 0.7, (0, 255, 0), 2, cv2.LINE_AA)
			for phase in phase_items:
				#print(phase)
				height = height + text_gap
				cv2.putText(frame, phase, (frame_width-text_start, height), font, 0.7, (0, 255, 0), 2, cv2.LINE_AA)

			height = height + text_gap
			cv2.putText(frame, 'Instrument', (frame_width-text_start, height), font, 0.7, (0, 0, 255), 2, cv2.LINE_AA)
			for inst in inst_items:
				#print(inst)
				height = height + text_gap
				cv2.putText(frame, inst, (frame_width-text_start, height), font, 0.7, (0, 0, 255), 2, cv2.LINE_AA)

			#window_name = vname# + '[' + str(i) + ']'
			#cv2.imshow(window_name, frame)
			#cv2.waitKey(0)
			#sys.exit(1)
			if i % 100 == 0:
				disp = str(i) + '/' + str(frame_count)
				print(disp)
			frame_array.append(frame)

		outName = vpath + prefix + str(n+1) + '_ann_part1' + vext
		print(outName)
		out = cv2.VideoWriter(outName,cv2.VideoWriter_fourcc(*'DIVX'), 30, (frame_width, frame_height))
		for i in range(len(frame_array)):
			out.write(frame_array[i])
		out.release()
		cap.release()

	if part == 2:
		for i in range(first):
			i = i + first
			cap.set(cv2.CAP_PROP_POS_FRAMES,i)
			#cap.set(1,fnum)
			ret, frame = cap.read()

			font = cv2.FONT_HERSHEY_SIMPLEX
			action_items = action_list[i]
			action_items = action_items[1:]
			phase_items = phase_list[i]
			phase_items = phase_items[1:]
			inst_items = inst_list[i]
			inst_items = inst_items[1:]
			text_gap = 30
			height = 0
			text_start = 300
			
			height = height + text_gap
			cv2.putText(frame, 'Action', (frame_width-text_start, height), font, 0.7, (255, 0, 0), 2, cv2.LINE_AA)
			for action in action_items:
				#print(action)
				height = height + text_gap	
				cv2.putText(frame, action, (frame_width-text_start, height), font, 0.7, (255, 0, 0), 2, cv2.LINE_AA)

			height = height + text_gap
			cv2.putText(frame, 'Phase', (frame_width-text_start, height), font, 0.7, (0, 255, 0), 2, cv2.LINE_AA)
			for phase in phase_items:
				#print(phase)
				height = height + text_gap
				cv2.putText(frame, phase, (frame_width-text_start, height), font, 0.7, (0, 255, 0), 2, cv2.LINE_AA)

			height = height + text_gap
			cv2.putText(frame, 'Instrument', (frame_width-text_start, height), font, 0.7, (0, 0, 255), 2, cv2.LINE_AA)
			for inst in inst_items:
				#print(inst)
				height = height + text_gap
				cv2.putText(frame, inst, (frame_width-text_start, height), font, 0.7, (0, 0, 255), 2, cv2.LINE_AA)

			#window_name = vname# + '[' + str(i) + ']'
			#cv2.imshow(window_name, frame)
			#cv2.waitKey(0)
			#sys.exit(1)
			if i % 100 == 0:
				disp = str(i) + '/' + str(frame_count)
				print(disp)
			frame_array.append(frame)

		outName = vpath + prefix + str(n+1) + '_ann_part2' + vext
		print(outName)
		out = cv2.VideoWriter(outName,cv2.VideoWriter_fourcc(*'DIVX'), 30, (frame_width, frame_height))
		for i in range(len(frame_array)):
			out.write(frame_array[i])
		out.release()

		cap.release()

	if part == 3:
		for i in range(first):
			i = i + second
			cap.set(cv2.CAP_PROP_POS_FRAMES,i)
			#cap.set(1,fnum)
			ret, frame = cap.read()

			font = cv2.FONT_HERSHEY_SIMPLEX
			action_items = action_list[i]
			action_items = action_items[1:]
			phase_items = phase_list[i]
			phase_items = phase_items[1:]
			inst_items = inst_list[i]
			inst_items = inst_items[1:]
			text_gap = 30
			height = 0
			text_start = 300
			
			height = height + text_gap
			cv2.putText(frame, 'Action', (frame_width-text_start, height), font, 0.7, (255, 0, 0), 2, cv2.LINE_AA)
			for action in action_items:
				#print(action)
				height = height + text_gap	
				cv2.putText(frame, action, (frame_width-text_start, height), font, 0.7, (255, 0, 0), 2, cv2.LINE_AA)

			height = height + text_gap
			cv2.putText(frame, 'Phase', (frame_width-text_start, height), font, 0.7, (0, 255, 0), 2, cv2.LINE_AA)
			for phase in phase_items:
				#print(phase)
				height = height + text_gap
				cv2.putText(frame, phase, (frame_width-text_start, height), font, 0.7, (0, 255, 0), 2, cv2.LINE_AA)

			height = height + text_gap
			cv2.putText(frame, 'Instrument', (frame_width-text_start, height), font, 0.7, (0, 0, 255), 2, cv2.LINE_AA)
			for inst in inst_items:
				#print(inst)
				height = height + text_gap
				cv2.putText(frame, inst, (frame_width-text_start, height), font, 0.7, (0, 0, 255), 2, cv2.LINE_AA)

			#window_name = vname# + '[' + str(i) + ']'
			#cv2.imshow(window_name, frame)
			#cv2.waitKey(0)
			#sys.exit(1)
			if i % 100 == 0:
				disp = str(i) + '/' + str(frame_count)
				print(disp)
			frame_array.append(frame)

		outName = vpath + prefix + str(n+1) + '_ann_part3' + vext
		print(outName)
		out = cv2.VideoWriter(outName,cv2.VideoWriter_fourcc(*'DIVX'), 30, (frame_width, frame_height))
		for i in range(len(frame_array)):
			out.write(frame_array[i])
		out.release()

		cap.release()
	