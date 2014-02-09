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

    #method, which is executed when the .start() method of the thread is called
    def run(self):
        log.l("Starting Thread: " + self.name, log.LEVEL_START_STOP_THREADS)
        self.state = constants.CMD_STATE_STARTED

        #decide which command should be executed

# FADE
        if self.name == 'fade':
            corefunctions.fade(self, float(self.cmd[1]), led.Color(self.cmd[2]), led.Color(self.cmd[3]) if len(self.cmd) > 3 else None)

# RANDOM FADE
        elif self.name == "rf":
            corefunctions.startRandomFade(self, float(self.cmd[1]), float(self.cmd[2]), float(self.cmd[3]) if len(self.cmd) > 3 else None, float(self.cmd[4]) if len(self.cmd) > 4 else None)

# PULSE
        elif self.name == "pulse":
            if len(self.cmd) > 3:
                pulse.startPulse(float(self.cmd[1]), led.Color(self.cmd[2]), led.Color(self.cmd[3]))
            else:
                pulse.startPulse(float(self.cmd[1]), led.Color(self.cmd[2]))
# JUMP
        elif self.name == "jump":
            if len(self.cmd) > 3:
                jump.startJump(float(self.cmd[1]), led.Color(self.cmd[2]), led.Color(self.cmd[3]))
            else:
                jump.startJump(float(self.cmd[1]), led.Color(self.cmd[2]))


        self.state = constants.CMD_STATE_EXPIRED
        log.l("Exiting:" + self.name, log.LEVEL_START_STOP_THREADS)

    #stops this thread, disregarding when its expiration should be
    def stop(self):
        log.l("stopping " + self.name, log.LEVEL_START_STOP_THREADS)
        if(self.state != constants.CMD_STATE_EXPIRED):
            self.state = constants.CMD_STATE_EXPIRED


class QueueThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.lock = threading.Condition()
        self.Q = Queue.Queue()
        self.current = None
        self.alive = 1

    def run(self):
        while self.alive:
            if self.current is None:
                self.current = self.deq()
                if self.current.state == constants.CMD_STATE_INIT:
                    self.current.start()

            while self.current.state == constants.CMD_STATE_STARTED:
                pass #TODO: wait command queue

            self.current = None

    def stop(self):
        self.lock.acquire()
        if self.current is not None:
            self.current.stop()
            self.current = None
        self.alive = 0
        self.lock.release()

    def enq(self, cmd):
        self.lock.acquire()
        self.Q.put_nowait(cmd)
        self.lock.release()

    def deq(self):
        self.lock.acquire()
        cmdT = None
        if not self.Q.empty():
            cmdT = self.Q.get_nowait()
        self.lock.release()
        return cmdT

    def pulse(self):
        pass #TODO: wake up the command queue

CMDQ = QueueThread()




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
                else:
                    log.l(command, log.LEVEL_COMMANDS)
                    ID += 1
                    cmdT = CommandThread(ID, string.lower(command[0]), command)
                    CMDQ.enq(cmdT)
            else:
                raise AttributeError("no commands received!")

        except:
            print "Unexpected error: ", sys.exc_info()[0], ": ", sys.exc_info()[1]
        else:
            clientsocket.close()

