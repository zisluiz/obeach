import sys
from lib.fusenet.options.test_options import TestOptions
from lib.fusenet.data import CreateDataLoader
from lib.fusenet.models import create_model
from lib.fusenet.util import util
import torch
import numpy as np

import ctypes
import cv2
from torchvision import transforms
from PIL import Image
from lib.algorithm_interface import AlgorithmInterface


class Fusenet(AlgorithmInterface):
    """The Foo class supports two methods, bar, and foobar..."""
    def __init__(self):
        AlgorithmInterface.__init__(self)
        opt = TestOptions()
        opt.initialize()
        # hard-code some parameters for test
        # opt.num_threads = 1   # test code only supports num_threads = 1
        opt.batch_size = 1  # test code only supports batch_size = 1
        opt.serial_batches = True  # no shuffle
        opt.no_flip = True  # no flip
        opt.display_id = -1  # no visdom display
        opt.dataset_mode = 'sunrgbd'
        opt.dataset = 'sunrgbd'
        opt.name = 'sunrgbd'
        opt.epoch = '400'
        opt.parse()

        data_loader = CreateDataLoader(opt)
        dataset = data_loader.load_data()
        dataset.ignore_label = 1
        palet_file = '../lib/fusenet/palette.txt'
        self.impalette = list(np.genfromtxt(palet_file, dtype=np.uint8).reshape(3 * 256))
        self.model = create_model(opt, dataset.dataset)
        self.model.setup(opt)
        self.model.load_networks(opt.epoch)
        self.model.eval()


    def segment_image(self, rgb_image, depth_image, num_objects):
        #rgb_image = Image.open(rgb_file_path)
        #depth_image = Image.open(depth_file_path)
        #rgb_shape = (rgb_image.width,rgb_image.height)

        #test_transforms = transforms.Compose([transforms.Resize((224, 224)),
        #                                      transforms.ToTensor()])
        test_transforms = transforms.Compose([transforms.ToTensor()])
        rgb_image = test_transforms(rgb_image).float().unsqueeze(0)
        depth_image = test_transforms(depth_image).float().unsqueeze(0)

        pred = self.predict_image(rgb_image, depth_image)
        #pred = cv2.resize(pred, rgb_shape)
        objs = self.to_objects(pred)
        num_objects.value = str.encode('{0}'.format(len(objs)))
        return objs


    def cleanup_objects(self, results, num_objects):
        return

    def predict_image(self, rgb, depth):
        input = {'rgb_image': rgb, 'depth_image': depth}
        self.model.set_input(input)
        self.model.forward()

        _, pred = torch.max(self.model.output.data.cpu(), 1)
        #pred = pred.float().detach().int().numpy()
        im = util.tensor2labelim(pred, self.impalette)
        return im



