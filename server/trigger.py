#triggering events

#python modules
import threading
import time
import sys
import json

#rgb-pi modules
import log
import constants
import led
import configure
import server
import xbmcremote
import datatypes
import config


class TriggerManager(threading.Thread):
    """
    This thread is started with the rgb-pi server and handles adding, removing and runtime of all active triggers.
    """
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.daemon = True
        self.active = True
        self.triggers = {}
        self.mutex = threading.BoundedSemaphore()
        if log.m(log.LEVEL_TRIGGER): log.l('trigger manager initialized')

    #method, which is executed when the .start() method of the thread is called
    def run(self):
        if log.m(log.LEVEL_TRIGGER): log.l('starting trigger manager...')
        while self.active:
            self.mutex.acquire()
            try:
                for k,v in self.triggers:
                    if v.isTrue():
                        v.action()
            except:
                if log.m(log.LEVEL_ERRORS): log.l('ERROR in trigger run method: ' + str(sys.exc_info()[0]) + ': '+str(sys.exc_info()[1]))

            self.mutex.release()
            time.sleep(config.DELAY)
        if log.m(log.LEVEL_TRIGGER): log.l('stopping trigger manager...')

    #stops this thread, disregarding when its expiration should be
    def stop(self):
        self.active = False

    def addTrigger(self, trigger):
        exception = None
        self.mutex.acquire()
        try:
            self.triggers[trigger.name] = trigger
            if log.m(log.LEVEL_TRIGGER): log.l('trigger added with key=' + trigger.name)
        except:
            exception = StandardError(str(sys.exc_info()[0]) + ': '+str(sys.exc_info()[1]))
        self.mutex.release()
        if exception is not None:
            raise exception

    def removeTrigger(self, name):
        exception = None
        self.mutex.acquire()
        try:
            self.triggers.pop(name)
            if log.m(log.LEVEL_TRIGGER): log.l('trigger removed with key=' + name)
        except:
            exception = StandardError(str(sys.exc_info()[0]) + ': '+str(sys.exc_info()[1]))
        self.mutex.release()
        if exception is not None:
            raise exception


class Trigger(object):

    def __init__(self, trigger):
        self.name = trigger['name']
        self.condition = datatypes.TriggerCondition(trigger['condition'])
        self.onAction = trigger['action']
        self.repeat = int(trigger['repeat']) if trigger.has_key('repeat') else 0
        if log.m(log.LEVEL_FILTERS): log.l('trigger initialized: ' + self.name)


    def isTrue(self):
        self.condition.check()
        return self.condition.isTrue()

    def action(self):
        server.applyCommand(self.onAction)
        if self.repeat > 0:
            self.repeat -= 1
            if self.repeat <= 0:
                server.triggerManager.triggers.pop(self.name) #this might cause an error, but i'm not sure xD


