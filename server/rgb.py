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

RUN = 1


#command line options		

# choose to the given color. syntax: "./rgb.py c 0.1 0.5 1"
if sys.argv[1] == "c":
    r = float(sys.argv[2])
    g = float(sys.argv[3])
    b = float(sys.argv[4])
    led.changeColor(r, g, b)


# starts server listening to commands: syntax: "./rgb.py server"
if sys.argv[1] == "server":
    #readcommands("socket thread", 0.01)
    thread.start_new_thread(server.readcommands, ("socket thread", 0.01, ))
    time.sleep(1)
    print "'help' for commands\n\n"
    while RUN:
        input = raw_input(">")
        if(input == 'exit'):
            if server.serversocket is not None:
                server.serversocket.close()

            server.RUN = 0
            RUN = 0

            if server.CurrentCMD is not None:
                server.CurrentCMD.stop()
                server.CurrentCMD.join()
                server.CurrentCMD = None


            #led.changeColor(0,0,0,0xF)

        if(input == 'help'):
            help = "\n\nCommand list:"
            help = help + "\nc r g b - change color"
            help = help + "\nclear - clears log"
            help = help + "\nexit - stops the server end kills process"

            print help


        if input == 'clear':
            configure.cls()

        if input.startswith('c'):
            try:
                args = input.split(' ')
                r = float(args[1])
                g = float(args[2])
                b = float(args[3])
                led.changeColor(r, g, b)
            except:
                log.l('ERROR: ' + str(sys.exc_info()[0]) + ": "+ str(sys.exc_info()[1]), log.LEVEL_ERRORS)
