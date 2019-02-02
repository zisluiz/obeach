import ctypes

class Point(ctypes.Structure):
    _fields_ = [
        ('x', ctypes.c_int),
        ('y', ctypes.c_int),
        ('z', ctypes.c_int)
    ]

class Object(ctypes.Structure):
    _fields_ = [
        ('id', ctypes.c_int),
        ('pointsLength', ctypes.c_int),
        ('points', ctypes.POINTER(Point))
    ]