# -*- coding: utf-8 -*-
import os
import time
import RPi.GPIO as GPIO

#rgb-pi modules
import datatypes
import config
import log
import server
import utils
import mock

GPIOMapping_BCM = [4, 17, 18, 21, 22, 23, 24, 25]
PWM = [None, None, None, None, None, None, None, None]

#RPi.GPIO initialization
GPIO.setmode(GPIO.BCM)
for i in range(0, len(GPIOMapping_BCM)):
    GPIO.setup(GPIOMapping_BCM[i], GPIO.OUT)
    PWM[i] = GPIO.PWM(GPIOMapping_BCM[i], 100)
    PWM[i].start(0)

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
    global PWM
    global GPIOMapping_BCM

    for i in range(0, len(config.LED_PINS)):
        if ((i+1) & address) != 0:
            COLOR[i].R = r
            COLOR[i].G = g
            COLOR[i].B = b

            # if lower than min value turn LEDs off
            r = 0.0 if r<=0 else utils.clip(r, config.MIN_VALUE)
            g = 0.0 if g<=0 else utils.clip(g, config.MIN_VALUE)
            b = 0.0 if b<=0 else utils.clip(b, config.MIN_VALUE)

            setDutyCycle(PWM[config.LED_PINS[i][0]], r)
            setDutyCycle(PWM[config.LED_PINS[i][1]], g)
            setDutyCycle(PWM[config.LED_PINS[i][2]], b)

#RPi.GPIO works with values between 0-100
def setDutyCycle(pwmPin, value):
    if value < config.MIN_VALUE:
        pwmPin.ChangeDutyCycle(0)
        print "off"
    else:
        pwmPin.ChangeDutyCycle(value*100.0)

def setPin(pin, value):
    global PWM
    PWM[pin].ChangeDutyCycle(utils.clip(value)*100)

def setColor(color):
    for i in range(0, len(server.CurrentFilters)):
        color = server.CurrentFilters[i].onChangeColor(color)
    changeColor(color.R, color.G, color.B)
    
def cleanup():
    global PWM
    for pwm in PWM:
        if pwm is not None:
            pwm.stop()