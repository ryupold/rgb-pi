#!/usr/bin/env python


import time
import os
import sys
import random
import socket
import string
import thread
import math

# rgb representing pins on the raspberry pi GPIO interface
# see: https://github.com/sarfata/pi-blaster
RED_PIN_1 = 2
GREEN_PIN_1 = 5
BLUE_PIN_1 = 6


RUN = 1
COMMAND_RUN = 0

 
def pwm(pin, angle):
    cmd = "echo " + str(pin) + "=" + str(angle) + " > /dev/pi-blaster"
    os.system(cmd)
    time.sleep(0.05)
	
# elementary function to change the color of the LED strip
def changeColor(r, g, b):
	cmdR = "echo " + str(RED_PIN_1) + "=" + str(g) + " > /dev/pi-blaster"
	cmdG = "echo " + str(GREEN_PIN_1) + "=" + str(r) + " > /dev/pi-blaster"
	cmdB = "echo " + str(BLUE_PIN_1) + "=" + str(b) + " > /dev/pi-blaster"
	os.system(cmdR)
	os.system(cmdG)
	os.system(cmdB)
	
 
# if value is not in range between 0.0 and 1.0, it returns 0.0
def clip(value):
	if value >= 0.0 and value <= 1.0:
		return value
	else:
		return 0.0


def socket_thread(intervall):
	#create an INET, STREAMing socket
	serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
	#socket options
	serversocket.setblocking(1)
	serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	
	#bind the socket to a public host,
	# and a well-known port
	serversocket.bind(('', 4321)) # socket.gethostname()
	
	#become a server socket
	serversocket.listen(5)
	while RUN:
		try:
			(clientsocket, address) = serversocket.accept()
			#rgb = string.split(string.replace(str(clientsocket.recv(1024)), ",", "."))
			command = clientsocket.recv(1024);
		except:
			print "Unexpected error:", sys.exc_info()[0]
		else:
			clientsocket.close()

		
#command line options		

# choose to the given color. syntax: "./rgb.py c 0.1 0.5 1"
if sys.argv[1] == "c":
	r = float(sys.argv[2])
	g = float(sys.argv[3])
	b = float(sys.argv[4])
	changeColor(r,g,b)


# starts server listening to commands: syntax: "./rgb.py server"
if sys.argv[1] == "server":
	thread.start_new_thread(socket_thread, (0.01))
		
		
			
		
	
	