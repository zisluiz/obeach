# -*- coding: utf-8 -*-

import unittest
from ctypes import create_string_buffer

from core.segmentation import Segmentation
from core.parameter import Parameter
# from core.frame import RGBDFrame
from lib.graph_canny_segm import GraphCannySegm
import random
import cv2

class BasicTestSuite(unittest.TestCase):

    def test_absolute_truth_and_meaning(self):
        #dataset_path = '/home/zis/dev/datasets/putkk/Dataset_1_Kin_2'
        dataset_path = '/media/zis/Dados/dev/datasets/putkk.poznan/Dataset_1_Kin_2'

        seg = Segmentation(Parameter())
        graphCannySegm = GraphCannySegm()
        numObjects = create_string_buffer(3)

        for i in range(0, 10):
            filenameRGB = dataset_path + '/rgb/rgb_'+format(i, '05')+'.png'
            filenameDepth = dataset_path + '/depth/depth_' + format(i, '05') + '.png'
            # print(dataset_path + filenameRGB)
            # frame = RGBDFrame(cv2.imread(dataset_path + filenameRGB, cv2.IMREAD_COLOR), None)
            # seg.process(frame)

            results = graphCannySegm.segmentImage(filenameRGB, filenameDepth, False, False, numObjects)
            print 'Num objects', numObjects.value

            """
            for i in range(int(numObjects.value)):
                obj = results[i]
                print('Object id: ', obj.id, ' número de pontos: ',obj.pointsLength)
                for j in range(obj.pointsLength):
                    print(j, obj.points[j].x, obj.points[j].y, obj.points[j].z)
            """
            img = cv2.imread(filenameRGB, cv2.IMREAD_COLOR)
            r = lambda: random.randint(0, 255)

            for i in range(int(numObjects.value)):
                obj = results[i]
                red = r()
                green = r()
                blue = r()
                for j in range(obj.pointsLength):
                    point = obj.points[j]
                    img[point.y, point.x] = (red, green, blue)

            cv2.imshow('title', img)
            graphCannySegm.cleanupObjects(results.contents, numObjects)
            cv2.waitKey(0)
            break



        print 'Test finished!'

if __name__ == '__main__':
    unittest.main()