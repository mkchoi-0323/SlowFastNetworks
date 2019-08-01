params = dict()

params['num_classes'] = 27
params['dataset'] = '/raid/HuToM/201906_Gastric/ARMES/training_190709/2.0/armes_all'

params['epoch_num'] = 40
params['batch_size'] = 80
params['step'] = 15
params['num_workers'] = 4
params['learning_rate'] = 1e-3
params['momentum'] = 0.9
params['weight_decay'] = 1e-5
params['display'] = 10
params['pretrained'] ='pretrained/clip_len_90frame_sample_rate_3_checkpoint_125.pth.tar'
#params['pretrained'] = None
params['gpu'] = [0,1,2,3]
params['log'] = 'phase_log'
params['save_path'] = 'phase_model_save'
params['clip_len'] = 30
params['frame_sample_rate'] = 1
