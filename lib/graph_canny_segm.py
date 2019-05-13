"""foo.py - a simple demo of importing a calss from C++"""
import ctypes
from core.object import Object

# lib = ctypes.cdll.LoadLibrary('/media/zis/Dados/dev/Mestrado/codes/obeach/lib/libgraph-canny-segm.so')
lib = ctypes.cdll.LoadLibrary('/opt/project/lib/libgraph-canny-segm.so')


class GraphCannySegm(object):
    """The Foo class supports two methods, bar, and foobar..."""
    def __init__(self):
        lib.Facade_new.argtypes = [ctypes.c_char_p]
        lib.Facade_new.restype = ctypes.c_void_p

        lib.Facade_segmentImage.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_bool, ctypes.c_bool, ctypes.c_char_p]
        lib.Facade_segmentImage.restype = ctypes.POINTER(Object)

        lib.Facade_cleanupObjects.argtypes = [ctypes.c_void_p, ctypes.POINTER(Object), ctypes.c_char_p]

        self.obj = lib.Facade_new(ctypes.c_char_p('../config/config.graph-canny.properties'.encode('utf-8')))

    def segment_image(self, rgb_file_path, depth_file_path, show_debug, show_image, num_objects):
        return lib.Facade_segmentImage(self.obj, ctypes.c_char_p(rgb_file_path.encode('utf-8')), ctypes.c_char_p(depth_file_path.encode('utf-8')), show_debug, show_image, num_objects)

    def cleanup_objects(self, results, num_objects):
        return lib.Facade_cleanupObjects(self.obj, results, num_objects)
