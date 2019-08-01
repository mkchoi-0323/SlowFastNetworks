params = dict()

params['num_classes'] = 200
params['batch_size'] = 1
params['num_workers'] = 0
params['model'] ='models/clip_len_30_fsr_1_ckpt_53_res50.pth.tar'
params['gpu'] = [6]
params['clip_len'] = 30
params['frame_sample_rate'] = 1
params['log'] = 'log_test'

