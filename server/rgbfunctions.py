import time
import os
import sys
import random
import socket
import string
import thread
import math

RED_PIN_1 = 2
GREEN_PIN_1 = 5
BLUE_PIN_1 = 6

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