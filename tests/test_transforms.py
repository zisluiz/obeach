import unittest
import cv2
import numpy as np
from PIL import Image
import os


class TransformsTestSuite(unittest.TestCase):
    """Basic test cases."""

    def test_transforms(self):
        rgb = cv2.imread('dataset/png/rgb/rgb_00000.png', cv2.IMREAD_COLOR)
        depth = cv2.imread('dataset/png/depth/depth_00000.png', cv2.IMREAD_UNCHANGED)

        rgb_resized = cv2.resize(rgb, (640, 360))
        depth_resized = cv2.resize(depth, (640, 360))

        cv2.imwrite(os.getcwd()+'/results/transforms/res_rgb_00000.png', rgb_resized)
        cv2.imwrite(os.getcwd() + '/results/transforms/res_depth_00000.png', depth_resized)

if __name__ == '__main__':
    unittest.main()