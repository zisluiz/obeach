# -*- coding: utf-8 -*-

import unittest
import cv2
from core.segmentation import Segmentation
from core.parameter import Parameter
from core.object import Object
# from core.frame import RGBDFrame
from lib.graph_canny_segm import GraphCannySegm
import json
import zlib
from ctypes import *
import random

class BasicTestSuite(unittest.TestCase):

    def test_absolute_truth_and_meaning(self):
        dataset_path = '/home/zis/dev/datasets/putkk/Dataset_1_Kin_2'

        seg = Segmentation(Parameter())
        graphCannySegm = GraphCannySegm()

        for i in range(0, 10):
            filenameRGB = dataset_path + '/rgb/rgb_'+format(i, '05')+'.png'
            filenameDepth = dataset_path + '/depth/depth_' + format(i, '05') + '.png'
            # print(dataset_path + filenameRGB)
            # frame = RGBDFrame(cv2.imread(dataset_path + filenameRGB, cv2.IMREAD_COLOR), None)
            # seg.process(frame)
            resultsCharArray = create_string_buffer(1000000)
            graphCannySegm.segmentImage(filenameRGB, filenameDepth, False, False, resultsCharArray)
            #results = zlib.decompress(resultsCharArray.value, -zlib.MAX_WBITS)
            results = resultsCharArray.value
            print 'Process finished'
            print 'Results: ' + results
            objects = json.loads(results)

            """
            img = cv2.imread(filenameRGB, cv2.IMREAD_COLOR)
            r = lambda: random.randint(0, 255)

            for obj in objects:
                red = r()
                green = r()
                blue = r()
                #print 'Setting obj: ', obj['id']
                for point in obj['points']:
                    #print 'Point-x: ', point['x']
                    #print 'Point-y: ', point['y']
                    img[point['y'], point['x']] = (red, green, blue)


            cv2.imshow('title', img)
            cv2.waitKey(0)
            break"""


if __name__ == '__main__':
    unittest.main()