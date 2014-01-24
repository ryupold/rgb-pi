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

#rgb-pi modules
import led
import config
import corefunctions

import pulse
import jump
import specials



RUN = 1
COMMAND_RUN = 0
CURRENTTHREAD = None



class FadeThread(threading.Thread):
    def __init__(self, threadID, name, cmd):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.cmd = cmd

    def run(self):
        print self.cmd

        if self.cmd[0] == "fade":
            corefunctions.fade(float(self.cmd[1]), led.Color(self.cmd[2]), led.Color(self.cmd[3]) if len(self.cmd) > 3 else None)

        elif self.cmd[0] == "rf":
            corefunctions.startRandomFade(float(self.cmd[1]), float(self.cmd[2]), float(self.cmd[3]) if len(self.cmd) > 3 else None, float(self.cmd[4]) if len(self.cmd) > 4 else None)

    def stop(self):
        corefunctions.stopFade()


class PulseThread(threading.Thread):
    def __init__(self, threadID, name, cmd):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.cmd = cmd

    def run(self):
        print "Starting Thread: " + self.name
        ##this is a test
        if len(self.cmd) > 3:
            pulse.startPulse(float(self.cmd[1]), led.Color(self.cmd[2]), led.Color(self.cmd[3]))
        else:
            pulse.startPulse(float(self.cmd[1]), led.Color(self.cmd[2]))
        print "Exiting:" + self.name

    def stop(self):
        print "stopping " + self.name
        pulse.stopPulse()


class JumpThread(threading.Thread):
    def __init__(self, threadID, name, cmd):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.cmd = cmd

    def run(self):
        print "Starting Thread: " + self.name
        ##this is a test
        if len(self.cmd) > 3:
            jump.startJump(float(self.cmd[1]), led.Color(self.cmd[2]), led.Color(self.cmd[3]))
        else:
            jump.startJump(float(self.cmd[1]), led.Color(self.cmd[2]))
        print "Exiting:" + self.name

    def stop(self):
        print "stopping " + self.name
        jump.stopJump()

class SpecialThread(threading.Thread):
    def __init__(self, threadID, name, cmd):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.cmd = cmd

    def run(self):
        print "Starting Thread: " + self.name
        if self.cmd[1] == "jamaica":
            specials.startJamaica(self.cmd)
        print "Exiting:" + self.name

    def stop(self):
        print "stopping " + self.name
        specials.stop()


#server socket, which waits for incoming commands and starting actions like fading or simple color changes
def readcommands(threadName, intervall):
    print threadName + " started"

    global CURRENTTHREAD
    CURRENTTHREAD = None

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

            if CURRENTTHREAD != None:
                CURRENTTHREAD.stop()
                CURRENTTHREAD = None

            if command[0] == "cc":
                #led.changeColor(float(command[1]), float(command[2]), float(command[3]))
                led.setColor(led.Color(command[1]))
            elif command[0] == "rf":
                CURRENTTHREAD = FadeThread(1, "fade thread", command)
                CURRENTTHREAD.start()
            elif command[0] == "fade":
                CURRENTTHREAD = FadeThread(2, "fade thread", command)
                CURRENTTHREAD.start()
            elif command[0] == "pulse":
                CURRENTTHREAD = PulseThread(3, "pulse thread", command)
                CURRENTTHREAD.start()
            elif command[0] == "special":
                CURRENTTHREAD = SpecialThread(4, "special thread", command)
                CURRENTTHREAD.start()
            elif command[0] == "jump":
                CURRENTTHREAD = JumpThread(5, "jump thread", command)
                CURRENTTHREAD.start()
            else:
                print "unknown command: '", command, "'"

        except:
            print "Unexpected error: ", sys.exc_info()[0], ": ", sys.exc_info()[1]
        else:
            clientsocket.close()

