#filters
#python modules
import time

#rgb-pi modules
import log
import constants
import datatypes
import utils
import server

class Filter(object):
    """
    represents an abstract request to the server
    """
    def __init__(self, type, filter): # takes a filter type and a filter as json encoded object
        """
        initializes a new Request object
        @param type: type of the request (see protocol)
        @param request: JSON object with the request
        @return: instance of Request
        """
        self.active = True
        self.filter = filter
        self.type = type
        self.finishTrigger = None
        if filter.has_key('finish'): self.finishTrigger = datatypes.Condition(filter['finish'])
        if log.m(log.LEVEL_FILTERS): log.l('filter initialized: ' + self.type)


    def onChangeColor(self, newColor):
        """
        transforms the given color object
        @param newColor: color to be set as new color for the LEDs
        @return: transformed color according to the filter
        """
        return newColor



    @staticmethod
    def createFilter(filter):
        if isinstance(filter, dict) and filter.has_key('type'):
            if filter['type'] == constants.FILTER_TYPE_DIM:
                return DimFilter(filter)


    @staticmethod
    def finish(filter):
        if server.CurrentCMD is not None:
            server.CurrentCMD.stop()
            server.CurrentCMD = None
            server.CurrentFilters = []
            if log.m(log.LEVEL_FILTER_ACTIONS): log.l(filter.type+'-filter finished...')


class DimFilter(Filter):
    """
    this filter affects the led.setColor(color)-method and dims all incoming colors according to the defined time
    """
    def __init__(self, filter): # takes a command as json encoded object
        super(DimFilter, self).__init__(constants.FILTER_TYPE_DIM, filter)
        self.time = datatypes.Time(filter['time'])
        self.startTime = None
        self.black = datatypes.Color(0,0,0)

    def onChangeColor(self, newColor):
        if self.startTime is None:
            self.startTime = time.time()

        if (self.finishTrigger is None or self.finishTrigger.check()) and time.time() - self.startTime < self.time.seconds:
            filteredColor = utils.interpolateColor(newColor, self.black, (time.time()-self.startTime)/self.time.seconds)
            if log.m(log.LEVEL_FILTER_ACTIONS): log.l(self.type+'-filter color ('+str(100.0-((time.time()-self.startTime)/self.time.seconds)*100.0)+'%) from '+str(newColor)+' to '+str(filteredColor))
            return filteredColor
        else:
            self.finish(self)
            return newColor
