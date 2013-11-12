#!/usr/bin/env python
 
import time
import os
 
STEP = 1
DELAY = 0.05
 
def pwm(pin, angle):
    #print "servo[" + str(pin) + "][" + str(angle) + "]"
    cmd = "echo " + str(pin) + "=" + str(angle) + " > /dev/pi-blaster"
    os.system(cmd)
    time.sleep(DELAY)
	

import math
	
def changeColor(r, g, b):
	cmdR = "echo " + str(2) + "=" + str(g) + " > /dev/pi-blaster"
	cmdG = "echo " + str(5) + "=" + str(r) + " > /dev/pi-blaster"
	cmdB = "echo " + str(6) + "=" + str(b) + " > /dev/pi-blaster"
	os.system(cmdR)
	os.system(cmdG)
	os.system(cmdB)
	
 
#while True:
#    for i in range(0, 8):
#        for j in range(0, 100, STEP):
#            pwm(i,j/100.0)   
#    for i in range(0, 8):
#        for j in range(99, 1, (STEP*-1)):
#            pwm(i,j/100.0)

def clip(value):
	if value >= 0.0 and value <= 1.0:
		return value
	else:
		return 0.0
		
def rabs(value):
	if value < 0.0:
		return value * (-1.0)
	else:
		return value
	
		
r = 1.0
g = 1.0
b = 1.0	
changeColor(r,g,b)

			
	
	
	