from lib.algorithm_interface import AlgorithmInterface
import numpy as np
from lib import libgraph_canny_segm


class GraphCannySegm(AlgorithmInterface):
    """The Foo class supports two methods, bar, and foobar..."""
    def __init__(self):
        AlgorithmInterface.__init__(self)
        self.python_segmentation = False
        self.depth_image_grayscale = False
        self.obj = libgraph_canny_segm.Facade_new('config/config.graph-canny.properties')

    def segment_image(self, rgb_image, depth_image):
        return libgraph_canny_segm.Facade_segmentImage(self.obj, rgb_image, depth_image)

    def cleanup_objects(self, results):
        results.clear()


    def get_num_objects(self):
        return self.obj.numObjects

    def release(self):
        return

