#requests to the server

#python modules
import json

#rgb-pi modules
import log
import constants
import led
import configure
import server
import xbmcremote

class Request(object):
    """
    represents an abstract request to the server
    """
    def __init__(self, type, request): # takes a command as json encoded object
        """
        initializes a new Request object
        @param type: type of the request (see protocol)
        @param request: JSON object with the request
        @return: instance of Request
        """
        self.request = request
        self.type = type
        if log.m(log.LEVEL_REQUESTS): log.l('request received: ' + self.request)

    def execute(self):
        """
        executes the request and returns an answer according to the protocol
        @return: answer as JSON object
        """
        if log.m(log.LEVEL_REQUESTS): log.l('executing request of type: ' + self.type)
        return None

    @staticmethod
    def createRequest(request):
        if isinstance(request, dict) and request.has_key('type'):
            if request['type'] == constants.REQUEST_TYPE_CONFIG:
                return ConfigRequest(request)
            if request['type'] == constants.REQUEST_TYPE_RUNTIME:
                return RuntimeRequest(request)
            if request['type'] == constants.REQUEST_TYPE_REMOVE:
                return RemoveRequest(request)
            if request['type'] == constants.REQUEST_TYPE_XBMC:
                return XBMCRequest(request)




class ConfigRequest(Request):
    def __init__(self, request): # takes a command as json encoded object
        """
        initializes a new Config-Request object
        @param type: type of the request (see protocol)
        @param request: JSON object with the request
        @return: instance of Request
        """
        super(ConfigRequest, self).__init__(constants.REQUEST_TYPE_CONFIG, request)
        self.keys = request['keys']
        self.values = []

    def execute(self):
        super(ConfigRequest, self).execute()
        configure.readConfig()
        for key in self.keys:
            if configure.CONFIG.has_key(key):
                self.values.append(configure.CONFIG[key])
            else:
                raise KeyError('there is no config entry with the name \''+key+'\'')

        answer = {"type":self.type, "keys":self.keys, "values":self.values}
        return answer


class RuntimeRequest(Request):
    def __init__(self, request): # takes a command as json encoded object
        """
        initializes a new Runtime-Request object
        @param request: JSON object with the request
        @return: instance of Request
        """
        super(RuntimeRequest, self).__init__(constants.REQUEST_TYPE_RUNTIME, request)
        self.variable = request['variable']
        self.value = None

    def execute(self):
        super(RuntimeRequest, self).execute()

        if self.variable == constants.REQUEST_RUNTIME_VARIABLE_COLOR:
            self.value = str(led.COLOR[0])
        if self.variable == constants.REQUEST_RUNTIME_VARIABLE_FILTERS:
            self.value  = '{'
            for f in server.CurrentFilters:
                self.value += json.dumps(f.filter)
            self.value += '}'
            #self.value = json.dumps(server.CurrentFilters)
        if self.variable == constants.REQUEST_RUNTIME_VARIABLE_TRIGGERS:
            self.value  = '{'
            for k,t in server.triggerManager.triggers.items():
                self.value += json.dumps(t.trigger)
            self.value += '}'
            #self.value = json.dumps(server.triggerManager.triggers)

        answer = {"type":self.type, "variable":self.variable, "value":self.value}
        return answer

class RemoveRequest(Request):
    def __init__(self, request): # takes a command as json encoded object
        """
        initializes a new Remove-Request object for removing runtime-items
        @param request: JSON object with the request
        @return: instance of Request
        """
        super(RemoveRequest, self).__init__(constants.REQUEST_TYPE_REMOVE, request)
        self.item = request['item']
        self.id = request['id']

    def execute(self):
        super(RemoveRequest, self).execute()
        count = 0
        if self.item == 'filter':
            i = 0
            while i < len(server.CurrentFilters):
                if server.CurrentFilters[i].type == self.id:
                    filter = server.CurrentFilters.pop(i)
                    if log.m(log.LEVEL_FILTERS): log.l('removing ' + filter.type+' filter')
                    count = count + 1
                else:
                    i += 1
        if self.item == 'trigger':
            try:
                server.triggerManager.removeTrigger(self.id)
                count = 1
            except:
                count = 0

        answer = {"type":self.type, "item":self.item, "id":self.id, "count":count}
        return answer

class XBMCRequest(Request):
    def __init__(self, request): # takes a command as json encoded object
        """
        initializes a new XMBC-Request object
        @param request: JSON object with the request
        @return: instance of Request
        """
        super(XBMCRequest, self).__init__(constants.REQUEST_TYPE_REMOVE, request)
        self.action = constants.REQUEST_XBMC_ACTION_GET if request.has_key(constants.REQUEST_XBMC_ACTION_GET) \
            else constants.REQUEST_XBMC_ACTION_SET if request.has_key(constants.REQUEST_XBMC_ACTION_SET) \
            else constants.REQUEST_XBMC_ACTION_CMD if request.has_key(constants.REQUEST_XBMC_ACTION_CMD) \
            else None
        if self.action is None:
            raise ValueError('no action (get or set) specified')
        self.cmd = request[self.action]
        self.answer = None

    def execute(self):
        super(XBMCRequest, self).execute()

        if self.action == constants.REQUEST_XBMC_ACTION_GET:
            if self.cmd == 'player':
                self.answer = xbmcremote.getActivePlayer()
            if self.cmd == 'volume':
                self.answer = xbmcremote.getVolume()

        if self.action == constants.REQUEST_XBMC_ACTION_SET:
            if self.cmd == 'notification':
                self.answer = xbmcremote.showNotification(self.request['params'][0], self.request['params'][1])
            if self.cmd == 'playpause':
                self.answer = xbmcremote.playPause()
            if self.cmd == 'stop':
                self.answer = xbmcremote.stop()
            if self.cmd == 'next':
                self.answer = xbmcremote.next()
            if self.cmd == 'previous':
                self.answer = xbmcremote.previous()
            if self.cmd == 'volume':
                self.answer = xbmcremote.setVolume(int(self.request['params'][0]))
            if self.cmd == 'volup':
                self.answer = xbmcremote.volumeUp()
            if self.cmd == 'voldown':
                self.answer = xbmcremote.volumeDown()

        if self.action == constants.REQUEST_XBMC_ACTION_CMD:
            self.answer = xbmcremote.sendCommand(self.cmd)

        answer = {"type":self.type, self.action:self.cmd, "answer":self.answer}
        return answer