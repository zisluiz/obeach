import os.path
import random
import torchvision.transforms as transforms
import torch
from ..data.base_dataset import BaseDataset
from ..data.image_folder import make_dataset
from PIL import Image
import numpy as np
import pickle

class sunrgbddataset(BaseDataset):
	@staticmethod
	def modify_commandline_options(parser, is_train):
		return parser

	def initialize(self, opt):
		self.opt = opt
		self.batch_size = opt.batch_size
		self.root = opt.dataroot # path for the dataset
		self.num_labels = 38
		self.ignore_label = 0
		assert(opt.resize_or_crop == 'none')

	def name(self):
		return 'sunrgbd'
