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

import config
import configure
import log
import constants
import requests
import tasks

RUN = 1
serversocket = None
ID = 0
CurrentCMD = None
CurrentFilters = []




#mega thread class
class CommandThread(threading.Thread):
    #ctor
    def __init__(self, threadID, name, cmd):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.state = constants.CMD_STATE_INIT
        self.task = tasks.Task.createTask(cmd['commands'], self)

    #method, which is executed when the .start() method of the thread is called
    def run(self):
        if log.m(log.LEVEL_START_STOP_THREADS): log.l('<'+str(self.threadID)+'> starting Thread: ' + self.name)
        self.state = constants.CMD_STATE_STARTED

        self.task.start()

        self.stop()
        if log.m(log.LEVEL_START_STOP_THREADS): log.l('<'+str(self.threadID)+'> exiting:' + self.name)

    #stops this thread, disregarding when its expiration should be
    def stop(self):
        if log.m(log.LEVEL_START_STOP_THREADS): log.l('<'+str(self.threadID)+'> stopping ' + self.name)
        self.state = constants.CMD_STATE_STOPPED
        self.task.stop()



#server socket, which waits for incoming commands and starting actions like fading or simple color changes
def readcommands(threadName, intervall):
    #print the config parameters
    configure.cls()
    configure.printConfig()

    print '\n... starting server...\n\n'

    #globals
    global ID
    global serversocket

    #create an INET, STREAMing socket
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    #bind the socket to a public host,
    # and a well-known port
    success = False
    while not success:
        try:
            log.l('trying to bind on port '+str(config.SERVER_PORT)+'...', log.LEVEL_UI)
            serversocket.bind(('', config.SERVER_PORT)) # socket.gethostname() # for getting own address
            success = True
            log.l('successfully bound server to port '+str(config.SERVER_PORT)+'...', log.LEVEL_UI)
        except:
            log.l('port is already in use. Trying to reconnect in 5 seconds', log.LEVEL_ERRORS)
            time.sleep(5)

    #become a server socket
    serversocket.listen(5)


    while RUN:
        try:
            (clientsocket, address) = serversocket.accept()

            global CurrentCMD
            global CurrentFilters

            rcvString = str(clientsocket.recv(1024))
            if log.m(log.LEVEL_SOCKET_COMMUNICATION): log.l('RECEIVED: '+rcvString+'\n\n')
            answer = {}
            answer['error'] = []

            try:
                r = json.loads(rcvString)

                if isinstance(r, dict) and r.has_key('commands') and len(r['commands']) > 0:
                    try:
                        if log.m(log.LEVEL_COMMANDS): log.l( 'commands: '+ str(len(r['commands'])))

                        if CurrentCMD is not None:
                            CurrentCMD.stop()
                            CurrentCMD.join()
                            CurrentCMD = None

                        ID = ID + 1
                        CurrentCMD = CommandThread(ID, 'command thread', r)
                        CurrentFilters = []
                        answer['commands'] = 1

                    except:
                        answer['error'].append('ERROR: ' + str(sys.exc_info()[0]) + ": "+ str(sys.exc_info()[1]))
                        answer['commands'] = 0
                        log.l('ERROR: ' + str(sys.exc_info()[0]) + ": "+ str(sys.exc_info()[1]), log.LEVEL_ERRORS)
                else:
                    answer['commands'] = 0

                #TODO create filters

                #TODO answer requests
                if isinstance(r, dict) and r.has_key('request'):
                    try:
                        req = requests.Request.createRequest(r['request'])
                        answer['request'] = req.execute()
                    except:
                        answer['error'].append('ERROR: ' + str(sys.exc_info()[0]) + ": "+ str(sys.exc_info()[1]))
                        log.l('ERROR: ' + str(sys.exc_info()[0]) + ": "+ str(sys.exc_info()[1]), log.LEVEL_ERRORS)


                #starting a new command if a new arrived and could be correctly decoded
                if answer['commands'] == 1:
                    CurrentCMD.start()


                if log.m(log.LEVEL_SOCKET_COMMUNICATION):
                    log.l('---ANSWER---')
                    log.l(str(answer))

            except:
                log.l('ERROR: ' + str(sys.exc_info()[0]) + ": "+ str(sys.exc_info()[1]), log.LEVEL_ERRORS)
                answer['error'].append(str(sys.exc_info()[0]) + ": "+ str(sys.exc_info()[1]))
                clientsocket.send(json.dumps(answer, separators=(',',':')))
            else:
                clientsocket.send(json.dumps(answer, separators=(',',':')))

        except:
            log.l('ERROR: ' + str(sys.exc_info()[0])+ ": "+ str(sys.exc_info()[1]), log.LEVEL_ERRORS)
        else:
            clientsocket.close()

