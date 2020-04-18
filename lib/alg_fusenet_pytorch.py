from lib.fusenet.options.test_options import TestOptions
from lib.fusenet.data import CreateDataLoader
from lib.fusenet.models import create_model
import cv2
import os
import torch
import numpy as np
from torchvision import transforms
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
        opt.no_flip = False  # no flip
        opt.display_id = -1  # no visdom display
        opt.dataset_mode = 'sunrgbd'
        opt.dataset = 'sunrgbd'
        opt.name = 'sunrgbd'
        opt.epoch = '400'
        opt.parse()

        data_loader = CreateDataLoader(opt)
        dataset = data_loader.load_data()
        dataset.ignore_label = 1
        self.model = create_model(opt, dataset.dataset)
        self.model.setup(opt)
        self.model.load_networks(opt.epoch)
        self.model.eval()
        self.num_objects = 0


    def segment_image(self, rgb_image, depth_image):
        test_transforms = transforms.Compose([transforms.ToTensor()])
        rgb_image = test_transforms(rgb_image).float().unsqueeze(0)
        depth_image = test_transforms(depth_image).float().unsqueeze(0)

        pred = self.predict_image(rgb_image, depth_image)
        objs = self.to_objects(pred)
        self.num_objects = len(objs)
        return objs

    def cleanup_objects(self, results):
        results.clear()

    def predict_image(self, rgb, depth):
        input = {'rgb_image': rgb, 'depth_image': depth}
        self.model.set_input(input)
        self.model.forward()

        _, pred = torch.max(self.model.output.data.cpu(), 1)
        pred = pred.float().detach().int().numpy()
        return pred.reshape(224, 224)

    def get_num_objects(self):
        return self.num_objects

    def release(self):
        return

