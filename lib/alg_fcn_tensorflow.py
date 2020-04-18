import tensorflow as tf
import numpy as np
from lib.algorithm_interface import AlgorithmInterface


class FcnTensorflow(AlgorithmInterface):
    """The Foo class supports two methods, bar, and foobar..."""
    def __init__(self):
        AlgorithmInterface.__init__(self)
        graph = tf.Graph()
        self.sess = tf.Session(graph=graph)
        tf.saved_model.loader.load(self.sess, ["serve"], '/opt/project/lib/fcn_tensorflow')
        #graph = tf.get_default_graph()
        self.pred = graph.get_tensor_by_name("ExpandDims:0")
        self.num_objects = 0

    def segment_image(self, rgb_image, depth_image):
        output = self.sess.run(self.pred,
                          feed_dict={'input_image:0': rgb_image.reshape(1, rgb_image.shape[0], rgb_image.shape[1], 3)
                              #,'annotation:0': np.array(depth_image).reshape(1, depth_image.width, depth_image.height, 1)
                              , 'keep_probabilty:0': 1.0})
        output = np.squeeze(output, axis=3)

        #rgb_resized_image = misc.imresize(output[0],
        #              [original_height, original_width], interp='nearest')
        #print(output)
        objs = self.to_objects(output.reshape(output.shape[1], output.shape[2]))
        self.num_objects = len(objs)
        return objs

    def cleanup_objects(self, results):
        results.clear()

    def get_num_objects(self):
        return self.num_objects

    def release(self):
        return

