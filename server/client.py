#!/usr/bin/env python

# this script is for testing commands, which are sent to the rgb-pi server
#python modules
import socket
import sys

#rgb-pi modules
import log


print sys.argv

if len(sys.argv) > 1:
    if len(sys.argv) >= 2 and sys.argv[1] == "command":
        try:
            clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #clientsocket.connect(("192.168.1.150", 4321))
            clientsocket.connect(("localhost", 4321))

            cmdString = ""
            for s in range(2, len(sys.argv)):
                if len(cmdString) > 0:
                    cmdString += " "
                cmdString += str(sys.argv[s])

            print "sending command "+ cmdString
            clientsocket.send(cmdString)
            clientsocket.close()
        except socket.error:
            log.l(str(sys.exc_info()[0])+ ": "+ str(sys.exc_info()[1]))


    if len(sys.argv) >= 2 and sys.argv[1] == "test":
        try:
            clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #clientsocket.connect(("192.168.1.150", 4321))
            if len(sys.argv) > 2:
                clientsocket.connect((sys.argv[2], 4321))
                print "connected to ", sys.argv[2]
            else:
                clientsocket.connect(("localhost", 4321))
                print "connected to localhost"

            cmdFile = open('test.js', 'r+')
            cmdString = "{}"

            print "sending command "+ cmdString
            clientsocket.send(cmdString)
            clientsocket.close()
        except socket.error:
            log.l(str(sys.exc_info()[0])+ ": "+ str(sys.exc_info()[1]))