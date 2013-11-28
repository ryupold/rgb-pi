#! /usr/bin/env python

#system modules
import random
import time
import math
import utils
import sys
import time

#rgb-pi modules
import corefunctions
import led
import config

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
    led.changeColor(R, G, B)

#Returns Array with integer RGB components
def getRandomColor():
    global max
    global min
    R = random.randint(min, max)
    G = random.randint(min, max)
    B = random.randint(min, max)

    return [R, G, B]


def stopPulse():
    global RUN
    RUN = RUN + 1
    corefunctions.stopFade()


def startPulse(timeInSecs, startColor, endColor=None):
    global RUN
    myrun = RUN

    if endColor is None:
        endColor = led.Color(0, 0, 0)

    while myrun == RUN:
        corefunctions.fade(timeInSecs, endColor, startColor)
        if myrun == RUN:
            corefunctions.fade(timeInSecs, startColor, endColor)




