# this script is for testing commands, which are sent to the rgb-pi server
#python modules
import socket
import sys


if len(sys.argv) > 1:
    if sys.argv[1] == "command":
        clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
