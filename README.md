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
		<h3>configuring</h3>
		<p>first you have to set the pin numbers according to the pins you connected the rgb-channels of your LEDs</p>
		<pre><code># file: rgb.py
		# rgb representing pins on the raspberry pi GPIO interface
		# see: https://github.com/sarfata/pi-blaster
		RED_PIN_1 = 2
		GREEN_PIN_1 = 5
		BLUE_PIN_1 = 6</code></pre>
		<p>simply changing color<p>
		<pre><code>./rgb.py c 1.0 0.2 0.4</code></pre>
		<p>starting the server<p>
		<pre><code>./rgb.py server</code></pre>
	</body>
</html> 
