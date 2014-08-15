#python modules
import os
import time

#rgb-pi modules
import datatypes
import config
import log
import constants
import server


GPIOMapping_BCM = [4, 17, 18, 21, 22, 23, 24, 25]
PWMs = {}
if config.USE_PI_BLASTER == 0:
    try:
        import RPi.GPIO as GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        for pin in GPIOMapping_BCM:
            print("setting up BCM Pin: "+str(pin))
            GPIO.setup(pin, GPIO.OUT, GPIO.LOW)
            p = GPIO.PWM(pin, 100)
            p.start(0)
            p.ChangeDutyCycle(0)
            PWMs[pin] = p
            #p.stop()
        time.sleep(2)
    except RuntimeError:
        print("Error importing RPi.GPIO!  This is probably because you need superuser privileges. ")



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

    if config.USE_PI_BLASTER:
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
    else:
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
                PWMs[GPIOMapping_BCM[config.LED_PINS[i][0]]].ChangeDutyCycle((int)(r*100))
                PWMs[GPIOMapping_BCM[config.LED_PINS[i][1]]].ChangeDutyCycle((int)(g*100))
                PWMs[GPIOMapping_BCM[config.LED_PINS[i][2]]].ChangeDutyCycle((int)(b*100))

def setColor(color):
    for i in range(0, len(server.CurrentFilters)):
        color = server.CurrentFilters[i].onChangeColor(color)
    changeColor(color.R, color.G, color.B)