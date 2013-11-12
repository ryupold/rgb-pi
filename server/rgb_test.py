#!/usr/bin/env python
 
import time
import os
 
STEP = 100
DELAY = 0.5
 
def pwm(pin, angle):
    print "servo[" + str(pin) + "][" + str(angle) + "]"
    cmd = "echo " + str(pin) + "=" + str(angle) + " > /dev/servoblaster"
    os.system(cmd)
    time.sleep(DELAY)
 
while True:
    for i in range(0, 8):
        for j in range(1, 249, STEP):
            pwm(i,j)   
    for i in range(0, 8):
        for j in range(249, 1, (STEP*-1)):
            pwm(i,j)