#! /usr/bin/env python

import random
import time
import rgbfunctions
import math
import utils
import sys

RUN = 0


#Set new color
#Param color String (i.e. "FF0000")
def setColor(color):
	c = utils.getIntComponents(color)
	R = c[0] / 255.0
	G = c[1] / 255.0
	B = c[2] / 255.0
	global currentColor
	#print color
	currentColor = color
	rgbfunctions.changeColor(R, G, B)

#Returns Array with integer RGB components
def getRandomColor():
	global max
	global min
	R = random.randint(min, max)
	G = random.randint(min, max)
	B = random.randint(min, max)
	
	return [R, G, B]

#Returns the currently set color
def getCurrentColor():
	return currentColor


endColor = '0000FF'
speed = 100
currentColor = '000000'
colorToPulse = endColor
	
def stopPulse():
	global RUN
	RUN = RUN + 1

def startPulse(secondsToDim, startColor, endColor=None):
	global RUN
	myrun = RUN

	currentColor = utils.getIntComponents(startColor)

	#Now, in seconds
	startTime = int(time.time())
	

	#time, when lights should go out
	endTime = startTime + secondsToDim

	#startColor as Array
	startColorArray = utils.getIntComponents(startColor)
	R = startColorArray[0] / 255.0
	G = startColorArray[1] / 255.0
	B = startColorArray[2] / 255.0
	rgbfunctions.changeColor(R, G, B)
	
	#endColor is a defaultValue
	if endColor is None:
		endColor = '000000'
	endColorArray = utils.getIntComponents(endColor)
		#time between two steps for R
	secondsBetweenRChange = (sys.maxint if startColorArray[0] == 0 else secondsToDim / float(startColorArray[0]))

	#time between two steps for G
	secondsBetweenGChange = (sys.maxint if startColorArray[1] == 0 else secondsToDim / float(startColorArray[1]))

	#time between two steps for B
	secondsBetweenBChange = (sys.maxint if startColorArray[2] == 0 else secondsToDim / float(startColorArray[2]))

	#time between to steps
	secondsBetweenChange = min(min(secondsBetweenRChange, secondsBetweenGChange), secondsBetweenBChange)
	
	secondsPassed = 0
	
	while (myrun == RUN):

		now = time.time()
		secondsPassed = now - startTime
		
		#interpolate new color		
		currentColor[0] = max(0, utils.interpolateColor(startColorArray[0], endColorArray[0], 1.0*secondsPassed/(secondsToDim)))
		currentColor[1] = max(0, utils.interpolateColor(startColorArray[1], endColorArray[1], 1.0*secondsPassed/(secondsToDim)))
		currentColor[2] = max(0, utils.interpolateColor(startColorArray[2], endColorArray[2], 1.0*secondsPassed/(secondsToDim)))
		

		R = currentColor[0] / 255.0
		G = currentColor[1] / 255.0
		B = currentColor[2] / 255.0

		
		rgbfunctions.changeColor(R, G, B)
		
		if (secondsPassed >= secondsToDim):
			tempColor = endColorArray
			endColorArray = startColorArray
			startColorArray = tempColor
			startTime = time.time()

		#next step
		time.sleep(secondsBetweenChange)
	
def stopPulse():
	global RUN
	RUN = RUN + 1
