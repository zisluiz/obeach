import tensorflow as tf
import numpy as np
import scipy.misc as misc

class FcnTensorflow(object):
    """The Foo class supports two methods, bar, and foobar..."""
    def __init__(self):
        graph = tf.Graph()
        self.sess = tf.Session(graph=graph)
        tf.saved_model.loader.load(self.sess, ["serve"], '/opt/project/lib/fcn_tensorflow')
        #graph = tf.get_default_graph()
        self.pred = graph.get_tensor_by_name("ExpandDims:0")
        self.resize_size = 224

    def segment_image(self, rgb_file_path, depth_file_path, num_objects):
        rgb_image = misc.imread(rgb_file_path, flatten=False, mode='RGB')
        depth_image = misc.imread(depth_file_path, flatten=True, mode='P')
        original_height = rgb_image.shape[0]
        original_width = rgb_image.shape()[1]
        rgb_resized_image = misc.imresize(rgb_image,
                      [self.resize_size, self.resize_size], interp='nearest')
        depth_resized_image = misc.imresize(depth_image,
                      [self.resize_size, self.resize_size], interp='nearest')

        output = self.sess.run(self.pred,
                          feed_dict={'input_image:0': rgb_resized_image.reshape(1, self.resize_size,self.resize_size,3),
                                     'annotation:0': depth_resized_image.reshape(1, self.resize_size,self.resize_size,1), 'keep_probabilty:0': 1.0})
        output = np.squeeze(output, axis=3)

        rgb_resized_image = misc.imresize(output[0],
                      [original_height, original_width], interp='nearest')
        print(rgb_resized_image)


    def cleanup_objects(self, results, num_objects):
        return self.librgbd_saliency.Facade_cleanupObjects(self.obj, results, num_objects)


    def _transform(filename, __channels):
        image_options = {'resize': True, 'resize_size': 224}
        image = misc.imread(filename, flatten=False if __channels else True, mode='RGB' if __channels else 'P')
        if __channels and len(image.shape) < 3:  # make sure images are of shape(h,w,3)
            image = np.array([image for i in range(3)])

        if image_options.get("resize", False) and image_options["resize"]:
            resize_size = int(image_options["resize_size"])
            resize_image = misc.imresize(image,
                                            [resize_size, resize_size], interp='nearest')
            #print('resized')
        else:
            resize_image = image

        return resize_image.reshape(1, resize_size,resize_size,3 if __channels else 1)

