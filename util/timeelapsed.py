import logging
import datetime
from util.log import Logger


class TimeElapsed(object):

    def __init__(self):
        self.startedTime = self.get_now()

    def start(self):
        self.startedTime = self.get_now()

    def get_now(self):
        return datetime.datetime.now()

    def printTimeElapsed(self, message=''):
        end = self.get_now()
        elapsed = end - self.startedTime
        Logger.info(message + 'Time elapsed: ' + str(elapsed))
