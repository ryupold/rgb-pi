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
    if config.ENABLE_XBMC_REMOTE:
        httpServ = httplib.HTTPConnection(config.XBMC_HOST, config.XBMC_PORT)
        httpServ.connect()

        httpServ.request('GET', '/jsonrpc?request=' + request)

        response = httpServ.getresponse()

        if response.status == httplib.OK:
            return response.read()
    else:
        raise EnvironmentError(
                'config.ENABLE_XBMC_REMOTE needs to be enabled in order to send commands to your xbmc-service')


############################
############################
##### COMMANDS

#TODO: remove old commented json-strings if python object format works

#Shows a notification
def showNotification(title, message):
    #request = sendCommand(
    #'{"jsonrpc":"2.0","method":"GUI.ShowNotification",%20"params":{"title":"' + title + '",%20"message":"' + message + '"},"id":1}')
    request = sendCommand( json.dumps({
        "jsonrpc": "2.0",
        "method": "GUI.ShowNotification",
        "params":
            {
                "title": title,
                "message":message,
                "id":1
            }
    }))
    return request


#get Active Players
def getActivePlayer():
    #request = sendCommand('{"jsonrpc":"2.0","method":"Player.GetActivePlayers","id":1}')
    request = sendCommand( json.dumps({
        "jsonrpc": "2.0",
        "method": "Player.GetActivePlayers",
        "id":1
    }))
    decoded = json.loads(request)
    return decoded["result"][0]["playerid"]


#Play/Pause
def playPause():
    activePlayer = str(getActivePlayer())
    #request = sendCommand(
    #    '{"jsonrpc":"2.0","method":"Player.PlayPause","params":{"playerid":' + activePlayer + '},"id":1}')
    request = sendCommand( json.dumps({
        "jsonrpc": "2.0",
        "method": "Player.GetActivePlayers",
        "id":1
    }))
    decoded = json.loads(request)
    return decoded["result"]["speed"]

#Stop
def stop():
    activePlayer = str(getActivePlayer())
    #request = sendCommand(
    #    '{"jsonrpc":"2.0","method":"Player.Stop",%20"params":{"playerid":' + activePlayer + '},"id":1}')
    request = sendCommand( json.dumps({
        "jsonrpc": "2.0",
        "method": "Player.Stop",
        "params":{
            "playerid":activePlayer
        },
        "id":1
    }))

    return request

#Next
def next():
    activePlayer = str(getActivePlayer())
    #request = sendCommand(
     #   '{"jsonrpc":"2.0","method":"Player.GoTo","params":{"playerid":' + activePlayer + ',"to":"next"},"id":1}')
    request = sendCommand( json.dumps({
        "jsonrpc": "2.0",
        "method": "Player.GoTo",
        "params":{
            "playerid":activePlayer,
            "to":"next"
        },
        "id":1
    }))

    return request

#Previous
def previous():
    activePlayer = str(getActivePlayer())
    #request = sendCommand(
    #   '{"jsonrpc":"2.0","method":"Player.GoTo","params":{"playerid":' + activePlayer + ',"to":"previous"},"id":1}')
    request = sendCommand( json.dumps({
        "jsonrpc": "2.0",
        "method": "Player.GoTo",
        "params":{
            "playerid":activePlayer,
            "to":"previous"
        },
        "id":1
    }))

    return request


#set Volume
def setVolume(vol):
    #request = sendCommand(
    #   '{"jsonrpc":"2.0","method":"Application.SetVolume","params":%20{"volume":' + str(vol) + '},"id":1}')
    request = sendCommand( json.dumps({
        "jsonrpc": "2.0",
        "method": "Application.SetVolume",
        "params":{
            "volume":vol
        },
        "id":1
    }))

    #decoded = json.loads(request)
    return request

#get Volume
def getVolume():
    #request = sendCommand(
    #    '{%22jsonrpc%22:%222.0%22,%22method%22:%22Application.GetProperties%22,%22params%22:{%22properties%22:[%22volume%22]},%22id%22:%201}')
    request = sendCommand( json.dumps({
        "jsonrpc": "2.0",
        "method": "Application.GetProperties",
        "params":{
            "properties":"volume"
        },
        "id":1
    }))
    decoded = json.loads(request)
    return decoded["result"]["volume"]

#volume Up
def volumeUp():
    volume = int(getVolume()) + 5
    return setVolume(min(volume, 100))

#volume Down
def volumeDown():
    volume = int(getVolume()) - 5
    return setVolume(max(volume, 0))