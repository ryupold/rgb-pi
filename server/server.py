#server threads

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


RUN = 1
serversocket = None
ID = 1
#global variable 'CMDQ' is under class definition of QueueThread



#mega thread class
class CommandThread(threading.Thread):
    #ctor
    def __init__(self, threadID, name, cmd):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.cmd = cmd
        self.state = constants.CMD_STATE_INIT
        self.runtime = 0
        self.timer = None
        self.next = None

    #method, which is executed when the .start() method of the thread is called
    def run(self):
        log.l("Starting Thread: " + self.name, log.LEVEL_START_STOP_THREADS)
        self.state = constants.CMD_STATE_STARTED

        #a command is alsways followed by a time (secs) after the command expires
        #set runtime to '0' or below to run the command infinite
        self.runtime = float(self.cmd[1])
        if self.runtime > 0.0:
            #set the timer for the given runtime
            self.timer = threading.Timer(self.runtime, self.stop())

        #decide which command should be executed

# FADE
        if self.name == 'fade':
            corefunctions.fade(self, float(self.cmd[2]), led.Color(self.cmd[3]), led.Color(self.cmd[4]) if len(self.cmd) > 4 else None)

# RANDOM FADE
        elif self.name == "rf":
            corefunctions.startRandomFade(self, float(self.cmd[2]), float(self.cmd[3]), float(self.cmd[4]) if len(self.cmd) > 4 else None, float(self.cmd[5]) if len(self.cmd) > 5 else None)

# PULSE
        elif self.name == "pulse":
            if len(self.cmd) > 4:
                pulse.startPulse(float(self.cmd[2]), led.Color(self.cmd[3]), led.Color(self.cmd[4]))
            else:
                pulse.startPulse(float(self.cmd[2]), led.Color(self.cmd[3]))
# JUMP
        elif self.name == "jump":
            if len(self.cmd) > 4:
                jump.startJump(float(self.cmd[2]), led.Color(self.cmd[3]), led.Color(self.cmd[4]))
            else:
                jump.startJump(float(self.cmd[2]), led.Color(self.cmd[3]))


        self.stop()
        log.l("Exiting:" + self.name, log.LEVEL_START_STOP_THREADS)

    #stops this thread, disregarding when its expiration should be
    def stop(self):
        log.l("stopping " + self.name, log.LEVEL_START_STOP_THREADS)

        #stop timer
        if self.timer is not None:
            self.timer.cancel()
            self.timer = None

        if(self.state != constants.CMD_STATE_EXPIRED):
            self.state = constants.CMD_STATE_EXPIRED
        global CMDQ
        CMDQ.notify()


class CommandQueue(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.lock = threading.Semaphore()
        self.monitor = threading.Event()
        self.current = None
        self.startCMD = None
        self.alive = 1

        self.monitor.clear()

    def run(self):
        while self.alive:
            while self.startCMD is None and self.alive:
                self.monitor.wait()
            if self.alive:
                self.lock.acquire()
                if self.current is None:
                    self.current = self.startCMD
                    if self.current.state == constants.CMD_STATE_INIT:
                        self.current.state = constants.CMD_STATE_STARTED
                        self.current.start()
                else:
                    if self.current.next is not None and self.current.state == constants.CMD_STATE_EXPIRED:
                        self.current = self.current.next
                        self.current.state = constants.CMD_STATE_STARTED
                        self.current.start()
                    elif self.current is not None and self.current.state == constants.CMD_STATE_INIT:
                        self.current.state = constants.CMD_STATE_STARTED
                        self.current.start()
                    else:
                        self.current = None
                        self.startCMD = None

                self.lock.release()
                while self.current is not None and self.current.state == constants.CMD_STATE_STARTED and self.alive:
                    self.monitor.wait()

    def stop(self):
        self.lock.acquire()
        self.startCMD = None
        if self.current is not None:
            self.current.stop()
            self.current = None

        self.alive = 0
        self.notify()
        self.lock.release()

    def enq(self, cmd):
        self.lock.acquire()

#CASE 1: if no command is running, take cmd as main command
        if self.startCMD is None:
            self.startCMD = cmd

        else:
            preLastCMD = self.startCMD
            lastCMD = self.startCMD.next

#CASE 2: if only one command is running, attach to it or replace it if its infinite
            if lastCMD is None:
                if self.current.runtime > 0:
                    self.current.next = cmd
                else:
                    self.current.stop()
                    self.current = None
                    self.startCMD = cmd

#CASE 3: if multiple commands in a queue, attach to the last or replace the last if its infinite
            else:
                while lastCMD is not None and lastCMD.next is not None and lastCMD.next is not self.startCMD:
                    preLastCMD = lastCMD
                    lastCMD = lastCMD.next
                if lastCMD.runtime > 0:
                    lastCMD.next = cmd
                else:
                    if self.current is lastCMD:
                        self.current.stop()
                        self.current = cmd
                    preLastCMD.next = cmd


        self.notify()
        self.lock.release()

    def notify(self):
        self.lock.acquire()
        if self.current.state == constants.CMD_STATE_EXPIRED:
            self.current = None
        if self.startCMD.state == constants.CMD_STATE_EXPIRED:
            self.startCMD = None
        self.lock.release()
        self.monitor.set()

CMDQ = CommandQueue()




#server socket, which waits for incoming commands and starting actions like fading or simple color changes
def readcommands(threadName, intervall):
    #print the config parameters
    configure.cls()
    configure.printConfig()

    print "\n... starting server...\n\n"

    #globals
    global CMDQ
    global ID
    global serversocket

    #create an INET, STREAMing socket
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #bind the socket to a public host,
    # and a well-known port
    serversocket.bind(('', config.SERVER_PORT)) # socket.gethostname() # for getting own address

    #become a server socket
    serversocket.listen(5)

    #start cmd queue
    CMDQ.setDaemon(1)
    CMDQ.start()

    while RUN:
        try:
            (clientsocket, address) = serversocket.accept()
            #command = string.split(string.replace(str(clientsocket.recv(1024)), ",", "."))
            ## put this line in, if commas need to be sent in a command!!
            command = string.split(string.strip(str(clientsocket.recv(1024))))
            if len(command) > 0:
                if command[0] == "cc":
                    log.l(command, log.LEVEL_COMMAND_CC)
                    led.setColor(led.Color(command[1]))

                elif command[0] == "loop":
                    log.l(command, log.LEVEL_COMMANDS)
                    if CMDQ.startCMD is not None:
                        lastCMD = CMDQ.startCMD.next
                        while lastCMD is not None and lastCMD.next is not None and lastCMD.next is not CMDQ.startCMD:
                            lastCMD = lastCMD.next
                        if lastCMD.next is not CMDQ.startCMD:
                            lastCMD.next = CMDQ.startCMD

                else:
                    log.l(command, log.LEVEL_COMMANDS)
                    ID += 1
                    cmdT = CommandThread(ID, string.lower(command[0]), command)
                    CMDQ.enq(cmdT)
            else:
                raise AttributeError("no commands received!")

        except:
            print "Unexpected ERROR: ", sys.exc_info()[0], ": ", sys.exc_info()[1]
        else:
            clientsocket.close()

