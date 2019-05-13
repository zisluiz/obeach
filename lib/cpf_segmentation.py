"""foo.py - a simple demo of importing a calss from C++"""
import ctypes

lib = ctypes.cdll.LoadLibrary('/opt/project/lib/libcpf_segmentation.so')
# lib = ctypes.cdll.LoadLibrary('/media/zis/Dados/dev/Mestrado/codes/obeach/lib/libcpf_segmentation.so')


class CpfSegmentation(object):
    """The Foo class supports two methods, bar, and foobar..."""
    def __init__(self):
        lib.Facade_new.argtypes = [ctypes.c_char_p]
        lib.Facade_new.restype = ctypes.c_void_p

        lib.Facade_segmentImage.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_bool]
        lib.Facade_segmentImage.restype = ctypes.c_void_p

        self.obj = lib.Facade_new(ctypes.c_char_p('../config/config.cpf-segmentation.properties'.encode('utf-8')))

    def segment_image(self, point_cloud, show_debug):
        return lib.Facade_segmentImage(self.obj, point_cloud, show_debug)
