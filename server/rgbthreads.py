#server threads
 
import time
import os
import sys
import random
import socket
import string
import thread
import threading
import math
import rgbfunctions
import colorFader


RUN = 1
COMMAND_RUN = 0
CURRENTTHREAD = None

class FadeThread (threading.Thread):
	def __init__(self, threadID, name, cmd):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.cmd = cmd
	def run(self):
		print "Starting Thread: " + self.name
		##this is a test
		#colorFader.startFade(2, 100, 0, 50)
		colorFader.startFade(int(self.cmd[1]), int(self.cmd[2]), int(self.cmd[3]), int(self.cmd[4]))
		print "Exiting:" + self.name
	def stop(self):
		print "stopping "+self.name
		colorFader.stopFade()
		
	


#server socket, which waits for incoming commands and starting actions like fading or simple color changes
def readcommands(threadName, intervall):
	print threadName+" started"
	
	global CURRENTTHREAD
	CURRENTTHREAD = None
	
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
			command = string.split(string.replace(str(clientsocket.recv(1024)), ",", "."))
			## put this line in, if commas need to be sent in a command!!
			#command = string.split(str(clientsocket.recv(1024)))
			
			if CURRENTTHREAD != None:
				CURRENTTHREAD.stop()
				CURRENTTHREAD = None
			
			if command[0] == "cc":
				rgbfunctions.changeColor(float(command[1]), float(command[2]), float(command[3]))
			elif command[0] == "rf":
				CURRENTTHREAD = FadeThread(1, "fade thread", command)
				CURRENTTHREAD.start()
			else:
				print "unknown command: '", command, "'"
				
			
		except:
			print "Unexpected error: ", sys.exc_info()[0], ": ",sys.exc_info()[1]
		else:
			clientsocket.close()


		
		
			
		
	
	