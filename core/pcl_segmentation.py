#!/usr/bin/python
# -*- coding: utf-8 -*-
from util.log import Logger
from util.timeelapsed import TimeElapsed
from lib.cpf_segmentation import CpfSegmentation
from core.parameter import Segmentation
import pcl.pcl_visualization


class PCLSegmentation(object):
    def __init__(self, parameter):
        self.parameter = parameter
        self.algorithmSegmentation = None
        self.lastProcessedFrame = None
        if self.parameter.segmentation.__eq__(Segmentation.CPF):
            self.algorithmSegmentation = CpfSegmentation()
        else:
            raise ValueError('Segmentation options not supported: '+self.parameter.segmentation.name+'.')

    def process(self, frame):
        time_elapsed = TimeElapsed()
        self.lastProcessedFrame = frame
        Logger.info('Processing frame - PCL: ' + frame.getFilePath())
        cloud = pcl.load_XYZRGB(frame.getFilePath())
        self.algorithmSegmentation.segment_image(cloud, True)
        time_elapsed.printTimeElapsed()

    def show_results(self):
        visual = pcl.pcl_visualization.CloudViewing()
        visual.ShowColorCloud(self.results, b'cloud')
        flag = True
        while flag:
            flag != visual.WasStopped()

    def write_results(self):
            timeElapsed = TimeElapsed()
            destiny_file = self.parameter.outputDir+self.lastProcessedFrame.rgbFrame.fileName
            Logger.info('Saving result to ' + destiny_file)
            pcl.save(self.results, destiny_file)
            timeElapsed.printTimeElapsed()

    def finish(self):
        Logger.info('Finishing segmentation')
