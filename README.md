<html>
	<head><title></title></head>
	<body>
		<h1>rgb-pi</h1>
		<p >Controlling RGB LED Stripes using a Raspberry Pi and a mobile Device</p>
		<p>This project was build on the work of sarfata and his project <a href="https://github.com/sarfata/pi-blaster">pi-blaster</a></p>
		<p>This project provides a server, written in in python. It can be connected by a simple TCP stream socket and controlled by command strings. (protocoll in development)</p>
		<p>To control the whole thing there are mobile apps planned for various platforms:</p>
		<ul>
			<li>Windows Phone</li>
			<li>Android</li>
			<li>...</li>
		</ul>
		<h2>hardware parts needed:</h2>
			<ul>
				<li>Raspberry Pi</li>
				<li>3 x TIP120 power transistors for each LED strip (in case you wanna controll them seperatly)</li>
				<li>RGB LED strip</li>
				<li>Perfboard/Breadboard or Dupont cables</li>
				<li>12V power supply</li>
			</ul>
		<p style="font-size: 1em;">sources & helpful links:</p>
		<ul>
			<li><a href="http://mitchtech.net/raspberry-pi-pwm-rgb-led-strip/">michael@mitchtech.net-Assembly</a></li>
			<li><a href="http://www.tbideas.com/blog/2013/02/controling-a-high-power-rgb-led-with-a-raspberry-pi/">thomas@tbideas.com-PWM</a></li>
		</ul>
		<h2>rgb-pi server</h2>
		<h3>configure</h3>
		<p>first you have to set the pin numbers according to the pins you connected the rgb-channels of your LEDs. This have to be done in the <strong>config.py</strong> file:</p>
		<p>rgb representing pins on the raspberry pi GPIO interface. See: <a href="https://github.com/sarfata/pi-blaster">https://github.com/sarfata/pi-blaster</a></p>
		<pre><code> 
RED_PIN_1 = 2 
GREEN_PIN_1 = 5 
BLUE_PIN_1 = 6</code></pre>
<p>
this value indicates the minimum value of the sum of
red, green and blue channels can be set to before the LEDs start blinking
</p>
<pre><code>MIN_VALUE = 0.05</code></pre>
<p>
# this is the minimum value threads wait between their processing intervals
# increase this value to get more cpu time for other programs
# decrease this value, to get smoother fading
# don't set this value lower or equal 0!!!
</p>
<pre><code>DELAY = 0.01</code></pre>
<p>TCP Port the server is listening on</p>
<pre><code>SERVER_PORT = 4321</code></pre>
<h3>use</h3>
<p>simply changing color<p>
<pre><code>python rgb.py c 1.0 0.2 0.4</code></pre>
<p>starting the server<p>
<pre><code>python rgb.py server</code></pre>
<h4>communication protocol</h4>
<p>The server can receive commands from third party applications, like mobile apps. To send a commands to the server, a TCP stream socket has to be initialized and connected to the raspberry pi host ip. The command has to be a string with a maximum size of 1024 bytes.</p>
<p>By default the server listens to <strong>port 4321</strong>, but this can be configured in <strong>config.py</strong>.</p>
<p>Following commands are implemented in the current version (command arguments are seperated by a space):</p>
<p>Some commands need a color as parameter this must be provided in the following format:</p>
<p>color string format <strong>{x|b|f:string}</strong><br/>
example1 hex-string:	<strong>{x:FF00A1}</strong><br/>
example2 byte:		<strong>{b:255,0,161}</strong><br/>
example3 float:	<strong>{f:1,0,0.63}</strong></p>
<ul>
<li><strong>cc</strong> - set a specific color (red, green and blue are float values from 0.0 to 1.0):
<pre><code>cc color</code></pre>
example (violet): <pre><code>cc {f:0.5,0,1}</code></pre></li>
<li><strong>rf</strong> - randomized fader (all values are integer | speed values must be bigger than 0 | brightness has to be between 0 and 255):
<pre><code>rf minSpeed maxSpeed minBrightness maxBrightness</code></pre>
example: <pre><code>rf 50 150 10 200</code></pre></li>
<li><strong>fade</strong> - fades the current color, over a certain time (time is given in seconds as an integer) to the endColor:
<pre><code>fade timeInSeconds endColor [startColor]</code></pre>
example smooth turn off: <pre><code>fade 2 {x:000000}</code></pre>
example fade red to green: <pre><code>fade 2 {b:255,0,0} {b:0,255,0}</code></pre></li>
</ul>
<p>There is no acknowledgement for sent commands in the current communication protocol, but planned for the future.</p>
</body>
</html> 
