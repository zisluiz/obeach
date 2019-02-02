"""foo.py - a simple demo of importing a calss from C++"""
import ctypes
from core.object import Object



lib = ctypes.cdll.LoadLibrary('/media/zis/Dados/dev/Mestrado/codes/obeach/lib/graph-canny-segm.so')

class GraphCannySegm(object):
    """The Foo class supports two methods, bar, and foobar..."""
    def __init__(self):
        lib.Facade_new.argtypes = [ctypes.c_char_p]
        lib.Facade_new.restype = ctypes.c_void_p

        lib.Facade_segmentImage.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_bool, ctypes.c_bool, ctypes.c_char_p]
        lib.Facade_segmentImage.restype = ctypes.POINTER(Object)

        lib.Facade_cleanupObjects.argtypes = [ctypes.c_void_p, ctypes.POINTER(Object), ctypes.c_char_p]

        self.obj = lib.Facade_new("../config/config.graph-canny.properties")


    def segmentImage(self, rgbFilePath, depthFilePath, showDebug, showImage, numObjects):
        return lib.Facade_segmentImage(self.obj, rgbFilePath, depthFilePath, showDebug, showImage, numObjects)

    def cleanupObjects(self, results, numObjects):
        return lib.Facade_cleanupObjects(self.obj, results, numObjects)