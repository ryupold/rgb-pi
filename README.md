# RGB-pi
**Controlling RGB LED stripes using a Raspberry Pi**
	
This project provides a server, written in in python. It can be connected by a simple TCP stream socket and controlled by command strings. We use the [pigpio library](http://abyz.co.uk/rpi/pigpio) to control the GPIO outputs.

## hardware parts needed:
  * Raspberry Pi
  * 3 x TIP120 power transistors for each LED strip (in case you wanna control them separately)
  * RGB LED strip
  * Perfboard/Breadboard or Dupont cables
  * 12V power supply (_Watt amount needed depends on the used LED-stripe and its length_)
	
**sources & helpful links:**
  * [michael at mitchtech.net - Assembly](http://mitchtech.net/raspberry-pi-pwm-rgb-led-strip)
  * [thomas at tbideas.com - PWM](http://www.tbideas.com/blog/2013/02/controling-a-high-power-rgb-led-with-a-raspberry-pi)
  * [The pigpio Library - pigpio](http://abyz.co.uk/rpi/pigpio)

## rgb-pi server
### configure

Before you can start using RGB-Pi you have to set it up.
You can do this easily by running this command:
configuration of the server:
```bash
sudo python configure.py config
```

First thing to do is installing pigpio by calling number 1 in the configuration script:
configuration of the server:
```bash
1: install/uninstall pigpio
```

After installing pi-blaster you have to set the pin numbers according to the pins you connected the rgb-channels of your LEDs.
This is done by the 2nd option of the configuration script:
```bash
2: configure LED-channels
```

The next steps are optional.
You can change the server runtime constants with the 3rd number of the configuration script:
```bash
3: configure server
```

Setup RGB-Pi as service. So it starts on boot:
```bash
5: enable/disable autostart (root)
```

#### server values
##### min-value
This value indicates the minimum value of the sum of red, green and blue channels.
If a color is set with **R + G + B < MIN_VALUE**, rgb-pi will set black (off) as color to prevent the LEDs from blinking.
			
```python
MIN_VALUE = 0.00
```

##### delay
This is the minimum value threads wait between their processing intervals
increase this value to get more cpu time for other programs
decrease this value, to get smoother fading.
Do not set this value lower or equal 0!!!
```python
DELAY = 0.01
```

##### server port
TCP port the server is listening on: 
```python
SERVER_PORT = 4321
```

##### connection timeout
The maximum time waited till a sending or receiving socket operation is aborted (in seconds).
The value 0.0 enables the non-blocking mode for the connections.
Default value: 1.0
```python
CONNECTION_TIMEOUT = 1.0
```

#### XBMC control
RGB-Pi is also able to control a local or remote XBMC-service.
In order to make this available you have to set the IP of the service (127.0.0.1 or localhost your Raspberry Pi itself is running XBMC)
and the port the service is listening on:
```bash
1: ENABLE_XBMC_REMOTE
2: XBMC_HOST
3: XBMC_PORT
```


### use
simply changing color:
```bash
python rgb.py c 1.0 0.2 0.4
```

starting the server:
```bash
python rgb.py server
```

#### communication protocol
A documentation to the communication protocol can be found here (http://htmlpreview.github.io/?https://github.com/ryupold/rgb-pi/blob/master/doc/protocol.html)

The server can receive commands from third party applications, like mobile apps. To send commands to the server, a TCP stream socket has to be initialized and connected to the raspberry pi host ip. The command has to be a unicode string.

By default the server listens to <strong>port 4321</strong>, but this can be configured with **python configutre.py config**.


## Contributors
BenjaminDieter (https://github.com/BenjaminDieter)  
ryupold (https://github.com/ryupold)

## License
```
The MIT License (MIT)

Copyright (c) 2013 Creative RyU

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
```
