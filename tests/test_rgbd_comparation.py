# -*- coding: utf-8 -*-

import unittest
from core.parameter import *
from core.fakedevice import *
from util.log import Logger
from core.rgbd_segmentation import RGBDSegmentation
from core.parameter import Parameter
from core.frame import *


class RgbdComparationTestSuite(unittest.TestCase):

    def test_print_result(self):
        device = FakeDevice(SourceType.IMAGE, 'dataset/png/')
        # device = FakeDevice(SourceType.IMAGE, '/media/zis/Dados/dev/datasets/putkk.poznan/Dataset_1_Kin_2')

        algorithms = []
        algorithms.append(RGBDSegmentation(Parameter(Segmentation.GRAPH_CANNY, os.getcwd()+'/results/graph_canny/', resize=(640, 360), fix_proportion=False)))
        #algorithms.append(RGBDSegmentation(Parameter(Segmentation.RGBD_SALIENCY, os.getcwd() + '/results/rgbd_saliency/', resize=(324, 324))))
        #algorithms.append(RGBDSegmentation(Parameter(Segmentation.FCN_TENSORFLOW, os.getcwd() + '/results/fcn_tensorflow/', resize=(224, 224))))
        #algorithms.append(RGBDSegmentation(Parameter(Segmentation.FUSENET, os.getcwd() + '/results/fusenet/', resize=(224, 224))))

        directory_rgb = device.datasetPath + 'rgb/'
        directory_depth = device.datasetPath + 'depth/'

        for algorithm in algorithms:
            Logger.info('############# Testing algorithm '+str(algorithm.parameter.segmentation))
            for i in range(0, 10):
                frame = RGBDFrame(RGBFrame(directory_rgb, 'rgb_'+format(i, '05')+'.png'), DepthFrame(directory_depth, 'depth_' + format(i, '05') + '.png'))

                algorithm.process(frame)
                algorithm.write_results()
                algorithm.finish()
                #break

            algorithm.release()
            break


if __name__ == '__main__':
    Logger.init()
    unittest.main()
    Logger.info('Test finished!')
