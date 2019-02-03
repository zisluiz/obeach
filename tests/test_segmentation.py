# -*- coding: utf-8 -*-

import unittest

from core.segmentation import Segmentation
from core.parameter import Parameter
from core.frame import *
from util.log import Logger
from lib.graph_canny_segm import GraphCannySegm
import os

class BasicTestSuite(unittest.TestCase):

    def test_absolute_truth_and_meaning(self):
        #dataset_path = '/home/zis/dev/datasets/putkk/Dataset_1_Kin_2'
        dataset_path = '/media/zis/Dados/dev/datasets/putkk.poznan/Dataset_1_Kin_2'
        Logger.info('Dataset path: '+dataset_path)

        parameter = Parameter()
        parameter.tecnique = GraphCannySegm()
        parameter.outputDir = os.getcwd()+'/results/'
        seg = Segmentation(parameter)
        directoryRGB =  dataset_path + '/rgb/'
        directoryDepth = dataset_path + '/depth/'

        for i in range(0, 10):
            frame = RGBDFrame(RGBFrame(directoryRGB, 'rgb_'+format(i, '05')+'.png'), RGBFrame(directoryDepth, 'depth_' + format(i, '05') + '.png'))
            seg.process(frame)
            #seg.printResults()
            #seg.showResults()
            seg.writeResults()
            seg.finish()
            break


if __name__ == '__main__':
    Logger.init()
    unittest.main()
    Logger.info('Test finished!')
