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

import colorFader
import timedDimmer
import pulse
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
        print "Starting Thread: " + self.name
        ##this is a test
        colorFader.startFade(int(self.cmd[1]), int(self.cmd[2]), int(self.cmd[3]), int(self.cmd[4]))
        print "Exiting:" + self.name

    def stop(self):
        print "stopping " + self.name
        colorFader.stopFade()


class FadeThread(threading.Thread):
    def __init__(self, threadID, name, cmd):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.cmd = cmd

    def run(self):
        if len(self.cmd) > 2:
            corefunctions.fade(int(self.cmd[1]), led.Color(self.cmd[2]), led.Color(self.cmd[3]))
        else:
            corefunctions.fade(int(self.cmd[1]), led.Color(self.cmd[2]))

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
        pulse.startPulse(int(self.cmd[1]), self.cmd[2], self.cmd[3])
        print "Exiting:" + self.name

    def stop(self):
        print "stopping " + self.name
        pulse.stopPulse()


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
                led.changeColor(float(command[1]), float(command[2]), float(command[3]))
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
            else:
                print "unknown command: '", command, "'"

        except:
            print "Unexpected error: ", sys.exc_info()[0], ": ", sys.exc_info()[1]
        else:
            clientsocket.close()

