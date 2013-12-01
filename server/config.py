#! /usr/bin/env python


#GPIO pins for RGB
RED_PIN_1 = 5
GREEN_PIN_1 = 2
BLUE_PIN_1 = 6

# this value indicates the minimum value of the sum of
# red, green and blue channels can be set to before the LEDs start blinking
MIN_VALUE = 0.00

# this is the minimum value threads wait between their processing intervals
# increase this value to get more cpu time for other programs
# decrease this value, to get smoother fading
# don't set this value lower or equal 0!!!
DELAY = 0.01



#server port
SERVER_PORT = 4321