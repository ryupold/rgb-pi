#triggering events

#rgb-pi modules
import log
import constants
import led
import configure
import server
import xbmcremote


class Trigger(object):

    def __init__(self, trigger):
        self.type = trigger['type']
        if log.m(log.LEVEL_FILTERS): log.l('trigger initialized: ' + self.type)
        

    def action(self):
        pass

