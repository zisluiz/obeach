#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

#sys.path.append('/usr/local/lib/python2.7/dist-packages/cv2/python-2.7/')
sys.path.append('/usr/local/python/cv2/python-2.7')
import cv2
import random
import os
from util.log import Logger
from util.timeelapsed import TimeElapsed
from ctypes import create_string_buffer

class Segmentation(object):
    def __init__(self, parameter):
        self.parameter = parameter
        self.numObjects = create_string_buffer(3)
        self.r = lambda: random.randint(0, 255)

    def process(self, frame):
        timeElapsed = TimeElapsed()
        self.lastProcessedFrame = frame
        Logger.info('Processing frame - RGB: ' + frame.rgbFrame.getFilePath() + ', Depth: '+frame.depthFrame.getFilePath())
        self.results = self.parameter.tecnique.segmentImage(frame.rgbFrame.getFilePath(),
                        frame.depthFrame.getFilePath(), False, False, self.numObjects)
        Logger.info('Objects segmented: ' + str(self.getNumObjects()))
        timeElapsed.printTimeElapsed()

    def printResults(self):
        for i in range(self.getNumObjects()):
            obj = self.results[i]
            print('Object id: ', obj.id, ' número de pontos: ', obj.pointsLength)
            for j in range(obj.pointsLength):
                print(j, obj.points[j].x, obj.points[j].y, obj.points[j].z)

    def showResults(self):
            img = self.writeObjects()
            cv2.imshow('image', img)
            cv2.waitKey(0)
            #cv2.destroyAllWindows()

    def writeResults(self):
            timeElapsed = TimeElapsed()
            img = self.writeObjects()
            Logger.info('Saving result to ' + self.parameter.outputDir+self.lastProcessedFrame.rgbFrame.fileName)

            if not os.path.exists(self.parameter.outputDir):
                os.makedirs(self.parameter.outputDir)

            cv2.imwrite(self.parameter.outputDir+self.lastProcessedFrame.rgbFrame.fileName, img)
            timeElapsed.printTimeElapsed()

    def writeObjects(self):
        img = cv2.imread(self.lastProcessedFrame.rgbFrame.getFilePath(), cv2.IMREAD_COLOR)

        for i in range(int(self.getNumObjects())):
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
        self.parameter.tecnique.cleanupObjects(self.results.contents, self.numObjects)

    def getNumObjects(self):
        return int(self.numObjects.value)

