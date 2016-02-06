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
import urllib


#rgb-pi modules

import config
import configure
import log
import constants
import requests
import tasks
import filters
import trigger
import led
#import rest

RUN = 1
serversocket = None
mutex = threading.BoundedSemaphore()
ID = 0
CurrentCMD = None
CurrentFilters = []
CommandHistory = []
CommandCount = 0

#starting trigger thread
triggerManager = trigger.TriggerManager(-10, 'Trigger Manager')
triggerManager.start()


class CommandThread(threading.Thread):
    """
    command thread class which holds the root command/list.
    there can only be one command thread running at a time.
    """
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


    def isStarted(self):
        return self.state == constants.CMD_STATE_STARTED

    def isStopped(self):
        return self.state == constants.CMD_STATE_STOPPED

    def isInitialized(self):
        return self.state == constants.CMD_STATE_INIT

    def getThreadID(self):
        return self.threadID




#server socket, which waits for incoming commands and starting actions like fading or simple color changes
def readcommands(threadName, intervall):
    #print the config parameters
    configure.cls()
    configure.printConfig()

    print '\n... starting server (',intervall,')...\n\n'

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
            global CommandHistory
            global CommandCount


            rcvString = ''
            clientsocket.setblocking(1) # recv() waits til data comes or timeout is reached
            clientsocket.settimeout(config.CONNECTION_TIMEOUT) # timeout for receiving and sending
            kilobyte = str(clientsocket.recv(1024))
            try:
                while(kilobyte):
                    rcvString += kilobyte
                    try:
                        json.loads(rcvString)
                        kilobyte = None
                    except:
                        kilobyte = str(clientsocket.recv(1024))
            except:
                pass

            #flag which is true if the received command comes from a http request
            isHTTPRequest = False

            mutex.acquire()
            try:
                answer = {}
                answer['error'] = []
                if log.m(log.LEVEL_SOCKET_COMMUNICATION): log.l('RECEIVED SOCKET ('+str(len(rcvString))+'): '+rcvString+'\n\n')

                if rcvString.startswith('GET') or rcvString.startswith('OPTIONS') or rcvString.startswith('POST') or rcvString.startswith('PUT'):
                    isHTTPRequest = True
                    rcvString = urllib.unquote(str.split(rcvString, '\n', 1)[1])
                    if log.m(log.LEVEL_SOCKET_COMMUNICATION): log.l('RECEIVED HTTP ('+str(len(rcvString))+'): '+rcvString+'\n\n')

                    startIndex = rcvString.find('{')
                    endIndex = rcvString.rfind('}')
                    if startIndex >= 0 and endIndex >= 0:
                        rcvString = rcvString[rcvString.find('{'):rcvString.rfind('}')+1]
                        if log.m(log.LEVEL_SOCKET_COMMUNICATION): log.l('RECEIVED Command ('+str(len(rcvString))+'): '+rcvString+'\n\n')
                    else:
                        if log.m(log.LEVEL_SOCKET_COMMUNICATION): log.l('no valid command found in ('+str(len(rcvString))+'): '+rcvString+'\n\n')
                else:
                    isHTTPRequest = False
                    if log.m(log.LEVEL_SOCKET_COMMUNICATION): log.l('RECEIVED Command ('+str(len(rcvString))+'): '+rcvString+'\n\n')



                r = json.loads(rcvString)
                CommandCount += 1
                CommandHistory.append(r)
                #limit command history to the last 10 commands (client request messages)
                if len(CommandHistory) > 10:
                    CommandHistory = CommandHistory[len(CommandHistory)-10:len(CommandHistory)]

                # execute commands
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


                #add new filters if a command is running
                if isinstance(r, dict) and r.has_key('filters') and len(r['filters']) > 0 and CurrentCMD is not None and CurrentCMD.state != constants.CMD_STATE_STOPPED:
                    try:
                        for f in r['filters']:
                            CurrentFilters.append(filters.Filter.createFilter(f))
                        answer['filters'] = 1
                    except:
                        answer['error'].append('ERROR: ' + str(sys.exc_info()[0]) + ": "+ str(sys.exc_info()[1]))
                        answer['filters'] = 0
                        log.l('ERROR: ' + str(sys.exc_info()[0]) + ": "+ str(sys.exc_info()[1]), log.LEVEL_ERRORS)

                #answer request
                if isinstance(r, dict) and r.has_key('request'):
                    try:
                        req = requests.Request.createRequest(r['request'])
                        answer['request'] = req.execute()
                    except:
                        answer['error'].append('ERROR: ' + str(sys.exc_info()[0]) + ": "+ str(sys.exc_info()[1]))
                        answer['request'] = None
                        log.l('ERROR: ' + str(sys.exc_info()[0]) + ": "+ str(sys.exc_info()[1]), log.LEVEL_ERRORS)

                #add new triggers
                if isinstance(r, dict) and r.has_key('triggers') and len(r['triggers']) > 0:
                    try:
                        for t in r['triggers']:
                            triggerManager.addTrigger(trigger.Trigger(t))
                        answer['triggers'] = 1
                    except:
                        answer['error'].append('ERROR: ' + str(sys.exc_info()[0]) + ": "+ str(sys.exc_info()[1]))
                        answer['triggers'] = 0
                        log.l('ERROR: ' + str(sys.exc_info()[0]) + ": "+ str(sys.exc_info()[1]), log.LEVEL_ERRORS)


                #starting a new command if a new arrived and could be correctly decoded
                if answer.has_key('commands') and answer['commands'] == 1:
                    CurrentCMD.start()


                if log.m(log.LEVEL_SOCKET_COMMUNICATION):
                    log.l('---ANSWER---')
                    log.l(str(answer))

            except:
                log.l('ERROR: ' + str(sys.exc_info()[0]) + ": "+ str(sys.exc_info()[1]), log.LEVEL_ERRORS)
                answer['error'].append(str(sys.exc_info()[0]) + ": "+ str(sys.exc_info()[1]))
                #clientsocket.send(json.dumps(answer, separators=(',',':')))


            mutex.release()

            if isHTTPRequest:
                answerString = json.dumps(answer, separators=(',',':'))
                httpResponse = 'HTTP/1.1 200 OK\n'
                httpResponse = httpResponse + 'Content-Type: application/json;charset=utf-8\n'
                httpResponse = httpResponse + 'Access-Control-Allow-Origin: *\n'
                httpResponse = httpResponse + 'Content-Length: '+str(len(answerString))+'\n\n'
                httpResponse = httpResponse + answerString
                clientsocket.send(httpResponse)
                log.l('answer sent (http response)', log.LEVEL_SOCKET_COMMUNICATION)
            else:
                clientsocket.send(json.dumps(answer, separators=(',',':')))
                log.l('answer sent (normal socket)', log.LEVEL_SOCKET_COMMUNICATION)

            clientsocket.close()

        except:
            log.l('ERROR: ' + str(sys.exc_info()[0])+ ": "+ str(sys.exc_info()[1]), log.LEVEL_ERRORS)






def applyCommand(r):
    """
    This method can be used from other scripts like triggers.py to apply commands to the server
    :param r: json object with command
    :return: None
    """

    global ID
    global serversocket
    global CurrentCMD
    global CurrentFilters
    global CommandHistory
    global CommandCount

    answer = {}
    mutex.acquire()
    try:
        answer['error'] = []
        CommandCount += 1
        CommandHistory.append(r)
        #limit command history to the last 10 commands (client request messages)
        if len(CommandHistory) > 10:
            CommandHistory = CommandHistory[len(CommandHistory)-10:len(CommandHistory)]

        contains_cmd = False

        # execute commands
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
                contains_cmd = True

            except:
                log.l('ERROR: ' + str(sys.exc_info()[0]) + ": "+ str(sys.exc_info()[1]), log.LEVEL_ERRORS)


        #add new filters if a command is running
        if isinstance(r, dict) and r.has_key('filters') and len(r['filters']) > 0 and CurrentCMD is not None and CurrentCMD.state != constants.CMD_STATE_STOPPED:
            try:
                for f in r['filters']:
                    CurrentFilters.append(filters.Filter.createFilter(f))
            except:
                log.l('ERROR: ' + str(sys.exc_info()[0]) + ": "+ str(sys.exc_info()[1]), log.LEVEL_ERRORS)

        #answer request
        if isinstance(r, dict) and r.has_key('request'):
            try:
                req = requests.Request.createRequest(r['request'])
                req.execute()
            except:
                log.l('ERROR: ' + str(sys.exc_info()[0]) + ": "+ str(sys.exc_info()[1]), log.LEVEL_ERRORS)


        #add new triggers
        if isinstance(r, dict) and r.has_key('triggers') and len(r['triggers']) > 0:
            try:
                for t in r['triggers']:
                    triggerManager.addTrigger(trigger.Trigger(t))
            except:
                log.l('ERROR: ' + str(sys.exc_info()[0]) + ": "+ str(sys.exc_info()[1]), log.LEVEL_ERRORS)

        #starting a new command if a new arrived and could be correctly decoded
        if contains_cmd:
            CurrentCMD.start()
    except:
        log.l('ERROR: ' + str(sys.exc_info()[0]) + ": "+ str(sys.exc_info()[1]), log.LEVEL_ERRORS)

    mutex.release()
    return answer
