import sys

sys.path.append('/usr/local/python/cv2/python-2.7')
import cv2


class Segmentation(object):
    def __init__(self, parameter):
        self.parameter = parameter

    def process(self, frame):
        cv2.imshow('image', frame.rgbImage)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
