
def createInitD(serverPath, pigpioPath):
  return "#! /bin/sh\n\
# /etc/init.d/rgb-pi\n\
#\n\
\n\
case \"$1\" in\n\
  start)\n\
    echo \"Starting pigpio and RGB-Pi...\"\n\
    sudo "+pigpioPath+" \n\
    su - pi -c \"screen -dmS 'rgb-pi'\"\n\
    su - pi -c \"screen -r 'rgb-pi' -X stuff $'cd "+serverPath+"\\n'\"\n\
    su - pi -c \"screen -r 'rgb-pi' -X stuff $'python rgb.py server\\n'\" \n\
    ;;\n\
  stop)\n\
    echo \"Stopping RGB-Pi and pigpio\"\n\
    kill $(ps aux | grep python rgb.py | awk '{ print $2 }') \n\
    killall pigpiod \n\
    screen -S \"rgb-pi\" -X quit \n\
    ;;\n\
  *)\n\
    echo \"Usage: /etc/init.d/rgb-pi {start|stop}\"\n\
    exit 1\n\
    ;;\n\
esac\n\
\n\
exit 0\n"

def writeInitD(serverPath, pigpioPath):
  target = open("/etc/init.d/rgb-pi", 'w')
  target.truncate()
  target.write(createInitD(serverPath, pigpioPath))
  target.close()
