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

def dim(minutesToDim, startColor):
	global RUN
	myrun = RUN

	currentColor = utils.getIntComponents(startColor)

	#Now, in seconds
	startTime = int(time.time())

	#time to dim, seconds
	secondsToDim = minutesToDim * 60

	#time, when lights should go out
	endTime = startTime + secondsToDim

	#startColor as Array
	startColorArray = utils.getIntComponents(startColor)

	#time between two steps for R
	secondsBetweenRChange = (sys.maxint if startColorArray[0] == 0 else secondsToDim / float(startColorArray[0]))

	#time between two steps for G
	secondsBetweenGChange = (sys.maxint if startColorArray[1] == 0 else secondsToDim / float(startColorArray[1]))

	#time between two steps for B
	secondsBetweenBChange = (sys.maxint if startColorArray[2] == 0 else secondsToDim / float(startColorArray[2]))

	#time between to steps
	secondsBetweenChange = min(min(secondsBetweenRChange, secondsBetweenGChange), secondsBetweenBChange)
		
	while ((myrun == RUN) and ((currentColor[0] > 0) or (currentColor[1] > 0) or (currentColor[2] > 0))):

		now = time.time()
		secondsPassed = now - startTime

		#Set new color (startcolor - (seconds passed * stepsPerSecond))
		currentColor[0] = max(0, startColorArray[0] - int((secondsPassed * (startColorArray[0] / secondsToDim))))
		currentColor[1] = max(0, startColorArray[1] - int((secondsPassed * (startColorArray[1] / secondsToDim))))
		currentColor[2] = max(0, startColorArray[2] - int((secondsPassed * (startColorArray[2] / secondsToDim))))

		R = currentColor[0] / 255.0
		G = currentColor[1] / 255.0
		B = currentColor[2] / 255.0

		rgbfunctions.changeColor(R, G, B)

		#next step
		time.sleep(secondsBetweenChange)
