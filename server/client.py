#!/usr/bin/env python

# this script is for testing commands, which are sent to the rgb-pi server
#python modules
import socket
import sys

#rgb-pi modules
import log



if len(sys.argv) > 1:
    if sys.argv[1] == "command" and len(sys.argv) > 2:
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