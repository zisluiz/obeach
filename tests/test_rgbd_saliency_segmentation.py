# -*- coding: utf-8 -*-

import unittest
from core.parameter import *
from core.fakedevice import *
from core.rgbd_segmentation import RGBDSegmentation
from core.parameter import Parameter
from core.frame import *


class RgbdSaliencyTestSuite(unittest.TestCase):

    def test_print_result(self):
        device = FakeDevice(SourceType.IMAGE, 'dataset/png/')
        parameter = Parameter(Segmentation.RGBD_SALIENCY, os.getcwd()+'/results/rgbd_saliency/')
        seg = RGBDSegmentation(parameter)
        directory_rgb = device.datasetPath + 'rgb/'
        directory_depth = device.datasetPath + 'depth/'
        frame = RGBDFrame(RGBFrame(directory_rgb, 'demo1.png'), DepthFrame(directory_depth, 'demo1.png'))
        seg.process(frame)
        seg.print_results()
        seg.finish()

        frame = RGBDFrame(RGBFrame(directory_rgb, 'demo3.png'), DepthFrame(directory_depth, 'demo3.png'))
        seg.process(frame)
        seg.print_results()
        seg.finish()

    def test_write_result(self):
        device = FakeDevice(SourceType.IMAGE, 'dataset/png/')
        parameter = Parameter(Segmentation.RGBD_SALIENCY, os.getcwd()+'/results/rgbd_saliency/')
        seg = RGBDSegmentation(parameter)
        directory_rgb = device.datasetPath + 'rgb/'
        directory_depth = device.datasetPath + 'depth/'
        frame = RGBDFrame(RGBFrame(directory_rgb, 'demo1.png'), DepthFrame(directory_depth, 'demo1.png'))
        seg.process(frame)
        seg.write_results()
        seg.finish()

        frame = RGBDFrame(RGBFrame(directory_rgb, 'demo3.png'), DepthFrame(directory_depth, 'demo3.png'))
        seg.process(frame)
        seg.write_results()
        seg.finish()


if __name__ == '__main__':
    Logger.init()
    unittest.main()
    Logger.info('Test finished!')
