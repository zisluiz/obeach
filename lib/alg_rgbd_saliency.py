"""foo.py - a simple demo of importing a calss from C++"""
from lib.algorithm_interface import AlgorithmInterface
import numpy as np
#from lib.rgbd_saliency import librgbd_saliency


class RgbdSaliency(AlgorithmInterface):
    """The Foo class supports two methods, bar, and foobar..."""
    def __init__(self):
        AlgorithmInterface.__init__(self)
        self.python_segmentation = False
        self.depth_image_colored = True
        self.obj = librgbd_saliency.Facade_new('../config/config.rgbd-saliency.properties')

    def segment_image(self, rgb_image, depth_image):
        rgb_image_np = np.array(rgb_image, dtype='uint8')
        depth_image_np = np.array(depth_image, dtype='uint8')
        return librgbd_saliency.Facade_segmentImage(self.obj, rgb_image_np, depth_image_np)

    def cleanup_objects(self, results):
        results.clear()

    def get_num_objects(self):
        return self.obj.numObjects

    def release(self):
        return

