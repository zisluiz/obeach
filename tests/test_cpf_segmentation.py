# -*- coding: utf-8 -*-

import unittest

from core.pcl_segmentation import PCLSegmentation
from core.parameter import *
from core.fakedevice import *
from util.log import Logger
import os


class BasicTestSuite(unittest.TestCase):

    def test_show_result(self):
        device = FakeDevice(SourceType.PCL, '/media/zis/Dados/dev/code/cpf_segmentation/test_data/')
        parameter = Parameter(Segmentation.CPF, os.getcwd()+'/results/')
        seg = PCLSegmentation(parameter)
        seg.process(device.oneFrame())
        seg.show_results()
        seg.finish()


if __name__ == '__main__':
    Logger.init()
    unittest.main()
    Logger.info('Test finished!')
