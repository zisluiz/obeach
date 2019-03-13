#!/usr/bin/python
# -*- coding: utf-8 -*-
import cv2
import random
import os
from core.parameter import Segmentation
from lib.graph_canny_segm import GraphCannySegm
from util.log import Logger
from util.timeelapsed import TimeElapsed
from ctypes import create_string_buffer
# import sys
# sys.path.append('/usr/local/lib/python2.7/dist-packages/cv2/python-2.7/')
# sys.path.append('/usr/local/python/cv2/python-2.7')


class RGBDSegmentation(object):
    def __init__(self, parameter):
        self.parameter = parameter
        self.numObjects = create_string_buffer(3)
        self.algorithmSegmentation = None
        self.lastProcessedFrame = None
        self.results = None
        self.r = lambda: random.randint(0, 255)
        if self.parameter.segmentation.__eq__(Segmentation.GRAPH_CANNY):
            self.algorithmSegmentation = GraphCannySegm()
        else:
            raise ValueError('Segmentation options not supported: '+self.parameter.segmentation.name+'.')

    def process(self, frame):
        time_elapsed = TimeElapsed()
        self.lastProcessedFrame = frame
        Logger.info('Processing frame - RGB: ' + frame.rgbFrame.getFilePath() + ', Depth: '+frame.depthFrame.getFilePath())
        self.results = self.algorithmSegmentation.segment_image(frame.rgbFrame.getFilePath(),
                        frame.depthFrame.getFilePath(), False, False, self.numObjects)
        Logger.info('Objects segmented: ' + str(self.get_num_objects()))
        time_elapsed.printTimeElapsed()

    def print_results(self):
        for i in range(self.get_num_objects()):
            obj = self.results[i]
            Logger.info('Object id: ' + str(obj.id) + ', número de pontos: ' + str(obj.pointsLength))
            for j in range(obj.pointsLength):
                Logger.info('Ponto ' + str(j) + ' - x: ' + str(obj.points[j].x) + ' y: ' + str(obj.points[j].y) + ' z: ' + str(obj.points[j].z))

    def show_results(self):
            img = self.write_objects()
            cv2.imshow('image', img)
            cv2.waitKey(0)
            # cv2.destroyAllWindows()

    def write_results(self):
        time_elapsed = TimeElapsed()
        img = self.write_objects()
        Logger.info('Saving result to ' + self.parameter.outputDir+self.lastProcessedFrame.rgbFrame.fileName)

        if not os.path.exists(self.parameter.outputDir):
            os.makedirs(self.parameter.outputDir)

        cv2.imwrite(self.parameter.outputDir+self.lastProcessedFrame.rgbFrame.fileName, img)
        time_elapsed.printTimeElapsed()

    def write_objects(self):
        img = cv2.imread(self.lastProcessedFrame.rgbFrame.getFilePath(), cv2.IMREAD_COLOR)

        for i in range(int(self.get_num_objects())):
            obj = self.results[i]
            red = self.r()
            green = self.r()
            blue = self.r()
            for j in range(obj.pointsLength):
                point = obj.points[j]
                img[point.y, point.x] = (red, green, blue)
        return img

    def finish(self):
        Logger.info('Finishing segmentation')
        self.algorithmSegmentation.cleanup_objects(self.results.contents, self.numObjects)

    def get_num_objects(self):
        return int(self.numObjects.value)

