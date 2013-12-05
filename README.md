# RGB-pi
======
**Controlling RGB LED Stripes using a Raspberry Pi and a mobile Device**

This project was build on the work of Michael Vitousek and his project [pi-blaster](https://github.com/mvitousek/pi-blaster)
	
This project provides a server, written in in python. It can be connected by a simple TCP stream socket and controlled by command strings. (protocoll in development)
	
To control the whole thing there are mobile apps planned for various platforms:
  * Windows Phone
  * Android
  * HTML
  * ...

======

## hardware parts needed:
  * Raspberry Pi
  * 3 x TIP120 power transistors for each LED strip (in case you wanna controll them seperatly)
  * RGB LED strip
  * Perfboard/Breadboard or Dupont cables
  * 12V power supply (_Watt amount needed depends on the used LED-stripe and its lenght_)
	
**sources & helpful links:**
  * [michael at mitchtech.net - Assembly](http://mitchtech.net/raspberry-pi-pwm-rgb-led-strip)
  * [thomas at tbideas.com - PWM](http://www.tbideas.com/blog/2013/02/controling-a-high-power-rgb-led-with-a-raspberry-pi)
	
======

## rgb-pi server
### configure
first you have to set the pin numbers according to the pins you connected the rgb-channels of your LEDs. This have to be done in the **config.py** file:
			
Pins on the raspberry pi GPIO interface. See: (https://github.com/mvitousek/pi-blaster)
Which represents the RGB channels of your LEDs
```python
RED_PIN_1 = 2 
GREEN_PIN_1 = 5 
BLUE_PIN_1 = 6
```

This value indicates the minimum value of the sum of red, green and blue channels.  
If a Color is set with **R + G + B < MIN_VALUE**, rgb-pi will set black (off) as color to prevent the LEDs from blinking.
			
```python
MIN_VALUE = 0.00
```

this is the minimum value threads wait between their processing intervals
increase this value to get more cpu time for other programs
decrease this value, to get smoother fading
don't set this value lower or equal 0!!!
```python
DELAY = 0.01
```

TCP Port the server is listening on: 
```python
SERVER_PORT = 4321
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
The server can receive commands from third party applications, like mobile apps. To send a commands to the server, a TCP stream socket has to be initialized and connected to the raspberry pi host ip. The command has to be a string with a maximum size of 1024 bytes.

By default the server listens to <strong>port 4321</strong>, but this can be configured in **config.py**.

Following commands are implemented in the current version (command arguments are seperated by a space):

Some commands need a color as parameter this must be provided in the following format:
color string format **{x|b|f:string}**
  - example1 hex-string:	**{x:FF00A1}**
  - example2 byte:		**{b:255,0,161}**
  - example3 float:		**{f:1,0,0.63}**

##### commands
* **cc** - set a specific color (red, green and blue are float values from 0.0 to 1.0):  
  `cc color`  
  1. example (violet): `cc {f:0.5,0,1}`

* **rf** - random color fader, fades in a random time between min and max (in seconds, as float) within the optional brightness limits:  
  `rf minSpeed maxSpeed [minBrightness [maxBrightness]]`  
  1. example random fade color between a brightness level of minimum 0.1 and maximum 0.5 within random times between 2 and 60 seconds after each fade: `rf 2 60 0.1 0.5`  
  2. example random fade all color with constant 10 seconds per fade: `rf 10 10`

* **fade** - fades the current color, over a certain time (time is given in seconds as an integer) to the endColor:  
  `fade timeInSeconds endColor [startColor]`  
  1. example smooth turn off: `fade 2 {x:000000}`  
  2. example fade green to red over 5 minutes: `fade 300 {b:255,0,0} {b:0,255,0}`

* **pulse** - fades from start color to end color and vice versa:  
  `pulse timeInSeconds endColor [startColor]`  
  1. example fast blue-black pulse: `pulse 1 {f:0,0,1}`  
  2. example pulse red to green over a minute: `pulse 60 {b:255,0,0} {b:0,255,0}`  


There is no acknowledgement for sent commands in the current communication protocol, but planned for the future.
