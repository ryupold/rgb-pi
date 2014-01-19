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
    def __init__(self, redFloat_Or_colorString, greenFloat=None, blueFloat=None, address=None):
        if greenFloat is None or blueFloat is None:
            self.colorString = string.strip(redFloat_Or_colorString)

            self.R = 0.0
            self.G = 0.0
            self.B = 0.0
            self.Address = 0



            if self.colorString[0] != '{' or self.colorString[len(self.colorString)-1] != '}':
                raise ValueError('color must defined within {} brackets' + self.colorString)

            colorString = self.colorString[1:len(self.colorString)-1]
            colorParts = string.split(colorString, ':')

            if not (colorParts[0] in ['x', 'b', 'f']):
                raise ValueError('unknown color type: '+colorParts[0])

            #extracting RGB
            if colorParts[0] == 'x':
                rgbcomps = utils.getIntComponents(colorParts[1])
                self.R = rgbcomps[0] / 255.0
                self.G = rgbcomps[1] / 255.0
                self.B = rgbcomps[2] / 255.0

            if colorParts[0] == 'b':
                rgbcomps = string.split(colorParts[1], ',')
                self.R = int(rgbcomps[0]) / 255.0
                self.G = int(rgbcomps[1]) / 255.0
                self.B = int(rgbcomps[2]) / 255.0

            if colorParts[0] == 'f':
                rgbcomps = string.split(colorParts[1], ',')
                self.R = float(rgbcomps[0])
                self.G = float(rgbcomps[1])
                self.B = float(rgbcomps[2])

            #extracting Address
            if len(colorParts) > 2:
                self.Address = int(colorParts[2], 16)
            elif len(colorParts) <= 2:
                self.Address = 0xF


        else:
            self.R = float(redFloat_Or_colorString)
            self.G = float(greenFloat)
            self.B = float(blueFloat)

            if address is None:
                self.Address = 0xF
            else:
                self.Address = address


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
COLOR = [Color('{x:000000}'),
         Color('{x:000000}'),
         Color('{x:000000}'),
         Color('{x:000000}'),
         Color('{x:000000}'),
         Color('{x:000000}'),
         Color('{x:000000}'),
         Color('{x:000000}')]


# elementary function to change the color of the LED strip
def changeColor(r, g, b, address=0xF):
    global COLOR
    
    cmd = ''

    #iterate over all led stripes and set the given color if the stripe address matches
    #the length auf config.RED_PINS is used to determine the stripe amount (could also be config.BLUE PINS or the green one)
    #TODO: think about a better way to do this :)
    for i in range(0, len(config.RED_PINS)):
        if ((i+1) & address) != 0:
            COLOR[i].R = r
            COLOR[i].G = g
            COLOR[i].B = b

            # if lower than min value turn LEDs off
            if (r + g + b) < config.MIN_VALUE:
                r = 0.0
                g = 0.0
                b = 0.0

            cmdR = "echo " + str(config.RED_PINS[i]) + "=" + str(r) + " > /dev/pi-blaster"
            cmdG = "echo " + str(config.GREEN_PINS[i]) + "=" + str(g) + " > /dev/pi-blaster"
            cmdB = "echo " + str(config.BLUE_PINS[i]) + "=" + str(b) + " > /dev/pi-blaster"
            cmd += cmdR + " & " + cmdG + " & " + cmdB + " & "

    os.system(cmd)

def setColor(color):
    changeColor(color.R, color.G, color.B)
