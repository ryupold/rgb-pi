#python modules
import time
import os
import sys
import string
import math

#rgb-pi modules
import utils
import config



#color string format {x|b|f:string}
#example1 hex-string:	{x:FF00A1}
#example2 byte:			{b:255,0,161}
#example3 float:		{f:1,0,0.63}
class Color():
    def __init__(self, redFloat_Or_colorString, greenFloat=None, blueFloat=None):

        if greenFloat is None or blueFloat is None:
            self.colorString = string.strip(redFloat_Or_colorString)

            self.R = 0.0
            self.G = 0.0
            self.B = 0.0

            if self.colorString[0] != '{' or self.colorString[len(self.colorString)-1] != '}':
                raise ValueError('color must defined within {} brackets' + self.colorString)

            colorString = self.colorString[1:len(self.colorString)-1]
            colorParts = string.split(colorString, ':')

            if not (colorParts[0] in ['x', 'b', 'f']):
                raise ValueError('unknown color type: '+colorParts[0])

            if colorParts[0] == 'x':
                rgbcomps = utils.getIntComponents(colorParts[1])
                self.R = rgbcomps[0] / 255.0
                self.G = rgbcomps[1] / 255.0
                self.B = rgbcomps[2] / 255.0

            if colorParts[0] == 'b':
                rgbcomps = string.split(colorParts[1], ',')
                self.R = int(rgbcomps[0])
                self.G = int(rgbcomps[1])
                self.B = int(rgbcomps[2])

            if colorParts[0] == 'f':
                rgbcomps = string.split(colorParts[1], ',')
                self.R = float(rgbcomps[0])
                self.G = float(rgbcomps[1])
                self.B = float(rgbcomps[2])
        else:
            self.R = float(redFloat_Or_colorString)
            self.G = float(greenFloat)
            self.B = float(blueFloat)


    def redByte(self):
        return int(self.R * 255)
    def greenByte(self):
        return int(self.G * 255)
    def blueByte(self):
        return int(self.B * 255)

    def getHexString(self):
        return utils.getColorString([self.redByte(), self.greenByte(), self.blueByte()])

    def __str__(self):
        return '{f:'+str(self.R)+','+str(self.G)+','+str(self.B)+'}'

    def __add__(self, other):
        return Color(utils.clip(self.R+other.R), utils.clip(self.G+other.G), utils.clip(self.B+other.B))

    def __sub__(self, other):
        return Color(utils.clip(self.R-other.R), utils.clip(self.G-other.G), utils.clip(self.B-other.B))

    def __mul__(self, other):
        return Color(utils.clip(self.R*other.R), utils.clip(self.G*other.G), utils.clip(self.B*other.B))

    def __div__(self, other):
        return Color(utils.clip(self.R/other.R), utils.clip(self.G/other.G), utils.clip(self.B/other.B))


#global rgb values
COLOR = Color('{x:000000}')




# elementary function to change the color of the LED strip
def changeColor(r, g, b):
    global COLOR
    COLOR.R = r
    COLOR.G = g
    COLOR.B = b

    # if lower than min value turn LEDs off
    if (r + g + b) < config.MIN_VALUE:
        r = 0.0
        g = 0.0
        b = 0.0

    cmdR = "echo " + str(config.RED_PIN_1) + "=" + str(r) + " > /dev/pi-blaster"
    cmdG = "echo " + str(config.GREEN_PIN_1) + "=" + str(g) + " > /dev/pi-blaster"
    cmdB = "echo " + str(config.BLUE_PIN_1) + "=" + str(b) + " > /dev/pi-blaster"
    os.system(cmdR + " & " + cmdG + " & " + cmdB)

def setColor(color):
    changeColor(color.R, color.G, color.B)



