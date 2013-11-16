#! /usr/bin/env python

import random
import time
import rgbfunctions
import math

def fade(endColor):
	try:
		i = 0
		while (1):
			global speed
			global endcolor
			global minSpeed
			global maxSpeed
			global changeSpeedAfter
			
			
			current = getIntComponents(getCurrentColor())
			end = endColor
			
			#print 'Target: '+str(end[0])+', '+str(end[1])+', '+str(end[2])
			#print 'Current: '+str(current[0])+', '+str(current[1])+', '+str(current[2])
			#print ''
			
			#If is already same color, start fade to new random color
			if ((abs(current[0] - end[0]) <= 4) and (abs(current[1] - end[1]) <= 4) and (abs(current[2] - end[2]) <= 4)):
				#fade(getRandomColor())
				endColor = getRandomColor()
			else:
				#R
				if (current[0] > end[0]):
					current[0] = current[0] - random.randint(1, 4)
				elif (current[0] < end[0]):
					current[0] = current[0] + random.randint(1, 4)
				if (abs(current[0] - end[0]) <= 2):
					current[0] = end[0]

				#G
				if (current[1] > end[1]):
					current[1] = current[1] - random.randint(1, 4)
				elif (current[1] < end[1]):
					current[1] = current[1] + random.randint(1, 4)
				if (abs(current[1] - end[1]) <= 2):
					current[1] = end[1]

				#B
				if (current[2] > end[2]):
					current[2] = current[2] - random.randint(1, 4)
				elif (current[2] < end[2]):
					current[2] = current[2] + random.randint(1, 4)
				if (abs(current[2] - end[2]) <= 2):
					current[2] = end[2]
				
				#####################################
				##### XTC Fader!!!!!!!!!! ###########
				#####################################
				#current[0] = random.randint(0, 255)
				#current[1] = random.randint(0, 255)
				#current[2] = random.randint(0, 255)
				#####################################
				#####################################
				
				setColor(getColorString(current))

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
	c = getIntComponents(color)
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

#Returns an array containing RGB values as integers
#Param: Color string (i.e. "FF0000")
def getIntComponents(color):
	R = int(color[0:2], 16)
	G = int(color[2:4], 16)
	B = int(color[4:6], 16)
	return [R, G, B]

#Returns color string (i.e. "FF0000");
#param: array with integer components (R, G, B)
def getColorString(c):
	R = hex(int(c[0]))[2:]
	if (int(c[0]) < 16):
		R = '0'+R

	G = hex(int(c[1]))[2:]
	if (int(c[1]) < 16):
		G = '0'+G
 
	B = hex(int(c[2]))[2:]
	if (int(c[2]) < 16):
		B = '0'+B 
	return R+G+B

endColor = '0000FF'
currentColor = '0000EE'
minSpeed = 10
maxSpeed = 100	#speed in ms
speed = 10
changeSpeedAfter = 5
max = 255
min = 0

def startFade(minS, maxS, mi, ma):
	global min
	min = mi
	global max
	max = ma
	global minSpeed
	minSpeed = minS
	global maxSpeed
	maxSpeed = maxS
	global speed
	speed = random.randint(minSpeed, maxSpeed)
	global currentColor
	currentColor = getColorString(getRandomColor())
	global endColor
	endColor = getColorString(getRandomColor())
	
	fade(getIntComponents(endColor))
