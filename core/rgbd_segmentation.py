#!/usr/bin/python
# -*- coding: utf-8 -*-
import cv2
import random
import os
import numpy as np
from core.parameter import Segmentation
from core.frame import DepthFrame
from lib.alg_graph_canny_segm import GraphCannySegm
from lib.alg_rgbd_saliency import RgbdSaliency
from lib.alg_fcn_tensorflow import FcnTensorflow
from lib.alg_fusenet_pytorch import Fusenet
from util.log import Logger
from util.timeelapsed import TimeElapsed


class RGBDSegmentation(object):
    def __init__(self, parameter):
        self.parameter = parameter
        self.algorithmSegmentation = None
        self.lastProcessedFrame = None
        self.results = None
        self.processedRgbImage = None
        self.processedDepthImage = None
        self.r = lambda: random.randint(0, 255)
        if self.parameter.segmentation == Segmentation.GRAPH_CANNY:
            self.algorithmSegmentation = GraphCannySegm()
        elif self.parameter.segmentation == Segmentation.RGBD_SALIENCY:
            self.algorithmSegmentation = RgbdSaliency()
        elif self.parameter.segmentation == Segmentation.FCN_TENSORFLOW:
            self.algorithmSegmentation = FcnTensorflow()
        elif self.parameter.segmentation == Segmentation.FUSENET:
            self.algorithmSegmentation = Fusenet()
        else:
            raise ValueError('Segmentation options not supported: '+self.parameter.segmentation.name+'.')

    def process(self, frame):
        time_elapsed = TimeElapsed()
        self.lastProcessedFrame = frame
        Logger.info('Processing frame - RGB: ' + frame.rgbFrame.getFilePath() + ', Depth: '+frame.depthFrame.getFilePath())
        self.processedRgbImage = self.get_image(frame.rgbFrame)
        self.processedDepthImage = self.get_image(frame.depthFrame)
        self.results = self.algorithmSegmentation.segment_image(self.processedRgbImage, self.processedDepthImage)
        Logger.info('Objects segmented: ' + str(self.algorithmSegmentation.get_num_objects()))
        time_elapsed.printTimeElapsed('Total segmentation - ')

    def print_results(self):
        for i in range(self.algorithmSegmentation.get_num_objects()):
            obj = self.results[i]
            if self.algorithmSegmentation.python_segmentation:
                Logger.info('Object id: ' + str(obj.id) + ', número de pontos: ' + str(len(obj.pointsList)))
                for j in range(len(obj.pointsList)):
                    Logger.info('Ponto ' + str(j) + ' - x: ' + str(obj.pointsList[j].x) + ' y: ' + str(obj.pointsList[j].y) + ' z: ' + str(obj.pointsList[j].z))
            else:
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
        time_elapsed.printTimeElapsed('Total writing file - ')

    def write_labels_to_file(self, fileName, colored):
        time_elapsed = TimeElapsed()
        img = self.write_objects_to_label(colored)
        Logger.info('Saving result to ' + fileName)

        cv2.imwrite(fileName, img)
        time_elapsed.printTimeElapsed('Total writing file - ')

    def write_objects(self):
        img = self.get_image(self.lastProcessedFrame.rgbFrame)

        for i in range(int(self.algorithmSegmentation.get_num_objects())):
            obj = self.results[i]
            red = self.r()
            green = self.r()
            blue = self.r()

            if self.algorithmSegmentation.python_segmentation:
                for j in range(len(obj.pointsList)):
                    point = obj.pointsList[j]
                    img[point.y, point.x] = (red, green, blue)
            else:
                for j in range(obj.pointsLength):
                    point = obj.points[j]
                    img[point.y, point.x] = (red, green, blue)

        return img

    def write_objects_to_label(self, colored):
        h, w, c = self.processedRgbImage.shape
        img = np.zeros( (h, w, 3) if colored else (h, w), np.uint8)

        for i in range(int(self.algorithmSegmentation.get_num_objects())):
            obj = self.results[i]

            color = (self.r(), self.r(), self.r()) if colored else i

            if self.algorithmSegmentation.python_segmentation:
                for j in range(len(obj.pointsList)):
                    point = obj.pointsList[j]
                    img[point.y, point.x] = color
            else:
                for j in range(obj.pointsLength):
                    point = obj.points[j]
                    img[point.y, point.x] = color

        return img

    def finish(self):
        Logger.info('Finishing segmentation')
        if self.algorithmSegmentation.python_segmentation:
            self.algorithmSegmentation.cleanup_objects(self.results)
        else:
            self.algorithmSegmentation.cleanup_objects(self.results)

    def get_image(self, rgbFrame):
        image = None
        imagePath = rgbFrame.directory
        isdepth = isinstance(rgbFrame, DepthFrame)

        if isdepth:
            if self.algorithmSegmentation.depth_image_colored:
                image = rgbFrame.getImage(False, True)
            elif not self.algorithmSegmentation.depth_image_grayscale:
                image = rgbFrame.getImage(False)

        if image is None:
            image = rgbFrame.getImage()

        if "active_vision" in imagePath or "putkk" in imagePath:
            image = image[0:1080, 419:1499]

        if self.parameter.resize is not None:
            image = self.fix_proportion(image)
            return cv2.resize(image, self.parameter.resize)
        elif self.parameter.scale is not None:
            image = cv2.resize(image, (int(image.shape[1] / self.parameter.scale), int(image.shape[0] / self.parameter.scale)))
            #cv2.imwrite('results/scale/' + ('d_' if isdepth else 'r_') + rgbFrame.fileName, image)
            return image
        else:
            return image

    def fix_proportion(self, image):
        if not self.parameter.fix_proportion:
            return image

        if image.shape[0] > image.shape[1]:
            diff = image.shape[0] - image.shape[1]
            crop_img = image[int(diff/2):int(image.shape[0]-(diff/2)), 0:image.shape[1]]
            return crop_img
        elif image.shape[0] < image.shape[1]:
            diff = image.shape[1] - image.shape[0]
            crop_img = image[0:image.shape[0], int(diff/2):int(image.shape[1]-(diff/2))]
            return crop_img
        else:
            return image

    def release(self):
        self.algorithmSegmentation.release()

