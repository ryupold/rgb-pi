#system modules
import time
import sys
import copy

#rgb-pi modules
import led
import utils
import config

RUN = 0


def fade(timeInSecs, endColor, startColor=None):
    global RUN
    myrun = RUN

    if startColor is None:
        startColor = led.Color(led.COLOR.R, led.COLOR.G, led.COLOR.B)


    currentColor = led.Color(startColor.R, startColor.G, startColor.B)

    startTime = time.time()

    secondsPassed = 0.0

    while ((myrun == RUN) and secondsPassed <= timeInSecs):

        secondsPassed = time.time() - startTime

        #interpolate new color
        utils.interpolateColor(startColor, endColor, secondsPassed/timeInSecs, currentColor)
        time.sleep(config.DELAY)
        led.setColor(currentColor)


def stopFade():
    global RUN
    RUN = RUN + 1
