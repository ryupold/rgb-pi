#system modules
import utils
import time
import math
import sys

#rgb-pi modules
import corefunctions
import server


def stop():
    global RUN
    RUN = RUN + 1
    corefunctions.stopFade()


def startJamaica(command):
    pass
    # TODO: with new color format
