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
import tasks

RUN = 1
serversocket = None
ID = 1
CurrentCMD = None
CurrentFilters = []




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
        #TODO


        self.stop()
        log.l("Exiting:" + self.name, log.LEVEL_START_STOP_THREADS)

    #stops this thread, disregarding when its expiration should be
    def stop(self):
        log.l("stopping " + self.name, log.LEVEL_START_STOP_THREADS)

        #stop timer
        if self.timer is not None:
            self.timer.cancel()
            self.timer = None

        self.state = constants.CMD_STATE_EXPIRED


#server socket, which waits for incoming commands and starting actions like fading or simple color changes
def readcommands(threadName, intervall):
    #print the config parameters
    configure.cls()
    configure.printConfig()

    log.l('\n... starting server...\n\n', log.LEVEL_UI)

    #globals
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

            global CurrentCMD
            global CurrentFilters

            rcvString = str(clientsocket.recv(1024))
            log.l('RECEIVED: '+rcvString+'\n\n')
            answer = {}

            try:
                r = json.loads(rcvString)

                if r.has_key('commands') and len(r['commands']) > 0:
                    try:
                        log.l( 'commands: '+ str(len(r['commands'])), log.LEVEL_COMMANDS)

                        if CurrentCMD is not None:
                            CurrentCMD.stop()
                        CurrentCMD = tasks.Task.createTask(r['commands'])
                        CurrentFilters = []
                        answer['commands'] = 1

                    except:
                        log.l('ERROR: ' + str(sys.exc_info()[0])+ ": "+ str(sys.exc_info()[1]), log.LEVEL_ERRORS)
                        answer['commands'] = 0
                else:
                    answer['commands'] = 0

                #TODO create filters

                #TODO answer requests

                #starting a new command if a new arrived and could be correctly decoded
                if answer['commands'] == 1:
                    CurrentCMD.start()


                log.l('---ANSWER---', log.LEVEL_ANSWER)
                log.l(str(answer), log.LEVEL_ANSWER)

            except:
                clientsocket.send(json.dumps(answer, separators=(',',':')))
            else:
                clientsocket.send(json.dumps(answer, separators=(',',':')))

            ### old format
            #command = string.split(string.strip(rcvString))
            #if len(command) > 0:
            #    if command[0] == "cc":
            #        log.l(command, log.LEVEL_COMMAND_CC)
            #    else:
            #        log.l(command, log.LEVEL_COMMANDS)

#                ID += 1
#                cmdT = CommandThread(ID, string.lower(command[0]), command)
#            else:
#                raise AttributeError("no commands received!")
            ### old format


        except:
            log.l('ERROR: ' + str(sys.exc_info()[0])+ ": "+ str(sys.exc_info()[1]), log.LEVEL_ERRORS)
        else:
            clientsocket.close()

