# -*- coding: utf-8 -*-

import unittest
import cv2
from core.segmentation import Segmentation
from core.parameter import Parameter
from core.frame import RGBDFrame

class BasicTestSuite(unittest.TestCase):
    """Basic test cases."""

    def test_absolute_truth_and_meaning(self):
        dataset_path = '../dataset/Dataset_1_Kin_2'

        seg = Segmentation(Parameter())

        for i in range(0, 10):
            filenameRGB = '/rgb/rgb_'+format(i, '05')+'.png'
            print(dataset_path + filenameRGB)
            frame = RGBDFrame(cv2.imread(dataset_path + filenameRGB, cv2.IMREAD_COLOR), None)
            seg.process(frame)

if __name__ == '__main__':
    unittest.main()