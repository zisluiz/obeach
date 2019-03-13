from enum import Enum
from util.log import Logger
from core.frame import PCLFrame
import os


class SourceType(Enum):
    IMAGE = 1
    PCL = 2


class FakeDevice(object):

    def __init__(self, source_type=SourceType.IMAGE, dataset_path="", fps=30):
        self.sourceType = source_type
        self.datasetPath = dataset_path
        self.fps = fps
        Logger.info('Dataset path: ' + self.datasetPath)

    def oneFrame(self):
        return PCLFrame(self.datasetPath, os.listdir(self.datasetPath)[0])
