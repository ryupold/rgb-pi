#python modules
import httplib
import json

#rgb-pi modules
import config

#########################
##  USAGE
#
# showNotification(title, message)		displays a notification
# next()					plays the next item in playlist
# previous()					plays the previous item in playlist
# playPause()
# setVolume(volume)				set players volume
# volumeUp()					volume up by 5
# volumeDown() 					volume down by 5





#Send command
def sendCommand(request):
	httpServ = httplib.HTTPConnection(config.XBMC_HOST, config.XBMC_PORT)
	httpServ.connect()

	httpServ.request('GET', '/jsonrpc?request='+request)

	response = httpServ.getresponse()

	if response.status == httplib.OK:
		return response.read()




############################
############################
##### COMMANDS

#Shows a notification
def showNotification(title, message):
	request = sendCommand('{"jsonrpc":"2.0","method":"GUI.ShowNotification",%20"params":{"title":"'+title+'",%20"message":"'+message+'"},"id":1}')

#get Active Players
def getActivePlayer():
	request = sendCommand('{"jsonrpc":"2.0","method":"Player.GetActivePlayers","id":1}')
	decoded = json.loads(request)
	return decoded["result"][0]["playerid"]

#Play/Pause
def playPause():
	activePlayer = str(getActivePlayer())
	request = sendCommand('{"jsonrpc":"2.0","method":"Player.PlayPause","params":{"playerid":'+activePlayer+'},"id":1}')
	decoded = json.loads(request)
	return decoded["result"]["speed"]

#Stop
def stop():
	activePlayer = str(getActivePlayer())
	request = sendCommand('{"jsonrpc":"2.0","method":"Player.Stop",%20"params":{"playerid":'+activePlayer+'},"id":1}')

#Next
def next():
	activePlayer = str(getActivePlayer())
	request = sendCommand('{"jsonrpc":"2.0","method":"Player.GoTo","params":{"playerid":'+activePlayer+',"to":"next"},"id":1}')
	
#Previous
def previous():
	activePlayer = str(getActivePlayer())
	request = sendCommand('{"jsonrpc":"2.0","method":"Player.GoTo","params":{"playerid":'+activePlayer+',"to":"previous"},"id":1}')

#set Volume
def setVolume(vol):
	request = sendCommand('{"jsonrpc":"2.0","method":"Application.SetVolume","params":%20{"volume":'+str(vol)+'},"id":1}')
	decoded = json.loads(request)

#get Volume
def getVolume():
	request = sendCommand('{%22jsonrpc%22:%222.0%22,%22method%22:%22Application.GetProperties%22,%22params%22:{%22properties%22:[%22volume%22]},%22id%22:%201}')
	decoded = json.loads(request)
	return decoded["result"]["volume"]

#volume Up
def volumeUp():
	volume = int(getVolume()) + 5
	setVolume(min(volume, 100))

#volume Down
def volumeDown():
	volume = int(getVolume()) - 5
	setVolume(max(volume, 0))
