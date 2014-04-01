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


class Task(object):
    def __init__(self, command=None): # takes a command as json encoded object
        self.command = command
        self.state = constants.CMD_STATE_INIT
        if log.m(log.LEVEL_INIT_COMMAND): log.l('initialized: ' + self.type)

    def start(self):
        self.state = constants.CMD_STATE_STARTED
        if log.m(log.LEVEL_START_STOP_THREADS): log.l('starting ' + self.type)

    def stop(self):
        self.state = constants.CMD_STATE_STOPPED
        if log.m(log.LEVEL_START_STOP_THREADS): log.l('stopping ' + self.type)

    def isStarted(self):
        return self.state == constants.CMD_STATE_STARTED

    def isStopped(self):
        return self.state == constants.CMD_STATE_STOPPED

    def isInitialized(self):
        return self.state == constants.CMD_STATE_INIT

    @staticmethod
    def createTask(command):
        if isinstance(command, dict) and command.has_key('type'):
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
            if command['type'] == constants.CMD_TYPE_NOP:
                return NOP(command)
        else:
            return List(command)


class CC(Task):
    def __init__(self, command): # takes a command (json encoded object)
        self.type = constants.CMD_TYPE_CC
        super(CC, self).__init__(command)
        self.color = None
        self.operator = None

    def start(self):
        super(CC, self).start()
        self.color = datatypes.Color(self.command['color'])
        if self.command.has_key('operator'):
            self.operator = datatypes.Color(self.command['operator'])
            if log.m(log.LEVEL_COMMAND_CC): log.l('color=' + str(led.COLOR[0]) + ' ' + self.operator + ' ' + str(self.color))
            for i in range(0, len(config.LED_PINS)):
                if ((i + 1) & self.color.Address) != 0:
                    newColor = led.COLOR[i];
                    if self.operator == '*':
                        newColor = newColor * self.color
                    if self.operator == '/':
                        newColor = newColor / self.color
                    if self.operator == '+':
                        newColor = newColor + self.color
                    if self.operator == '-':
                        newColor = newColor - self.color
                    led.setColor(newColor)
        else:
            if log.m(log.LEVEL_COMMAND_CC): log.l('color=' + str(self.color))
            led.setColor(self.color)
        self.stop()

    def stop(self):
        super(CC, self).stop()


class Fade(Task):
    def __init__(self, command): # takes a command (json encoded object)
        self.type = constants.CMD_TYPE_FADE
        super(Fade, self).__init__(command)
        self.startColor = None
        self.endColor = None
        self.time = 0.0

    def start(self):
        super(Fade, self).start()
        if self.command.has_key('start'):
            self.startColor = datatypes.Color(self.command['start'])

        self.endColor = datatypes.Color(self.command['end'])
        self.time = datatypes.Time(self.command['time'])

        corefunctions.fade(self, self.time.seconds, self.endColor, self.startColor)
        self.stop()

    def stop(self):
        super(Fade, self).stop()


class Wait(Task):
    def __init__(self, command): # takes a command (json encoded object)
        self.type = constants.CMD_TYPE_WAIT
        super(Wait, self).__init__(command)
        self.time = None

    def start(self):
        super(Wait, self).start()
        self.time = datatypes.Time(self.command['time'])
        if log.m(log.LEVEL_COMMAND_DETAIL): log.l('waiting for ' + str(self.time) + ' seconds')
        corefunctions.wait(self, self.time.seconds)
        self.stop()

    def stop(self):
        super(Wait, self).stop()


class List(Task):
    def __init__(self, command): # takes an array with commands or a list command (json encoded object(s))
        self.type = constants.CMD_TYPE_LIST
        super(List, self).__init__(command)
        self.tasks = []

        if isinstance(command, dict) and command.has_key('type'):
            for cmd in command['commands']:
                self.tasks.append(Task.createTask(cmd))
        else:
            for cmd in command:
                self.tasks.append(Task.createTask(cmd))

    def start(self):
        super(List, self).start()
        for t in self.tasks:
            t.start()

    def stop(self):
        for t in self.tasks:
            if t.state != constants.CMD_STATE_STOPPED:
                t.stop()
        super(List, self).stop()


class Loop(Task):
    def __init__(self, command): # takes an array with commands or a list command (json encoded object(s))
        self.type = constants.CMD_TYPE_LOOP
        super(Loop, self).__init__(command)
        self.condition = None
        self.tasks = []

        self.condition = None

        if command.has_key('type'):
            for cmd in command['commands']:
                self.tasks.append(Task.createTask(cmd))


    def start(self):
        super(Loop, self).start()
        self.condition = datatypes.Condition(self.command['condition'])
        if log.m(log.LEVEL_COMMAND_DETAIL): log.l('starting loop with condition: ' + str(self.condition))
        while self.condition.check():
            for t in self.tasks:
                t.start()
        self.stop()

    def stop(self):
        if log.m(log.LEVEL_COMMAND_DETAIL): log.l('stopping loop with condition: ' + str(self.condition))
        for t in self.tasks:
            if t.state != constants.CMD_STATE_STOPPED:
                t.stop()
        super(Loop, self).stop()


class NOP(Task):
    def __init__(self, command): # takes a command (json encoded object)
        self.type = constants.CMD_TYPE_NOP
        super(NOP, self).__init__(command)

    def start(self):
        super(NOP, self).start()
        if log.m(log.LEVEL_COMMAND_DETAIL): log.l('doing nothing')
        self.stop()

    def stop(self):
        super(NOP, self).stop()

