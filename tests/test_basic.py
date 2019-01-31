# -*- coding: utf-8 -*-

#from .context import sample
import sys

sys.path.append('/usr/local/lib/python2.7/dist-packages/cv2/python-2.7/')
import unittest
import cv2


class BasicTestSuite(unittest.TestCase):
    """Basic test cases."""

    def test_absolute_truth_and_meaning(self):
        img = cv2.imread('../dataset/demo.jpg', cv2.IMREAD_COLOR)

        cv2.imshow('image', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == '__main__':
    unittest.main()