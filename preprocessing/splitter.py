import errno
import os
import shutil
import sys

rep = '/home/nvadmin/SlowFastNetworks/'
list_path = rep + 'ucfTrainTestlist/'
train_path = rep + 'UCF-101/train/training/'
val_path = rep + 'UCF-101/train/validation/'
data_path = '/home/nvadmin/video_datasets/UCF101/'
train_split = 'trainlist01.txt'
test_split = 'testlist01.txt'

print('Split for training')
f = open(list_path + train_split, 'r')
lines = f.readlines()
for line in lines:
    line = line.split(' ')
    video_path = line[0]
    video = video_path.split('/')
    video = video[1]
    print(video)
    src = data_path + video

    print(train_path + video_path)
    sys.exit(1)
    try:
        shutil.copy(src, train_path+video_path)
    except IOError as e:
        # ENOENT(2): file does not exist, raised also on missing dest parent dir
        if e.errno != errno.ENOENT:
            raise
        # try creating parent directories
        os.makedirs(os.path.dirname(train_path+video_path))
        shutil.copy(src, train_path+video_path)
    
f.close()

print('Split for validation')
f = open(list_path + test_split, 'r')
lines = f.readlines()
for line in lines:
    #line = line.split('/')
    #video = line[1]
    video_path = line.rstrip()
    video = video_path.split('/')
    video = video[1]
    print(video)
    src = data_path + video
    try:
        shutil.copy(src, val_path+video_path)
    except IOError as e:
        # ENOENT(2): file does not exist, raised also on missing dest parent dir
        if e.errno != errno.ENOENT:
            raise
        # try creating parent directories
        os.makedirs(os.path.dirname(val_path+video_path))
        shutil.copy(src, val_path+video_path)

f.close()
