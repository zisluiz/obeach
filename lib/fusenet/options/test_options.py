from .base_options import BaseOptions


class TestOptions(BaseOptions):
    def initialize(self):
        super().initialize()
        self.ntest = "float('inf')" #n of test examples.')
        self.results_dir = './checkpoints/' #saves results here.
        self.aspect_ratio = 1.0 #aspect ratio of result images
        self.phase = 'test' #train, val, test, etc
        self.loadSize = self.fineSize
        self.isTrain = False

