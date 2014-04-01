#python modules
import os

#rgb-pi modules
import datatypes
import config
import log
import constants

#global rgb values
COLOR = [datatypes.Color('{x:000000}'),
         datatypes.Color('{x:000000}'),
         datatypes.Color('{x:000000}'),
         datatypes.Color('{x:000000}'),
         datatypes.Color('{x:000000}'),
         datatypes.Color('{x:000000}'),
         datatypes.Color('{x:000000}'),
         datatypes.Color('{x:000000}')]


# elementary function to change the color of LED stripes
def changeColor(r, g, b, address=0xF):
    global COLOR

    cmd = ''

    #iterate over all led stripes and set the given color if the stripe address matches
    #the length auf config.RED_PINS is used to determine the stripe amount (could also be config.BLUE PINS or the green one)
    #TODO: think about a better way to do this :)
    for i in range(0, len(config.LED_PINS)):
        if ((i+1) & address) != 0:
            COLOR[i].R = r
            COLOR[i].G = g
            COLOR[i].B = b

            # if lower than min value turn LEDs off
            if (r + g + b) < config.MIN_VALUE:
                r = 0.0
                g = 0.0
                b = 0.0

            cmdR = "echo " + str(config.LED_PINS[i][0]) + "=" + str(r) + " > "+constants.FIFO
            cmdG = "echo " + str(config.LED_PINS[i][1]) + "=" + str(g) + " > "+constants.FIFO
            cmdB = "echo " + str(config.LED_PINS[i][2]) + "=" + str(b) + " > "+constants.FIFO
            cmd += cmdR + " & " + cmdG + " & " + cmdB + " & "
            if log.m(log.LEVEL_CHANGE_COLOR): log.l('changing color to '+str(COLOR[i]))

    os.system(cmd)

def setColor(color):
    changeColor(color.R, color.G, color.B)
