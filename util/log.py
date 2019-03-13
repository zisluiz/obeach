import logging
import os

class Logger(object):

    #def __init__(self):

    @staticmethod
    def init():
        if not os.path.exists('logs'):
            os.makedirs('logs')

        logging.basicConfig(filename='logs/segmentation.log', level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')
        logging.getLogger().addHandler(logging.StreamHandler())
        logging.info('####### Logging started!')

    @staticmethod
    def info(msg):
        logging.info(msg)