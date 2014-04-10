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
import constants
import datatypes
import server

# fades the start color to the end color over time in seconds
# if start color is not given, current color is used as start
#(cmdThread can be set to None if no thread is responsible for this fade call)
def fade(task, timeInSecs, endColor, startColor=None):

    if task is not None and task.state != constants.CMD_STATE_STARTED:
        raise RuntimeError("the thread, which is responsible for this fade has an invalid state: "+str(task.state))
    if timeInSecs <= 0:
        raise ValueError("time cannot be 0 or below: "+str(timeInSecs))

    startVolume = 0
    ##timeInSecs = 20
    if config.ENABLE_XBMC_REMOTE:
        startVolume = xbmcremote.getVolume()

    if startColor is None:
        startColor = datatypes.Color(led.COLOR[0].R, led.COLOR[0].G, led.COLOR[0].B)

    currentColor = datatypes.Color(startColor.R, startColor.G, startColor.B)

    startTime = time.time()

    secondsPassed = 0.0
    lastVolume = startVolume

    while ((task is not None and (task.state == constants.CMD_STATE_STARTED and (task.thread is None or task.thread.state == constants.CMD_STATE_STARTED))) and secondsPassed <= timeInSecs):

        secondsPassed = time.time() - startTime
        #interpolate new color
        utils.interpolateColor(startColor, endColor, secondsPassed/timeInSecs, currentColor)
        
        #fade step filters
        for f in server.CurrentFilters:
            f.onFadeStep(timeInSecs, startColor, endColor, secondsPassed/timeInSecs)

        time.sleep(config.DELAY)
        #print startColor," ", endColor, "     ", secondsPassed/timeInSecs
        led.setColor(currentColor)

    #fade end filters
    for f in server.CurrentFilters:
        f.onFadeEnd(timeInSecs, startColor, endColor)

def wait(task, timeInSecs):
    startTime = time.time()
    secondsPassed = 0.0
    while ((task is not None and (task.state == constants.CMD_STATE_STARTED and (task.thread is None or task.thread.state == constants.CMD_STATE_STARTED))) and secondsPassed <= timeInSecs):
        time.sleep(config.DELAY)
        secondsPassed = time.time() - startTime