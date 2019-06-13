"""foo.py - a simple demo of importing a calss from C++"""
import ctypes
from core.object import Object
from lib.algorithm_interface import AlgorithmInterface
import numpy as np
from lib.rgbd_saliency import librgbd_saliency
import numpy as np  # Import Python functions, attributes, submodules of numpy

#np.import_array()

#class Facade(object):
#    def __init__(self):
#        self.a = ''


class RgbdSaliency(AlgorithmInterface):
    """The Foo class supports two methods, bar, and foobar..."""
    def __init__(self):
        AlgorithmInterface.__init__(self)
        self.python_segmentation = False
        #self.librgbd_saliency = ctypes.cdll.LoadLibrary('/opt/project/lib/rgbd_saliency/librgbd_saliency.so')
        #self.librgbd_saliency.Facade_new.argtypes = [ctypes.c_char_p]
        #self.librgbd_saliency.Facade_new.restype = ctypes.c_void_p

        #self.librgbd_saliency.Facade_segmentImage.argtypes = [ctypes.c_void_p, ctypes.py_object, ctypes.py_object, ctypes.c_char_p]
        #self.librgbd_saliency.Facade_segmentImage.restype = ctypes.POINTER(Object)

        #self.librgbd_saliency.Facade_cleanupObjects.argtypes = [ctypes.c_void_p, ctypes.POINTER(Object), ctypes.c_char_p]

        #self.obj = self.librgbd_saliency.Facade_new(ctypes.c_char_p('../config/config.rgbd-saliency.properties'.encode('utf-8')))
        self.obj = librgbd_saliency.Facade_new('../config/config.rgbd-saliency.properties')

    def segment_image(self, rgb_image, depth_image, num_objects):
        rgb_image_np = np.array(rgb_image, dtype='uint8')
        depth_image_np = np.array(depth_image, dtype='uint8')
        objts = librgbd_saliency.Facade_segmentImage(self.obj, rgb_image_np, depth_image_np, num_objects)
        num_objects = librgbd_saliency.numObjects
        return objts

    def cleanup_objects(self, results, num_objects):
        return librgbd_saliency.Facade_cleanupObjects(self.obj, results, num_objects)

