import logging
import datetime
from util.log import Logger


class TimeElapsed(object):

    def __init__(self):
        self.start()

    def start(self):
        self.start = datetime.datetime.now()

    def printTimeElapsed(self):
        end = datetime.datetime.now()
        elapsed = end - self.start
        Logger.info('Time elapsed: ' + str(elapsed.seconds) + '.' + str(elapsed.microseconds) + ' seconds')
