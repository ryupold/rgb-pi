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
import log
import constants
import datatypes


class Task(object):
    def __init__(self, command, thread=None): # takes a command as json encoded object
        self.command = command
        self.thread = thread
        self.threadID = -1
        self.state = constants.CMD_STATE_INIT
        if log.m(log.LEVEL_INIT_COMMAND): log.l('<'+str(self.getThreadID())+'> initialized: ' + self.type)

    def start(self):
        self.state = constants.CMD_STATE_STARTED
        if self.thread is not None and self.thread.state != constants.CMD_STATE_STARTED:
            #raise RuntimeError('the CommandThread of this task needs to be in CMD_STATE_STARTED-state to start child tasks!')
            return False
        if log.m(log.LEVEL_START_STOP_THREADS): log.l('<'+str(self.getThreadID())+'> starting ' + self.type)
        return True

    def stop(self):
        self.state = constants.CMD_STATE_STOPPED
        if log.m(log.LEVEL_START_STOP_THREADS): log.l('<'+str(self.getThreadID())+'> stopping ' + self.type)

    def isStarted(self):
        return self.state == constants.CMD_STATE_STARTED

    def isStopped(self):
        return self.state == constants.CMD_STATE_STOPPED

    def isInitialized(self):
        return self.state == constants.CMD_STATE_INIT

    def getThreadID(self):
        return self.thread.threadID if self.thread is not None else -1

    @staticmethod
    def createTask(command, thread=None):
        if isinstance(command, dict) and command.has_key('type'):
            if command['type'] == constants.CMD_TYPE_CC:
                return CC(command, thread)
            if command['type'] == constants.CMD_TYPE_FADE:
                return Fade(command, thread)
            if command['type'] == constants.CMD_TYPE_WAIT:
                return Wait(command, thread)
            if command['type'] == constants.CMD_TYPE_LIST:
                return List(command, thread)
            if command['type'] == constants.CMD_TYPE_LOOP:
                return Loop(command, thread)
            if command['type'] == constants.CMD_TYPE_NOP:
                return NOP(command, thread)
        else:
            return List(command, thread)


class CC(Task):
    def __init__(self, command, thread=None): # takes a command (json encoded object)
        self.type = constants.CMD_TYPE_CC
        super(CC, self).__init__(command, thread)
        self.color = None
        self.operator = None

    def start(self):
        if super(CC, self).start():
            self.color = datatypes.Color(self.command['color'])
            if self.command.has_key('operator'):
                self.operator = self.command['operator']
                if log.m(log.LEVEL_COMMAND_CC): log.l('<'+str(self.getThreadID())+'> color=' + str(led.COLOR[0]) + ' ' + self.operator + ' ' + str(self.color))
                for i in range(0, len(config.LED_PINS)):
                    if ((i + 1) & self.color.Address) != 0:
                        newColor = led.COLOR[i]
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
                if log.m(log.LEVEL_COMMAND_CC): log.l('<'+str(self.getThreadID())+'> color=' + str(self.color))
                led.setColor(self.color)
        self.stop()

    def stop(self):
        super(CC, self).stop()


class Fade(Task):
    def __init__(self, command, thread=None): # takes a command (json encoded object)
        self.type = constants.CMD_TYPE_FADE
        super(Fade, self).__init__(command, thread)
        self.startColor = None
        self.endColor = None
        self.time = 0.0

    def start(self):
        if super(Fade, self).start():
            if self.command.has_key('start'):
                self.startColor = datatypes.Color(self.command['start'])

            self.endColor = datatypes.Color(self.command['end'])
            self.time = datatypes.Time(self.command['time'])
            if log.m(log.LEVEL_COMMAND_DETAIL): log.l('<'+str(self.getThreadID())+'> fading from '+str(self.startColor if self.startColor is not None else 'current color')+' to '+str(self.endColor)+' over ' + str(self.time) + ' seconds')
            corefunctions.fade(self, self.time.seconds, self.endColor, self.startColor)
        self.stop()

    def stop(self):
        super(Fade, self).stop()


class Wait(Task):
    def __init__(self, command, thread=None): # takes a command (json encoded object)
        self.type = constants.CMD_TYPE_WAIT
        super(Wait, self).__init__(command, thread)
        self.time = None

    def start(self):
        if super(Wait, self).start():
            self.time = datatypes.Time(self.command['time'])
            if log.m(log.LEVEL_COMMAND_DETAIL): log.l('<'+str(self.getThreadID())+'> waiting for ' + str(self.time) + ' seconds')
            corefunctions.wait(self, self.time.seconds)
        self.stop()

    def stop(self):
        super(Wait, self).stop()


class List(Task):
    def __init__(self, command, thread=None): # takes an array with commands or a list command (json encoded object(s))
        self.type = constants.CMD_TYPE_LIST
        super(List, self).__init__(command, thread)
        self.tasks = []

        if isinstance(command, dict) and command.has_key('type'):
            for cmd in command['commands']:
                self.tasks.append(Task.createTask(cmd, self))
        else:
            for cmd in command:
                self.tasks.append(Task.createTask(cmd, self))

    def start(self):
        if super(List, self).start():
            for t in self.tasks:
                if self.isStarted(): t.start()
                else: break
        self.stop()

    def stop(self):
        for t in self.tasks:
            if not t.isStopped():
                t.stop()
        super(List, self).stop()


class Loop(Task):
    def __init__(self, command, thread=None): # takes an array with commands or a list command (json encoded object(s))
        self.type = constants.CMD_TYPE_LOOP
        super(Loop, self).__init__(command, thread)
        self.condition = None
        self.tasks = []

        self.condition = None

        if command.has_key('type'):
            for cmd in command['commands']:
                self.tasks.append(Task.createTask(cmd, self))

    def isStarted(self):
        return self.state == constants.CMD_STATE_STARTED and self.condition.isTrue()


    def start(self):
        if super(Loop, self).start():
            self.condition = datatypes.Condition(self.command['condition'])
            if log.m(log.LEVEL_COMMAND_DETAIL): log.l('<'+str(self.getThreadID())+'> starting loop with condition: ' + str(self.condition))
            tmp = self.isStarted()
            while tmp:
                for t in self.tasks:
                    t.start()
                self.condition.step()
                tmp = self.isStarted()
        self.stop()

    def stop(self):
        if log.m(log.LEVEL_COMMAND_DETAIL): log.l('<'+str(self.getThreadID())+'> stopping loop with condition: ' + str(self.condition))
        for t in self.tasks:
            if t.state != constants.CMD_STATE_STOPPED:
                t.stop()
        super(Loop, self).stop()


class NOP(Task):
    def __init__(self, command, thread=None): # takes a command (json encoded object)
        self.type = constants.CMD_TYPE_NOP
        super(NOP, self).__init__(command, thread)

    def start(self):
        if super(NOP, self).start():
            if log.m(log.LEVEL_COMMAND_DETAIL): log.l('<'+str(self.getThreadID())+'> doing nothing')
        self.stop()

    def stop(self):
        super(NOP, self).stop()