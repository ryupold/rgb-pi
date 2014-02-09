#system modules
import time
import sys
import copy
import random

#rgb-pi modules
import led
import utils
import config
import xbmcremote

RUN = 0

# fades the start color to the end color over time in seconds
# if start color is not given, current color is used as start
def fade(timeInSecs, endColor, startColor=None):
    if timeInSecs <= 0:
        raise ValueError("time cannot be 0 or below: "+str(timeInSecs))

    global RUN
    myrun = RUN
    fadeXBMCVolume = 0
    startVolume = 0
    ##timeInSecs = 20
    if config.ENABLE_XBMC_REMOTE and endColor.R == 0 and endColor.G == 0 and endColor.B == 0:
        fadeXBMCVolume = 1
        startVolume = xbmcremote.getVolume()
        print startVolume		

    if startColor is None:
        startColor = led.Color(led.COLOR[0].R, led.COLOR[0].G, led.COLOR[0].B)

    currentColor = led.Color(startColor.R, startColor.G, startColor.B)

    startTime = time.time()

    secondsPassed = 0.0
    lastVolume = startVolume

    while ((myrun == RUN) and secondsPassed <= timeInSecs):

        secondsPassed = time.time() - startTime
        #interpolate new color
        utils.interpolateColor(startColor, endColor, secondsPassed/timeInSecs, currentColor)
        
        if fadeXBMCVolume:
            #interpolate new volume
            newVolume = int(startVolume - startVolume * (secondsPassed/timeInSecs))
            if newVolume > 0 and newVolume < lastVolume:
                #print newVolume
                lastVolume = newVolume
                xbmcremote.setVolume(newVolume)
            elif newVolume <= 0:
                print "pause"
                xbmcremote.stop()
        time.sleep(config.DELAY)
        #print startColor," ", endColor, "     ", secondsPassed/timeInSecs
        led.setColor(currentColor)

def fadeToRandom(timeInSecs, startColor=None, minBrightness=None, maxBrightness=None):
    if minBrightness is None:
        minBrightness = 0.0

    if maxBrightness is None:
        maxBrightness = 1.0

    rndColor = led.Color(utils.randfloat(minBrightness,maxBrightness), utils.randfloat(minBrightness,maxBrightness), utils.randfloat(minBrightness,maxBrightness))
    fade(timeInSecs, rndColor, startColor)

def startRandomFade(minTimeBetweenFades, maxTimeBetweenFades, minBrightness=None, maxBrightness=None):
    global RUN
    myrun = RUN

    if minBrightness is None:
        minBrightness = 0.0

    if maxBrightness is None:
        maxBrightness = 1.0

    minB = min(minBrightness, maxBrightness)
    maxB = max(minBrightness, maxBrightness)
    minBrightness = minB
    maxBrightness = maxB

    while myrun == RUN:
        timeInSecs = random.randint(int(minTimeBetweenFades*1000), int(maxTimeBetweenFades*1000))/1000.0
        fadeToRandom(timeInSecs, None, minBrightness, maxBrightness)



def stopFade():
    global RUN
    RUN = RUN + 1
