#requests to the server
import log
import constants
import led
import configure
import server

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

        answer = {"type":self.type, "variable":self.variable, "value":self.value}
        return answer

class RemoveRequest(Request):
    def __init__(self, request): # takes a command as json encoded object
        """
        initializes a new Remove-Request object
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
                    server.CurrentFilters.pop(i)
                    count = count + 1
                else:
                    i = i + 1

        answer = {"type":self.type, "item":self.item, "id":self.id, "count":count}
        return answer
