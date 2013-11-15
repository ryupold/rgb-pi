#!/usr/bin/env python
 
import time
import os
import sys
import random
import socket
import string
import thread
import math



#server threads
def socket_thread(threadName, intervall):
	
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
			command = clientsocket.recv(1024)
			#print command
		except:
			pass
			#print "Unexpected error:", sys.exc_info()[0]
		else:
			clientsocket.close()


		
		
			
		
	
	