from enum import Enum
import os


class Segmentation(Enum):
    GRAPH_CANNY = 1
    CPF = 2
    FOUR_D_SEG = 3
    RGBD_SALIENCY = 4
    FCN_TENSORFLOW = 5
    FUSENET = 6


class Parameter(object):

    def __init__(self, segmentation, output_dir, resize=None, fix_proportion=True, ops=20):
        self.segmentation = segmentation
        self.outputDir = output_dir
        self.resize = resize
        self.fix_proportion = fix_proportion
        self.ops = ops

        if not os.path.exists(self.outputDir):
            os.makedirs(self.outputDir)
