from core.object import Object
from core.object import Point
from util.timeelapsed import TimeElapsed


class AlgorithmInterface(object):
    def __init__(self):
        self.python_segmentation = True
        self.depth_image_grayscale = True
        self.depth_image_colored = False

    def to_objects(self, prediction):
        time_elapsed = TimeElapsed()
        objects = []
        colors = []

        for h in range(prediction.shape[0]):
            for w in range(prediction.shape[1]):
                if len(prediction.shape) == 3 and prediction.shape[2] == 3:
                    b, g, r = prediction[h, w]
                    if b == 0 and g == 0 and r == 0:
                        continue
                    key = (b, g, r)
                else:
                    v = prediction[h, w]
                    if v == 1:
                        continue
                    key = v

                if key not in colors:
                    obj = Object()
                    obj.pointsList = []

                    objects.append(obj)
                    colors.append(key)
                    obj.id = len(objects)

        if len(colors) == 0:
            return objects

        for h in range(prediction.shape[0]):
            for w in range(prediction.shape[1]):
                if len(prediction.shape) == 3 and prediction.shape[2] == 3:
                    b, g, r = prediction[h, w]
                    key = (b, g, r)
                else:
                    v = prediction[h, w]
                    key = v

                if key not in colors:
                    continue

                idx = colors.index(key)

                point = Point()
                objects[idx].pointsList.append(point)
                point.x = w
                point.y = h
                point.z = 0

        time_elapsed.printTimeElapsed('Total convertion array to objects - ')
        return objects

