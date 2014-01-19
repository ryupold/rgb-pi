//RGB-PI Functions
function shutDown() {
	sendCommand('fade 2 {x:000000}');
}
function rf() {
	var speed_min = document.getElementById("rf_speed_min").value;
	var speed_max = document.getElementById("rf_speed_max").value;
	var value_min = parseInt(document.getElementById("rf_value_min").value) / 255;
	var value_max = parseInt(document.getElementById("rf_value_max").value) / 255;
	sendCommand('rf '+speed_min+' '+speed_max+' '+value_min+' '+value_max);
}

function pulse() {
	var timeInSeconds = document.getElementById('pulseSpeed').value;
	sendCommand('pulse '+timeInSeconds+' '+hex2rgbpihex(getColorOne())+' '+hex2rgbpihex(getColorTwo()));
}
function c() {
	sendCommand("cc  {x:8B5A2B}");
}


//Send command to php-api
function sendCommand(cmd) {
	var xmlhttp;
	if (window.XMLHttpRequest)
	  {// code for IE7+, Firefox, Chrome, Opera, Safari
	  xmlhttp=new XMLHttpRequest();
	  }
	else
	  {// code for IE6, IE5
	  xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
	  }
	xmlhttp.open("GET","sendCommand.php?cmd="+cmd,true);
	xmlhttp.send();
}


//Getter and Setter for choosing color one / two
var selectedColor;
function selectColorOne() {
	selectedColor = 1;
	document.getElementById("colorOne").style.borderColor = "#00FF33";
	document.getElementById("colorOne").style.borderWidth = "2px";
	
	document.getElementById("colorTwo").style.borderColor = "#000000";
	document.getElementById("colorTwo").style.borderWidth = "2px";
}
function selectColorTwo() {
	selectedColor = 2;
	document.getElementById("colorTwo").style.borderColor = "#00FF33";
	document.getElementById("colorTwo").style.borderWidth = "2px";
	
	document.getElementById("colorOne").style.borderColor = "#000000";
	document.getElementById("colorOne").style.borderWidth = "2px";
}
function getSelectedColor() {
	return selectedColor;
}
function getColorOne() {
	return document.getElementById("colorOneHidden").value;
}
function getColorTwo() {
	return document.getElementById("colorTwoHidden").value;
}
function setColorOne(hex) {
	document.getElementById("colorOne").style.backgroundColor = hex;
	document.getElementById("colorOneHidden").value = hex;
	document.getElementById("colorOneHeader").innerHTML = "COLOR ONE ("+hex+")";
}
function setColorTwo(hex) {
	document.getElementById("colorTwo").style.backgroundColor = hex;
	document.getElementById("colorTwoHidden").value = hex;
	document.getElementById("colorTwoHeader").innerHTML = "COLOR TWO ("+hex+")";
}

//Helper methods
function hex2rgbpihex(hex) {
	return "{x:"+hex.substr(1, 6)+"}";
}