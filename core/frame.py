import cv2

class RGBFrame(object):

    def __init__(self, directory, fileName):
        self.directory = directory
        self.fileName = fileName

    def getFilePath(self):
        return self.directory + self.fileName

    def getImage(self):
        return cv2.imread(self.getFilePath(), cv2.IMREAD_COLOR)


class DepthFrame(object):

    def __init__(self, directory, fileName):
        self.directory = directory
        self.fileName = fileName

    def getImage(self):
        return cv2.imread(self.getFilePath(), cv2.IMREAD_GRAYSCALE)


class RGBDFrame(object):

    def __init__(self, rgbFrame, depthFrame):
        self.rgbFrame = rgbFrame
        self.depthFrame = depthFrame

class PCLFrame(object):

    def __init__(self, directory, fileName):
        self.directory = directory
        self.fileName = fileName

    def getFilePath(self):
        return self.directory + self.fileName
