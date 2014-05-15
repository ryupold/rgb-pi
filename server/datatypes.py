#python modules
import string
import time

#rgb-pi modules
import utils
import constants
import led
import datetime
import math


#color string format {x|b|f:string}
#example1 hex-string:	{x:FF00A1}
#example2 byte:			{b:255,0,161}
#example3 float:		{f:1,0,0.63}
class Color(object):
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

            if not (colorParts[0] in ['x', 'b', 'f', 'r']):
                raise ValueError('unknown color type: '+colorParts[0])

            #extracting Address
            if len(colorParts) > 2:
                self.Address = int(colorParts[2], 16)
            elif len(colorParts) <= 2:
                self.Address = 0xF

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

            if colorParts[0] == 'r':
                rndValues = string.split(colorParts[1], ',')

                fromRed = float(string.split(rndValues[0], '-')[0])
                toRed = float(string.split(rndValues[0], '-')[1])
                fromGreen = float(string.split(rndValues[1], '-')[0])
                toGreen = float(string.split(rndValues[1], '-')[1])
                fromBlue = float(string.split(rndValues[2], '-')[0])
                toBlue = float(string.split(rndValues[2], '-')[1])

                self.R = utils.randfloat(fromRed, toRed)
                self.G = utils.randfloat(fromGreen, toGreen)
                self.B = utils.randfloat(fromBlue, toBlue)


            self.R = utils.clip(self.R)
            self.G = utils.clip(self.G)
            self.B = utils.clip(self.B)




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

    def magnitude(self):
        return math.sqrt(self.R*self.R + self.G*self.G + self.B*self.B)

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

    def __eq__(self, other):
        return self.R == other.R and self.G == other.G and self.B == other.B

    def __ne__(self, other):
        return self.R != other.R or self.G != other.G or self.B != other.B



class Time(object):
    def __init__(self, seconds):
        self.timeString = string.strip(str(seconds))
        self.seconds = 0.0


        try:
            self.seconds = float(self.timeString)
        except:
            if self.timeString[0] == '{' and self.timeString[len(self.timeString)-1] == '}':
                timeString = self.timeString[1:len(self.timeString)-1]
                timeParts = string.split(timeString, ':')

                if len(timeParts) != 2:
                    raise ValueError('Time must be in following format "{c|r:string} | float". '+self.timeString+' has an incorrect format')

                if not (timeParts[0] in ['c', 'r']):
                    raise ValueError('unknown time type: '+timeParts[0])

                #extracting time
                if timeParts[0] == 'c':
                    self.seconds = float(timeParts[1])

                if timeParts[0] == 'r':
                    timecomps = string.split(timeParts[1], ',')
                    self.seconds = utils.randfloat(float(timecomps[0]), float(timecomps[1]))
            else:
                raise ValueError('time must defined within {} brackets or be a float value: ' + self.timeString)

    def __str__(self):
        return str(self.seconds)

    def __add__(self, other):
        return Time(max(self.seconds + other.seconds, 0))

    def __sub__(self, other):
        return Time(max(self.seconds - other.seconds, 0))

    def __mul__(self, other):
        return Time(max(self.seconds * other.seconds, 0))

    def __div__(self, other):
        return Time(max(self.seconds / other.seconds, 0))


class Condition(object):
    def __init__(self, condition):
        self.conditionString = string.strip(str(condition))
        self.condition = 0
        self.type = constants.CONDITION_BOOL
        self.time = 0
        self.startTime = None
        self.color = None
        self.iterations = 0
        self.startIterations = 0

        if not self.conditionString.isdigit() and self.conditionString[0] != '{' or self.conditionString[len(self.conditionString)-1] != '}':
            raise ValueError('condition must defined within {} brackets or be a bool value (1 or 0)' + self.conditionString)

        if self.conditionString.isdigit():
            self.type = constants.CONDITION_BOOL
            self.condition = int(self.conditionString) != 0
        else:
            conditionString = self.conditionString[1:len(self.conditionString)-1]
            conditionParts = string.split(conditionString, ':')

            if not (conditionParts[0] in ['t','c', 'i', 'b']):
                raise ValueError('unknown condition type: '+conditionParts[0])

            #extracting condition
            if conditionParts[0] == 't':
                self.type = constants.CONDITION_TIME
                self.time = float(conditionParts[1])
                if self.startTime is None:
                    self.startTime = time.time()

            if conditionParts[0] == 'c':
                self.type = constants.CONDITION_COLOR
                self.color = Color(conditionParts[1])

            if conditionParts[0] == 'i':
                self.type = constants.CONDITION_ITERATE
                self.startIterations = self.iterations = int(conditionParts[1])
                self.condition = self.iterations != 0

            if conditionParts[0] == 'b':
                self.type = constants.CONDITION_BOOL
                self.condition = int(conditionParts[1]) != 0

    def isTrue(self):
        return self.condition != 0

    def isFalse(self):
        return self.condition == 0

    def progress(self):
        if self.type == constants.CONDITION_TIME:
            return utils.clip((time.time()-self.startTime)/self.time)

        if self.type == constants.CONDITION_ITERATE:
            return (self.startIterations-self.iterations)*1.0/self.iterations

        if self.type == constants.CONDITION_COLOR:
            return 0 if led.COLOR[0] != self.color else 1

        if self.type == constants.CONDITION_BOOL:
            return 1.0 if self.condition else 0.0

    def check(self):
        if self.type == constants.CONDITION_TIME:
            if self.startTime is None:
                self.startTime = time.time()
            self.condition = self.startTime+self.time >= time.time()

        if self.type == constants.CONDITION_ITERATE:
            self.condition = self.iterations != 0
            self.iterations = max(self.iterations - 1, 0)
            print 'i='+str(self.iterations)

        if self.type == constants.CONDITION_COLOR:
            self.condition = led.COLOR[0] != self.color

        return self.condition

    def __str__(self):
        return str(self.condition)


class TriggerCondition(object):
    """
    Condition used by Triggers
    """
    def __init__(self, condition):
        self.conditionString = string.strip(str(condition))
        self.condition = 0
        self.type = constants.TRIGGER_TIME
        self.time = None
        self.lastTime = None
        self.color = None

        if self.conditionString[0] != '{' or self.conditionString[len(self.conditionString)-1] != '}':
            raise ValueError('condition must defined within {} brackets ' + self.conditionString)


        conditionString = self.conditionString[1:len(self.conditionString)-1]
        conditionParts = string.split(conditionString, ':')

        if not (conditionParts[0] in ['t','c']):
            raise ValueError('unknown condition type: '+conditionParts[0])

        #extracting condition
        if conditionParts[0] == 't':
            self.type = constants.TRIGGER_TYPE_TIME
            hms = string.split(conditionParts[1], ",")
            self.time = datetime.time(hms[0], hms[1], hms[2])

            if self.lastTime is None:
                self.lastTime = datetime.datetime.utcnow()

        if conditionParts[0] == 'c':
            self.type = constants.TRIGGER_TYPE_COLOR
            self.color = Color(conditionParts[1])

    def check(self):
        if self.type == constants.TRIGGER_TYPE_TIME:
            currentDateTime = datetime.datetime.combine(datetime.date.today(), self.time)
            if currentDateTime < datetime.datetime.utcnow() and currentDateTime > self.lastTime:
                self.condition = 1
            else:
                self.condition = 0
            self.lastTime = datetime.datetime.utcnow()

        if self.type == constants.TRIGGER_TYPE_COLOR:
            if (led.COLOR[0] - self.color).magnitude() < 0.01:
                self.condition = 1
            else:
                self.condition = 0

    def isTrue(self):
        return self.condition != 0

    def isFalse(self):
        return self.condition == 0

    def __str__(self):
        return str(self.condition)