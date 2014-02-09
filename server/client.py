# this script is for testing commands, which are sent to the rgb-pi server
#python modules
import socket
import sys

#rgb-pi modules
import server



if len(sys.argv) > 1:
    if sys.argv[1] == "command" and len(sys.argv) > 2:
        try:
            clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            clientsocket.connect(("localhost", 4321))
            clientsocket.send(str(sys.argv[2:]))
        except socket.error:
            server.log.l(str(sys.exc_info()[0])+ ": "+ str(sys.exc_info()[1]))


