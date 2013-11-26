#! /usr/bin/env python

import utils
import time
import math
import rgbfunctions
import sys

######################
#### USER INPUT ######
######################
minutesToDim = 1		#Time to dim, minutes
startColor = 'FF4444'		#Color to start with
######################
#### END U I #########
######################


RUN = 0

#dims/fades the current color to black 000000 over 'secondsToDim'
def dimCurrentColor(secondsToDim):
	startDim(secondsToDim, utils.getColorString([int(rgbfunctions.RED*255), int(rgbfunctions.GREEN*255), int(rgbfunctions.BLUE*255)]))

#dims/fades the current color to the 'endColorHex' over 'secondsToDim'
def fadeCurrentColor(secondsToDim, endColorHex):
	startDim(secondsToDim, utils.getColorString([int(rgbfunctions.RED*255), int(rgbfunctions.GREEN*255), int(rgbfunctions.BLUE*255)]), endColorHex)
	
#dims/fades the 'startColor' over 'secondsToDim' to 'endColor' (default is black 000000)
