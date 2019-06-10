from core.object import Object
from core.object import Point


class AlgorithmInterface(object):
    def __init__(self):
        self.python_segmentation = True

    def to_objects(self, prediction):
        objects = []
        colors = []

        for x in range(prediction.shape[0]):
            for y in range(prediction.shape[1]):
                if len(prediction.shape) == 3:
                    b, g, r = prediction[x, y]
                    key = (b, g, r)
                else:
                    v = prediction[x, y]
                    key = v

                if key not in colors:
                    obj = Object()
                    obj.pointsList = []

                    objects.append(obj)
                    colors.append(key)
                    obj.id = len(objects)

        for x in range(prediction.shape[0]):
            for y in range(prediction.shape[1]):
                if len(prediction.shape) == 3:
                    b, g, r = prediction[x, y]
                    key = (b, g, r)
                else:
                    v = prediction[x, y]
                    key = v

                idx = colors.index(key)
                point = Point()
                objects[idx].pointsList.append(point)
                point.x = x
                point.y = y
                point.z = 0

        return objects

