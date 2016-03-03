#!/usr/bin/env python

#system modules
import time
import os
import sys
import random
import socket
import string
import thread
import math

#rgb-pi modules
import led
import server
import configure
import log


# rgb representing pins on the raspberry pi GPIO interface
# see: https://github.com/sarfata/pi-blaster

RUN = 0


#command line options		

# choose to the given color. syntax: "./rgb.py c 0.1 0.5 1"
if len(sys.argv)>1:
    if sys.argv[1] == "c":
        r = float(sys.argv[2])
        g = float(sys.argv[3])
        b = float(sys.argv[4])
        led.changeColor(r, g, b)


def startServer(serverThread, var):
    global RUN

    if RUN == 0:
        RUN = 1
    else:
        return

    #readcommands("socket thread", 0.01)
    thread.start_new_thread(server.readcommands, ("socket thread", var, ))
    time.sleep(1)

    log.l("'help' for commands\n\n", log.LEVEL_UI)

    while RUN:
        input = raw_input(">")
        if(input == 'exit'):
            if server.serversocket is not None:
                server.serversocket.close()

            server.RUN = 0
            RUN = 0
            server.triggerManager.stop()

            if server.CurrentCMD is not None:
                server.CurrentCMD.stop()
                server.CurrentCMD.join()
                server.CurrentCMD = None
                
            led.PIGPIO.stop()

            
        if(input == 'help'):
            help = "\n\nCommand list:"
            help = help + "\ncc r g b - change color"
            help = help + "\nclear - clears log"
            help = help + "\nexit - stops the server end kills process"

            log.l(help, log.LEVEL_UI)
        

        if input == 'clear':
            configure.cls()

        if input.startswith('cc'):
            try:
                args = input.split(' ')
                r = float(args[1])
                g = float(args[2])
                b = float(args[3])
                led.changeColor(r, g, b)
            except:
                log.l('ERROR: ' + str(sys.exc_info()[0]) + ": "+ str(sys.exc_info()[1]), log.LEVEL_ERRORS)


# starts server listening to commands: syntax: "./rgb.py server"
try:
    if len(sys.argv)>1 and sys.argv[1] == "server":
        log.l("\nstarting server from console..." , log.LEVEL_UI)
        startServer('server thread', 0.01)
except KeyboardInterrupt:
    if(len(sys.argv)>1 and sys.argv[1] == "server"):
        led.PIGPIO.stop()
        log.l("\nstopping server with errors..." , log.LEVEL_UI)
else:
    if(len(sys.argv)>1 and sys.argv[1] == "server"):
        led.PIGPIO.stop()
        log.l("\nstopping server..." , log.LEVEL_UI)
