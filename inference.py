import os
import sys
import time
import glob
import numpy as np
import torch
from config_test import params
from torch import nn, optim
from torch.utils.data import DataLoader
import torch.backends.cudnn as cudnn
from lib.dataset_test import VideoDataset
from lib import slowfastnet
from tensorboardX import SummaryWriter
from moviepy.video.io.VideoFileClip import VideoFileClip

class AverageMeter(object):
    """Computes and stores the average and current value"""
    def __init__(self):
        self.reset()

    def reset(self):
        self.test = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def update(self, test, n=1):
        self.test = test
        self.sum += test * n
        self.count += n
        self.avg = self.sum / self.count

def accuracy(output, target, topk=(1,)):
    """Computes the precision@k for the specified values of k"""
    maxk = max(topk)
    batch_size = target.size(0)

    _, pred = output.topk(maxk, 1, True, True)
    pred = pred.t()
    correct = pred.eq(target.view(1, -1).expand_as(pred))

    res = []
    for k in topk:
        correct_k = correct[:k].view(-1).float().sum(0)
        res.append(correct_k.mul_(100.0 / batch_size))
    return res

def test(model, test_dataloader, writer):
    batch_time = AverageMeter()
    data_time = AverageMeter()

    model.eval()

    end = time.time()
    with torch.no_grad():
        for step, inputs in enumerate(test_dataloader):
            data_time.update(time.time() - end)
            inputs = inputs.cuda()
            feature = model(inputs)
            feature = feature.cpu().numpy()
            feature_up = np.zeros((1,400))
            idx = 0 
            for val in feature[0]:
                feature_up[0][idx*2] = feature[0][idx]
                if idx == 199:
                    feature_up[0][idx*2+1] = (feature[0][idx] + feature[0][idx]) / 2
                else:
                    feature_up[0][idx*2+1] = (feature[0][idx] + feature[0][idx+1]) / 2
                idx = idx + 1

            # measure accuracy and record loss
            batch_time.update(time.time() - end)
            end = time.time()
            
            print('----test----')
            print_string = 'data_time: {data_time:.3f}, batch time: {batch_time:.3f}'.format(
                data_time=data_time.test,
                batch_time=batch_time.test)
            print(print_string)
            break

    return feature, feature_up

def main():
    cudnn.benchmark = False
    cur_time = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
    logdir = os.path.join(params['log'], cur_time)
    data_path = '/raid/ActivityNet/Videos/'
    tmp_path = '/home/nvadmin/tmp/'
    feature_path = '/home/nvadmin/SlowFastNetworks/feature/'
    feature_up_path = '/home/nvadmin/SlowFastNetworks/feature_up/'
    sec = 1.0

    if not os.path.exists(logdir):
        os.makedirs(logdir)

    writer = SummaryWriter(log_dir=logdir)

    print("load model")
    model = slowfastnet.resnet50(class_num=params['num_classes'])
    #model = slowfastnet.resnet200(class_num=params['num_classes'])

    pretrained_dict = torch.load(params['model'], map_location='cpu')
    try:
        model_dict = model.module.state_dict()
    except AttributeError:
        model_dict = model.state_dict()
    pretrained_dict = {k: v for k, v in pretrained_dict.items() if k in model_dict}
    model_dict.update(pretrained_dict)
    model.load_state_dict(model_dict)

    model = model.cuda(params['gpu'][0])
    model = nn.DataParallel(model, device_ids=params['gpu'])  # multi-Gpu

    list_filter = data_path + '*.mp4'
    video_list = glob.glob(list_filter)
    
    print("Testing videos")
    s_video = 18000
    v_idx = 0
    e_video = 19993

    for video_path in video_list[s_video:e_video]:
        c_index = s_video + v_idx
        fname = video_path.split('.')
        fname = fname[0].split('/')[-1]
        idx = 0
        with VideoFileClip(video_path) as video:
            duration = video.duration
            n_segments = int(duration // sec)
            for i in range(0, n_segments-1):
                start = i
                end = i + sec
                trim = video.subclip(start, end)
                dst = tmp_path + fname + '.mp4'
                print("Start video idx [" + str(s_video) + "], current idx [" + str(c_index) + "], last video idx [" + str(e_video) + "]")
                print("Write video to [" + dst + "] with duration [" + str(start) + "] and [" + str(end) + "]")
                trim.write_videofile(dst, audio=False)

                print("Load inference video")
                test_dataloader = \
                    DataLoader(
                        VideoDataset(dst, clip_len=params['clip_len'], frame_sample_rate=params['frame_sample_rate']),
                        batch_size=params['batch_size'], shuffle=False, num_workers=params['num_workers'])
            
                feature, feature_up = test(model, test_dataloader, writer)
                if idx == 0:
                    video_feature = feature
                    video_feature_up = feature_up
                else:
                    video_feature = np.concatenate((video_feature, feature), axis=0)
                    video_feature_up = np.concatenate((video_feature_up, feature_up), axis=0)

                idx = idx + 1

                print(video_feature.shape, video_feature_up.shape)

        if not os.path.isdir(feature_path):
            os.makedirs(feature_path)
        if not os.path.isdir(feature_up_path):
            os.makedirs(feature_up_path)

        save_path = feature_path + fname + ".csv"
        np.savetxt(save_path, video_feature, delimiter=",")
        save_up_path = feature_up_path + fname + ".csv"
        np.savetxt(save_up_path, video_feature_up, delimiter=",")
        v_idx = v_idx+1


    writer.close

if __name__ == '__main__':
    main()
