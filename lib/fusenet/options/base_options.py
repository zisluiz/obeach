import os
from ..util import util
import torch
from .. import models
from .. import data


class BaseOptions():
    def __init__(self):
        self.initialized = False

    def initialize(self):
        self.dataroot = '' # path to images (should have subfolders trainA, trainB, valA, valB, etc)
        self.batch_size = 4 # input batch size
        self.loadSize = 224 # scale images to this size
        self.fineSize = 224 # then crop to this size
        self.display_winsize = 224 # display window size for both visdom and HTML
        self.gpu_ids = '0' # gpu ids: e.g. 0  0,1,2, 0,2. use -1 for CPU
        self.name = 'experiment_name' # name of the experiment. It decides where to store samples and models
        self.dataset_mode = 'unaligned' # chooses how datasets are loaded. [unaligned | aligned | single]
        self.model ='fusenet' # chooses which model to use.
        #parser.add_argument('--direction', type=str, default='AtoB', help='AtoB or BtoA')
        self.epoch = 'latest' # which epoch to load? set to latest to use latest cached model
        self.num_threads = 8 # threads for loading data
        self.checkpoints_dir = '../lib/fusenet/checkpoints' # models are saved here
        self.norm = 'instance' # instance normalization or batch normalization
        self.serial_batches = True # if true, takes images in order to make batches, otherwise takes them randomly
        self.no_dropout = False # no dropout for the generator
        self.max_dataset_size = "float('inf')" # Maximum number of samples allowed per dataset. If the dataset directory contains more than max_dataset_size, only a subset is loaded.
        self.resize_or_crop = 'none' # scaling and cropping of images at load time [resize_and_crop|crop|scale_width|scale_width_and_crop|none]
        self.no_flip = True # if specified, do not flip the images for data augmentation
        self.init_type = 'kaiming' #n etwork initialization [normal|xavier|kaiming|orthogonal]
        self.init_gain = 0.02 # scaling factor for normal, xavier and orthogonal
        self.verbose = False # if specified, print more debugging information
        self.suffix ='' # customized suffix: opt.name = opt.name + suffix: e.g., {model}_{netG}_size{loadSize}
        self.seed = 0 # seed for random generators
        self.initialized = True

    def gather_options(self):
        # initialize parser with basic options
        if not self.initialized:
            self.initialize()

        # modify model-related parser options
        model_name = self.model
        model_option_setter = models.get_option_setter(model_name)
        parser = model_option_setter(self, self.isTrain)
        opt, _ = parser.parse_known_args()  # parse again with the new defaults

        # modify dataset-related parser options
        dataset_name = opt.dataset_mode
        dataset_option_setter = data.get_option_setter(dataset_name)
        parser = dataset_option_setter(parser, self.isTrain)

    def print_options(self):
        message = ''
        message += '----------------- Options ---------------\n'
        for k, v in sorted(vars(self).items()):
            comment = ''

            message += '{:>25}: {:<30}{}\n'.format(str(k), str(v), comment)
        message += '----------------- End -------------------'
        print(message)

        # save to the disk
        expr_dir = os.path.join(self.checkpoints_dir, self.name)
        util.mkdirs(expr_dir)
        file_name = os.path.join(expr_dir, 'opt.txt')
        with open(file_name, 'wt') as opt_file:
            opt_file.write(message)
            opt_file.write('\n')

    def parse(self):
        self.print_options()

        # set gpu ids
        str_ids = self.gpu_ids.split(',')
        self.gpu_ids = []
        for str_id in str_ids:
            id = int(str_id)
            if id >= 0:
                self.gpu_ids.append(id)
        if len(self.gpu_ids) > 0:
            torch.cuda.set_device(self.gpu_ids[0])

