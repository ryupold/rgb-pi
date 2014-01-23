#! /usr/bin/env python


#GPIO pins for RGB
LED_PINS = [[5, 2, 6]]


# this value indicates the minimum value of the sum of
# red, green and blue channels can be set to before the LEDs start blinking
MIN_VALUE = 0.08

# this is the minimum value threads wait between their processing intervals
# increase this value to get more cpu time for other programs
# decrease this value, to get smoother fading
# don't set this value lower or equal 0!!!
DELAY = 0.01


#server port
SERVER_PORT = 4321


#Data for XBMC remote control
ENABLE_XBMC_REMOTE = 0
XBMC_HOST = "127.0.0.1"
XBMC_PORT = 80

BLUE_PINS = [6
GREEN_PINS = [2
RED_PINS = [5]