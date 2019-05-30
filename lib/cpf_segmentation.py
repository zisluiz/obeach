"""foo.py - a simple demo of importing a calss from C++"""
import ctypes

libcpf_segmentation = ctypes.cdll.LoadLibrary('/opt/project/lib/libcpf_segmentation.so')
# lib = ctypes.cdll.LoadLibrary('/media/zis/Dados/dev/Mestrado/codes/obeach/lib/libcpf_segmentation.so')


class CpfSegmentation(object):
    """The Foo class supports two methods, bar, and foobar..."""
    def __init__(self):
        libcpf_segmentation.Facade_new.argtypes = [ctypes.c_char_p]
        libcpf_segmentation.Facade_new.restype = ctypes.c_void_p

        libcpf_segmentation.Facade_segmentImage.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_bool]
        libcpf_segmentation.Facade_segmentImage.restype = ctypes.c_void_p

        self.obj = libcpf_segmentation.Facade_new(ctypes.c_char_p('../config/config.cpf-segmentation.properties'.encode('utf-8')))

    def segment_image(self, point_cloud, show_debug):
        return libcpf_segmentation.Facade_segmentImage(self.obj, point_cloud, show_debug)
