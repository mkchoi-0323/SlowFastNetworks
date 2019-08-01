import errno
import os
import shutil
import json
import sys

rep = '/raid/'
ann_file = rep + 'aNet/activity_net.v1-3.min.json'
train_path = rep + 'aNet/train/'
val_path = rep + 'aNet/validation/'
test_path = rep + 'aNet/test/'
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

ext = ['mp4','mkv','webm']

print('Copy data for training')
for item in train_list:
    exist = 0

    for v in ext:
        video = 'v_' + item[0] + '.' + v
        src = data_path + video
        if os.path.exists(src):
            exist = 1
            break

    dst_path = train_path + item[1] + '/'
    dst = dst_path + video

    print("Copying training set from [" + src + "]" + " to " + "[" + dst + "]" )

    try:
        shutil.copy(src, dst)
    except IOError as e:    
        # ENOENT(2): file does not exist, raised also on missing dest parent dir
        if e.errno != errno.ENOENT:
            raise
        # try creating parent directories
        os.makedirs(dst_path)
        shutil.copy(src, dst)

print('Copy data for validation')
for item in val_list:
    exist = 0

    for v in ext:
        video = 'v_' + item[0] + '.' + v
        src = data_path + video
        if os.path.exists(src):
            exist = 1
            break

    dst_path = val_path + item[1] + '/'
    dst = dst_path + video

    print("Copying validation set from [" + src + "]" + " to " + "[" + dst + "]" )

    try:
        shutil.copy(src, dst)
    except IOError as e:
        # ENOENT(2): file does not exist, raised also on missing dest parent dir
        if e.errno != errno.ENOENT:
            raise
        # try creating parent directories
        os.makedirs(dst_path)
        #os.makedirs(os.path.dirname(dst))
        shutil.copy(src, dst)

print('Copy data for testing')
for item in test_list:
    exist = 0

    for v in ext:
        video = 'v_' + item + '.' + v
        src = data_path + video
        if os.path.exists(src):
            exist = 1
            break

    dst = test_path + video

    print("Copying testing set from [" + src + "]" + " to " + "[" + dst + "]" )

    try:
        shutil.copy(src, dst)
    except IOError as e:
        # ENOENT(2): file does not exist, raised also on missing dest parent dir
        if e.errno != errno.ENOENT:
            raise
        # try creating parent directories
        os.makedirs(test_path)
        shutil.copy(src, dst)
