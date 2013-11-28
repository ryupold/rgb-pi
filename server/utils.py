import led


# clips the value between 0 and 1
def clip(value):
    if value < 0.0:
        return 0.0
    elif value > 1.0:
        return 1.0
    else:
        return value

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
    if int(c[0]) < 16:
        R = '0' + R

    G = hex(int(c[1]))[2:]
    if int(c[1]) < 16:
        G = '0' + G

    B = hex(int(c[2]))[2:]
    if int(c[2]) < 16:
        B = '0' + B
    return R + G + B


def interpolateColor(startColor, endColor, percent, resultColor=None):
    if resultColor is None:
        resultColor = led.Color(0, 0, 0)

    resultColor.R = startColor.R + (endColor.R - startColor.R) * percent
    resultColor.G = startColor.G + (endColor.G - startColor.G) * percent
    resultColor.B = startColor.B + (endColor.B - startColor.B) * percent

    return resultColor

def interpolateFloat(start, end, percent):
    return start + (end - start) * percent

