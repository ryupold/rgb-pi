
import utils
import time
import math
import rgbfunctions
import sys
import timedDimmer
import rgbthreads


def stop():
	global RUN
	RUN = RUN + 1
	timedDimmer.stopDim()

def startJamaica(command):
	stepSeconds = int(command[2])
	global RUN
	myrun = RUN
	while myrun == RUN:
		
		#timedDimmer.fadeCurrentColor(stepSeconds, '333300')
		timedDimmer.fadeCurrentColor(stepSeconds, '006600')
		timedDimmer.fadeCurrentColor(stepSeconds, '666600')
		timedDimmer.fadeCurrentColor(stepSeconds, '660000')
		
		
		