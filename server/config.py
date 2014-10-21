#!/usr/bin/env python

#GPIO pins for RGB
#Pin mapping: pi-blaster -> GPIO-interface on the Raspberry Pi
#   Pin 0 -> 4
#	Pin 1 -> 17
#	Pin 2 -> 18
#	Pin 3 -> 21
#	Pin 4 -> 22
#	Pin 5 -> 23
#	Pin 6 -> 24
#	Pin 7 -> 25
#
#this is a 2D-array.
# First level represents the index of the LED-stripe
#Seconds level contains the GPIO-pin addresses of [RED, GREEN, BLUE] of the corresponding stripe (always in this order)
#If a LED-Stripe supports only 1 or 2 colors the other pins are set to a negative value, to be ignored by the server
#e.g.: [[-1, -1, 3]] <- means a single-color blue led-stripe is connected to GPIO-Pin 3
LED_PINS = [[5, 2, 6]]


# this value indicates the minimum value of the sum of
# red, green and blue channels can be set to before the LEDs start blinking
MIN_VALUE = 0.008

# this is the minimum value threads wait between their processing intervals
# increase this value to get more cpu time for other tests
# decrease this value, to get smoother fading
# don't set this value lower or equal 0!!!
DELAY = 0.01


#server port
SERVER_PORT = 5000

#connection timeout for sending and receiving
#set to 0.0 for non-blocking mode
CONNECTION_TIMEOUT = 1.0


#Data for XBMC remote control
ENABLE_XBMC_REMOTE = 0
XBMC_HOST = "localhost"
XBMC_PORT = 80
