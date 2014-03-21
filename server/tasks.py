#command tasks

#system modules
import time
import os
import sys
import random
import socket
import string
import thread
import threading
import math
import Queue
import json

#rgb-pi modules
import led
import config
import corefunctions
import configure
import pulse
import jump
import specials
import log
import constants
import datatypes


class Task():
    def __init__(self, command): # takes a command as json encoded object
        self.type = None
        self.state = constants.CMD_STATE_INIT
        #self.command = None

    def start(self):
        self.state = constants.CMD_STATE_STARTED

    def stop(self):
        self.state = constants.CMD_STATE_STOPPED

    def isStarted(self):
        return self.state == constants.CMD_STATE_STARTED
    def isStopped(self):
        return self.state == constants.CMD_STATE_STOPPED
    def isInitialized(self):
        return self.state == constants.CMD_STATE_INIT

    @staticmethod
    def createTask(command):
        if command.has_key('type'):
            if command['type'] == constants.CMD_TYPE_CC:
                return CC(command)
            if command['type'] == constants.CMD_TYPE_FADE:
                return Fade(command)
            if command['type'] == constants.CMD_TYPE_WAIT:
                return Wait(command)
            if command['type'] == constants.CMD_TYPE_LIST:
                return List(command)
            if command['type'] == constants.CMD_TYPE_LOOP:
                return Loop(command)
        else:
            return List(command)



class CC(Task):
    def __init__(self, command): # takes a command (json encoded object)
        self.type = constants.CMD_TYPE_CC
        self.color = datatypes.Color(command['color'])

    def start(self):
        super(Task, self).start()
        led.setColor(self.color)
        self.stop()

    def stop(self):
        super(Task, self).stop()

class Fade(Task):
    def __init__(self, command): # takes a command (json encoded object)
        self.type = constants.CMD_TYPE_FADE
        self.startColor = None
        self.endColor = None
        self.time = 0.0

        if command.has_key('start'):
            self.startColor = datatypes.Color(command['start'])

        self.endColor = datatypes.Color(command['end'])
        self.time = datatypes.Time(command['time'])

    def start(self):
        super(Task, self).start()
        corefunctions.fade(self, self.time.seconds, self.endColor, self.startColor)
        self.stop()

    def stop(self):
        super(Task, self).stop()

class Wait(Task):
    def __init__(self, command): # takes a command (json encoded object)
        self.type = constants.CMD_TYPE_WAIT
        self.time = datatypes.Time(command['time'])

    def start(self):
        super(Task, self).start()
        corefunctions.wait(self, self.time.seconds)
        self.stop()

    def stop(self):
        super(Task, self).stop()


class List(Task):
    def __init__(self, command): # takes an array with commands or a list command (json encoded object(s))
        self.type = constants.CMD_TYPE_LIST
        self.tasks = []

        if command.has_key('type'):
            for cmd in command['commands']:
                self.tasks.append(Task.createTask(cmd))
        else:
            for cmd in command:
                self.tasks.append(Task.createTask(cmd))

    def start(self):
        super(Task, self).start()
        for t in self.tasks:
            t.start()

    def stop(self):
        for t in self.tasks:
            t.stop()
        super(Task, self).stop()


class Loop(Task):
    def __init__(self, command): # takes an array with commands or a list command (json encoded object(s))
        self.type = constants.CMD_TYPE_LOOP
        self.condition = None
        self.tasks = []

        self.condition = datatypes.Condition(command['condition'])

        if command.has_key('type'):
            for cmd in command['commands']:
                self.tasks.append(Task.createTask(cmd))


    def start(self):
        super(Task, self).start()
        while self.condition.check():
            for t in self.tasks:
                t.start()
        self.stop()

    def stop(self):
        for t in self.tasks:
            t.stop()
        super(Task, self).stop()

