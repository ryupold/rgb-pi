#server threads
 
import time
import os
import sys
import random
import socket
import string
import thread
import math
import rgbfunctions
import colorFader


RUN = 1
COMMAND_RUN = 0



#server socket, which waits for incoming commands and starting actions like fading or simple color changes
def readcommands(threadName, intervall):
	print threadName+" started"
	#create an INET, STREAMing socket
	serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
	#bind the socket to a public host,
	# and a well-known port
	serversocket.bind(('', 4321)) # socket.gethostname()
	
	#become a server socket
	serversocket.listen(5)
	while RUN:
		try:
			(clientsocket, address) = serversocket.accept()
			#rgb = string.split(string.replace(str(clientsocket.recv(1024)), ",", "."))
			#command = clientsocket.recv(1024)
			
			command = string.split(string.replace(str(clientsocket.recv(1024)), ",", "."))
			
			if command[0] == "cc":
				print "changing color: "+command[1]+" "+command[2]+ " " +command[3]
				rgbfunctions.changeColor(float(command[1]), float(command[2]), float(command[3]))
			elif command[0] == "rf":
				colorFader.startFade(2, 100, 0, 50)
			else:
				print command
				
			
		except:
			pass
			#print "Unexpected error:", sys.exc_info()[0]
		else:
			clientsocket.close()


		
		
			
		
	
	