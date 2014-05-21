#filters
#python modules
import time

#rgb-pi modules
import log
import constants
import datatypes
import utils
import server
import xbmcremote
import config

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
        self.active = True #TODO: not used yet
        self.filter = filter
        self.onfinish = filter['onfinish'] if filter.has_key('onfinish') else 'remove'
        self.type = type
        self.finishTrigger = self.finishTrigger = datatypes.Condition(filter['finish']) if filter.has_key('finish') else None
        if log.m(log.LEVEL_FILTERS): log.l('filter initialized: ' + self.type)


    def onChangeColor(self, newColor):
        """
        transforms the given color object
        @param newColor: color to be set as new color for the LEDs
        @return: transformed color according to the filter
        """
        return newColor

    def onFadeEnd(self, seconds, startColor, endColor):
        """
        called on the end of every fade
        @param seconds: time of the fade in seconds
        @param startColor: starting color of the fade
        @param endColor: ending color of the fade
        """
        pass

    def onFadeStep(self, seconds, startColor, endColor, progress):
        """
        called on the end of every fade
        @param seconds: time of the fade in seconds
        @param startColor: starting color of the fade
        @param endColor: ending color of the fade
        @param progress: progress of the fade as percent value between 0.0 and 1.0
        """
        pass

    def finish(self):
        if self.onfinish == constants.FILTER_ONFINISH_REMOVE:
            server.CurrentFilters.remove(self)

        if self.onfinish == constants.FILTER_ONFINISH_STOP:
            if server.CurrentCMD is not None:
                server.CurrentCMD.stop()
                server.CurrentCMD = None
                server.CurrentFilters = []
                if log.m(log.LEVEL_FILTER_ACTIONS): log.l(self.type+'-filter finished...')



    @staticmethod
    def createFilter(filter):
        if isinstance(filter, dict) and filter.has_key('type'):
            if filter['type'] == constants.FILTER_TYPE_DIM:
                return DimFilter(filter)
            if filter['type'] == constants.FILTER_TYPE_VOLUMEFADE:
                return VolumeFadeFilter(filter)
            if filter['type'] == constants.FILTER_TYPE_STOPMUSIC:
                return StopMusicFilter(filter)


class DimFilter(Filter):
    """
    this filter affects the led.setColor(color)-method and dims all incoming colors according to the defined time
    """
    def __init__(self, filter): # takes a command as json encoded object
        super(DimFilter, self).__init__(constants.FILTER_TYPE_DIM, filter)
        self.black = datatypes.Color(0,0,0)

    def onChangeColor(self, newColor):
        if not self.finishTrigger.check():
            self.finish()

        filteredColor = utils.interpolateColor(newColor, self.black, self.finishTrigger.progress())
        if log.m(log.LEVEL_FILTER_ACTIONS): log.l(self.type+'-filter color ('+str(self.finishTrigger.progress()*100)+'%) from '+str(newColor)+' to '+str(filteredColor))
        return filteredColor

class VolumeFadeFilter(Filter):
    """
    this filter affects the color changes in the corefunctions.fade() method.
    It changes the volume according to the progress percentage to 0% or 100%.
    """
    def __init__(self, filter): # takes a command as json encoded object
        if not config.ENABLE_XBMC_REMOTE:
            raise EnvironmentError(
                'config.ENABLE_XBMC_REMOTE needs to be enabled in order to send commands to your xbmc-service')
        super(VolumeFadeFilter, self).__init__(constants.FILTER_TYPE_VOLUMEFADE, filter)
        self.progress = filter['progress']
        self.limit = int(filter['limit'])

    def onFadeEnd(self, seconds, startColor, endColor):
        if not self.finishTrigger.check():
            self.finish()

    def onFadeStep(self, seconds, startColor, endColor, progress):
        if self.finishTrigger.type != constants.CONDITION_ITERATE and not self.finishTrigger.check():
            self.finish()
        p = self.finishTrigger.progress() if self.progress == 'louder' else 1.0-self.finishTrigger.progress()
        p = p*100
        if self.progress == 'louder':
            p = min(self.limit, p)
        else:
            p = max(self.limit, p)

        xbmcremote.setVolume(int(p))

class StopMusicFilter(Filter):
    """
    this filter affects the color changes in the corefunctions.fade() method.
    It changes the volume according to the progress percentage to 0% or 100%.
    """
    def __init__(self, filter): # takes a command as json encoded object
        if not config.ENABLE_XBMC_REMOTE:
            raise EnvironmentError(
                'config.ENABLE_XBMC_REMOTE needs to be enabled in order to send commands to your xbmc-service')
        super(StopMusicFilter, self).__init__(constants.FILTER_TYPE_STOPMUSIC, filter)

    def onChangeColor(self, newColor):
        if not self.finishTrigger.check():
            xbmcremote.stop()
            self.finish()

    def onFadeStep(self, seconds, startColor, endColor, progress):
        if not self.finishTrigger.check():
            xbmcremote.stop()
            self.finish()

    def onFadeEnd(self, seconds, startColor, endColor):
        if not self.finishTrigger.check():
            xbmcremote.stop()
            self.finish()

