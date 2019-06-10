# -*- coding: utf-8 -*-

import unittest
from core.parameter import *
from core.fakedevice import *
from util.log import Logger
from core.rgbd_segmentation import RGBDSegmentation
from core.parameter import Parameter
from core.frame import *
from torchvision import transforms

class RgbdComparationTestSuite(unittest.TestCase):

    def test_print_result(self):
        device = FakeDevice(SourceType.IMAGE, 'dataset/png/')
        # device = FakeDevice(SourceType.IMAGE, '/media/zis/Dados/dev/datasets/putkk.poznan/Dataset_1_Kin_2')

        transformations = transforms.Compose([transforms.Resize((224, 224))])
        #test_transforms = transforms.Compose([transforms.Resize((224, 224))])

        algorithms = []
        #algorithms.append(RGBDSegmentation(Parameter(Segmentation.GRAPH_CANNY, os.getcwd()+'/results/graph_canny/', transforms)))
        #algorithms.append(RGBDSegmentation(Parameter(Segmentation.RGBD_SALIENCY, os.getcwd() + '/results/rgbd_saliency/', transforms)))
        algorithms.append(RGBDSegmentation(Parameter(Segmentation.FCN_TENSORFLOW, os.getcwd() + '/results/fcn_tensorflow/', transformations=transformations)))
        #algorithms.append(RGBDSegmentation(Parameter(Segmentation.FUSENET, os.getcwd() + '/results/fusenet/', transformations=transformations)))

        directory_rgb = device.datasetPath + 'rgb/'
        directory_depth = device.datasetPath + 'depth/'

        for algorithm in algorithms:
            for i in range(0, 10):
                frame = RGBDFrame(RGBFrame(directory_rgb, 'rgb_'+format(i, '05')+'.png'), RGBFrame(directory_depth, 'depth_' + format(i, '05') + '.png'))

                algorithm.process(frame)
                algorithm.print_results()
                algorithm.finish()
                break

            algorithm.release()
"""
    def test_write_result(self):
        device = FakeDevice(SourceType.IMAGE, 'dataset/png/')
        # device = FakeDevice(SourceType.IMAGE, '/media/zis/Dados/dev/datasets/putkk.poznan/Dataset_1_Kin_2')
        parameter = Parameter(Segmentation.GRAPH_CANNY, os.getcwd()+'/results/')
        seg = RGBDSegmentation(parameter)
        directory_rgb = device.datasetPath + 'rgb/'
        directory_depth = device.datasetPath + 'depth/'

        for i in range(0, 10):
            frame = RGBDFrame(RGBFrame(directory_rgb, 'rgb_'+format(i, '05')+'.png'), RGBFrame(directory_depth, 'depth_' + format(i, '05') + '.png'))
            seg.process(frame)
            seg.write_results()
            seg.finish()
            break
"""

if __name__ == '__main__':
    Logger.init()
    unittest.main()
    Logger.info('Test finished!')
