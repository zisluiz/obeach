# -*- coding: utf-8 -*-

import unittest
from core.parameter import *
from core.fakedevice import *
from util.log import Logger
from core.rgbd_segmentation import RGBDSegmentation
from core.parameter import Parameter
from core.frame import *


class FusenetTestSuite(unittest.TestCase):

    def test_print_result(self):
        device = FakeDevice(SourceType.IMAGE, 'dataset/png/')
        parameter = Parameter(Segmentation.FUSENET, os.getcwd()+'/results/fusenet/', resize=(224, 224))
        seg = RGBDSegmentation(parameter)
        directory_rgb = device.datasetPath + 'rgb/'
        directory_depth = device.datasetPath + 'depth/'

        frame = RGBDFrame(RGBFrame(directory_rgb, 'inp_5.png'), DepthFrame(directory_depth, 'gt_5.png'))
        seg.process(frame)
        #seg.print_results()
        seg.finish()

        frame = RGBDFrame(RGBFrame(directory_rgb, 'inp_6.png'), DepthFrame(directory_depth, 'gt_6.png'))
        seg.process(frame)
        #seg.print_results()
        seg.finish()

        frame = RGBDFrame(RGBFrame(directory_rgb, '8.png'), DepthFrame(directory_depth, '8.png'))
        seg.process(frame)
        #seg.print_results()
        seg.finish()

    def test_write_result(self):
        device = FakeDevice(SourceType.IMAGE, 'dataset/png/')
        parameter = Parameter(Segmentation.FUSENET, os.getcwd()+'/results/fusenet/')
        seg = RGBDSegmentation(parameter)
        directory_rgb = device.datasetPath + 'rgb/'
        directory_depth = device.datasetPath + 'depth/'
        frame = RGBDFrame(RGBFrame(directory_rgb, 'inp_5.png'), DepthFrame(directory_depth, 'gt_5.png'))
        seg.process(frame)
        seg.write_results()
        seg.finish()

        frame = RGBDFrame(RGBFrame(directory_rgb, 'inp_6.png'), DepthFrame(directory_depth, 'gt_6.png'))
        seg.process(frame)
        seg.write_results()
        seg.finish()

        frame = RGBDFrame(RGBFrame(directory_rgb, '8.png'), DepthFrame(directory_depth, '8.png'))
        seg.process(frame)
        seg.write_results()
        seg.finish()


if __name__ == '__main__':
    Logger.init()
    unittest.main()
    Logger.info('Test finished!')
