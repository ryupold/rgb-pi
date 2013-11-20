#! /usr/bin/env python

import utils
import time
import math
import rgbfunctions
import sys

######################
#### USER INPUT ######
######################
minutesToDim = 1		#Time to dim, minutes
startColor = 'FF4444'		#Color to start with
######################
#### END U I #########
######################


RUN = 0

#dims/fades the current color to black 000000 over 'secondsToDim'
def dimCurrentColor(secondsToDim):
	startDim(secondsToDim, utils.getColorString([int(rgbfunctions.RED*255), int(rgbfunctions.GREEN*255), int(rgbfunctions.BLUE*255)]))

#dims/fades the current color to the 'endColorHex' over 'secondsToDim'
def fadeCurrentColor(secondsToDim, endColorHex):
	startDim(secondsToDim, utils.getColorString([int(rgbfunctions.RED*255), int(rgbfunctions.GREEN*255), int(rgbfunctions.BLUE*255)]), endColorHex)
	
#dims/fades the 'startColor' over 'secondsToDim' to 'endColor' (default is black 000000)
def startDim(secondsToDim, startColor, endColor=None):
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
	
	while ((myrun == RUN) and secondsPassed < secondsToDim):

		now = time.time()
		secondsPassed = now - startTime
		
		#interpolate new color		
		currentColor[0] = max(0, utils.interpolateColor(startColorArray[0], endColorArray[0], 1.0*secondsPassed/(secondsToDim)))
		currentColor[1] = max(0, utils.interpolateColor(startColorArray[1], endColorArray[1], 1.0*secondsPassed/(secondsToDim)))
		currentColor[2] = max(0, utils.interpolateColor(startColorArray[2], endColorArray[2], 1.0*secondsPassed/(secondsToDim)))
		
		#print currentColor

		R = currentColor[0] / 255.0
		G = currentColor[1] / 255.0
		B = currentColor[2] / 255.0
		
		rgbfunctions.changeColor(R, G, B)

		#next step
		time.sleep(secondsBetweenChange)

		
def stopDim():
	global RUN
	RUN = RUN + 1