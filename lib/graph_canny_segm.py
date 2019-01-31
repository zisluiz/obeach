"""foo.py - a simple demo of importing a calss from C++"""
import ctypes

lib = ctypes.cdll.LoadLibrary('/home/zis/dev/code/obeach/lib/graph-canny-segm.so')

class GraphCannySegm(object):
    """The Foo class supports two methods, bar, and foobar..."""
    def __init__(self):
        lib.Facade_new.argtypes = []
        lib.Facade_new.restype = ctypes.c_void_p

        lib.Facade_segmentImage.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_bool, ctypes.c_bool, ctypes.c_char_p]
        lib.Facade_segmentImage.restype = ctypes.c_void_p

        self.obj = lib.Facade_new()


    def segmentImage(self, rgbFilePath, depthFilePath, showDebug, showImage, jsonBuffer):
        lib.Facade_segmentImage(self.obj, rgbFilePath, depthFilePath, showDebug, showImage, jsonBuffer)
