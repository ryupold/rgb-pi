#! /usr/bin/env python

import random
import time
import rgbfunctions
import math
import utils

RUN = 0

def pulse():
	try:
		i = 0
		global RUN
		myrun = RUN
		while (myrun == RUN):
			global speed
			global endColor
			global colorToPulse
			
			current = utils.getIntComponents(getCurrentColor())
			end = utils.getIntComponents(endColor)
			
			
			#If is already same color, start fade to new random color
			if ((abs(current[0] - end[0]) <= 4) and (abs(current[1] - end[1]) <= 4) and (abs(current[2] - end[2]) <= 4)):
				if (getCurrentColor() == colorToPulse):
					endColor = '000000'
				else:
					endColor = colorToPulse
			else:
				

				
				#####################################
				##### XTC Fader!!!!!!!!!! ###########
				#####################################
				#current[0] = random.randint(0, 255)
				#current[1] = random.randint(0, 255)
				#current[2] = random.randint(0, 255)
				#####################################
				#####################################
				
				setColor(utils.getColorString(current))

				i = i + 1
				if (i == changeSpeedAfter):
					speed = random.randint(minSpeed, maxSpeed)
					i = 1
					
				#print 'speed: '+str(speed)
				#print 'i: '+str(i)
				time.sleep(speed / 1000.0)
			#fade(endColor)
	except:
		print 'FEHLER!!!', sys.exc_info()[0]


#Set new color
#Param color String (i.e. "FF0000")
def setColor(color):
	c = utils.getIntComponents(color)
	R = c[0] / 255.0
	G = c[1] / 255.0
	B = c[2] / 255.0
	global currentColor
	#print currentColor+'test'
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

def startPulse(color, pulseSpeed):
	global speed
	speed = pulseSpeed
	global endColor
	endColor = color
	global colorToPulse
	colorToPulse = color
	setColor('000000')
	
	pulse()
