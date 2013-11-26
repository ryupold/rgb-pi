#system modules
import time
import sys

#rgb-pi modules
import led
import utils

RUN = 0


def fade(timeInSecs, endColor, startColor=None):
    global RUN
    myrun = RUN


    if startColor is None:
        startColor = led.COLOR


    currentColor = utils.getIntComponents(startColor)

    #Now, in seconds
    startTime = int(time.time())


    #time, when lights should go out
    endTime = startTime + timeInSecs

    #startColor as Array
    startColorArray = utils.getIntComponents(startColor)
    R = startColorArray[0] / 255.0
    G = startColorArray[1] / 255.0
    B = startColorArray[2] / 255.0
    led.changeColor(R, G, B)

    #endColor is a defaultValue
    if endColor is None:
        endColor = '000000'
    endColorArray = utils.getIntComponents(endColor)


    #time between two steps for R
    secondsBetweenRChange = (sys.maxint if startColorArray[0] == 0 else timeInSecs / float(startColorArray[0]))

    #time between two steps for G
    secondsBetweenGChange = (sys.maxint if startColorArray[1] == 0 else timeInSecs / float(startColorArray[1]))

    #time between two steps for B
    secondsBetweenBChange = (sys.maxint if startColorArray[2] == 0 else timeInSecs / float(startColorArray[2]))

    #time between to steps
    secondsBetweenChange = min(min(secondsBetweenRChange, secondsBetweenGChange), secondsBetweenBChange)

    secondsPassed = 0

    while ((myrun == RUN) and secondsPassed < timeInSecs):
        now = time.time()
        secondsPassed = now - startTime

        #interpolate new color
        currentColor[0] = max(0, utils.interpolateColor(startColorArray[0], endColorArray[0],
                                                        1.0 * secondsPassed / (timeInSecs)))
        currentColor[1] = max(0, utils.interpolateColor(startColorArray[1], endColorArray[1],
                                                        1.0 * secondsPassed / (timeInSecs)))
        currentColor[2] = max(0, utils.interpolateColor(startColorArray[2], endColorArray[2],
                                                        1.0 * secondsPassed / (timeInSecs)))
        R = currentColor[0] / 255.0
        G = currentColor[1] / 255.0
        B = currentColor[2] / 255.0

        led.changeColor(R, G, B)

        #next step
        time.sleep(secondsBetweenChange)


def stopFade():
    global RUN
    RUN = RUN + 1