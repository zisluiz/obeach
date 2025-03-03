# -*- coding: utf-8 -*-

import unittest
from core.parameter import *
from core.fakedevice import *
from util.log import Logger
from core.rgbd_segmentation import RGBDSegmentation
from core.parameter import Parameter
from core.frame import *


class GraphCannySegTestSuite(unittest.TestCase):

    def test_print_result(self):
        device = FakeDevice(SourceType.IMAGE, 'dataset/png/')
        parameter = Parameter(Segmentation.GRAPH_CANNY, os.getcwd()+'/results/graph_canny/', resize=(640, 360))
        seg = RGBDSegmentation(parameter)
        directory_rgb = device.datasetPath + 'rgb/'
        directory_depth = device.datasetPath + 'depth/'

        for i in range(0, 10):
            frame = RGBDFrame(RGBFrame(directory_rgb, 'rgb_'+format(i, '05')+'.png'), DepthFrame(directory_depth, 'depth_' + format(i, '05') + '.png'))
            seg.process(frame)
            seg.print_results()
            seg.finish()

    def test_write_result(self):
        device = FakeDevice(SourceType.IMAGE, 'dataset/png/')
        parameter = Parameter(Segmentation.GRAPH_CANNY, os.getcwd()+'/results/graph_canny/', resize=(640, 360))
        seg = RGBDSegmentation(parameter)
        directory_rgb = device.datasetPath + 'rgb/'
        directory_depth = device.datasetPath + 'depth/'

        for i in range(0, 10):
            frame = RGBDFrame(RGBFrame(directory_rgb, 'rgb_'+format(i, '05')+'.png'), DepthFrame(directory_depth, 'depth_' + format(i, '05') + '.png'))
            seg.process(frame)
            seg.write_results()
            seg.finish()


if __name__ == '__main__':
    Logger.init()
    unittest.main()
    Logger.info('Test finished!')
