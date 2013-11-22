#!/usr/bin/env python


import time
import os
import sys
import random
import socket
import string
import thread
import math
import rgbfunctions
import rgbthreads


# rgb representing pins on the raspberry pi GPIO interface
# see: https://github.com/sarfata/pi-blaster

RUN = 1

rgbfunctions.RED = 0
rgbfunctions.GREEN = 0
rgbfunctions.BLUE = 0
		
#command line options		

# choose to the given color. syntax: "./rgb.py c 0.1 0.5 1"
if sys.argv[1] == "c":
	r = float(sys.argv[2])
	g = float(sys.argv[3])
	b = float(sys.argv[4])
	rgbfunctions.changeColor(r,g,b)


# starts server listening to commands: syntax: "./rgb.py server"
if sys.argv[1] == "server":
	#readcommands("socket thread", 0.01)
	thread.start_new_thread(rgbthreads.readcommands, ("socket thread", 0.01, ))
	while RUN:
		time.sleep(1)

		
			
		
	
	