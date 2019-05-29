"""foo.py - a simple demo of importing a calss from C++"""
import ctypes
from core.object import Object

librgbd_saliency = ctypes.cdll.LoadLibrary('/opt/project/lib/rgbd_saliency/librgbd_saliency.so')


class RgbdSaliency(object):
    """The Foo class supports two methods, bar, and foobar..."""
    def __init__(self):
        librgbd_saliency.Facade_new.argtypes = [ctypes.c_char_p]
        librgbd_saliency.Facade_new.restype = ctypes.c_void_p

        librgbd_saliency.Facade_segmentImage.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
        librgbd_saliency.Facade_segmentImage.restype = ctypes.POINTER(Object)

        librgbd_saliency.Facade_cleanupObjects.argtypes = [ctypes.c_void_p, ctypes.POINTER(Object), ctypes.c_char_p]

        self.obj = librgbd_saliency.Facade_new(ctypes.c_char_p('../config/config.rgbd-saliency.properties'.encode('utf-8')))

    def segment_image(self, rgb_file_path, depth_file_path, num_objects):
       return librgbd_saliency.Facade_segmentImage(self.obj, ctypes.c_char_p(rgb_file_path.encode('utf-8')), ctypes.c_char_p(depth_file_path.encode('utf-8')), num_objects)

    def cleanup_objects(self, results, num_objects):
        return librgbd_saliency.Facade_cleanupObjects(self.obj, results, num_objects)
