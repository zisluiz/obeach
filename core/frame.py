class RGBFrame(object):

    def __init__(self, directory, fileName):
        self.directory = directory
        self.fileName = fileName

    def getFilePath(self):
        return self.directory + self.fileName


class DepthFrame(object):

    def __init__(self, directory, fileName):
        self.directory = directory
        self.fileName = fileName

    def getFilePath(self):
        return self.directory + self.fileName


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
