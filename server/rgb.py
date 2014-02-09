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
import rgbthreads
import configure


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
    thread.start_new_thread(rgbthreads.readcommands, ("socket thread", 0.01, ))
    time.sleep(1)
    print "'help' for commands\n\n"
    while RUN:
        input = raw_input(">")
        if(input == 'exit'):
            if rgbthreads.serversocket is not None:
                rgbthreads.serversocket.close()
                rgbthreads.RUN = 0
            RUN = 0
            led.changeColor(0,0,0,0xF)

        if(input == 'help'):
            print "\n\nCommand list:\nexit - stops the server end kills process\nclear - clears log\n"

        if input == 'clear':
            configure.cls()
