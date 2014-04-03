#constants used by all scripts

#Command fifo
FIFO = '/dev/pi-blaster'

#command thread states
CMD_STATE_INIT = 0
CMD_STATE_STARTED = 1
CMD_STATE_STOPPED = 2


CMD_TYPE_CC = 'cc'
CMD_TYPE_FADE = 'fade'
CMD_TYPE_WAIT = 'wait'
CMD_TYPE_LIST = 'list'
CMD_TYPE_LOOP = 'loop'
CMD_TYPE_NOP = 'nop'

REQUEST_TYPE_CONFIG = 'config'
REQUEST_TYPE_RUNTIME = 'runtime'

REQUEST_RUNTIME_VARIABLE_COLOR = 'color'


CONDITION_BOOL = 1
CONDITION_COLOR = 2
CONDITION_TIME = 3
CONDITION_ITERATE = 4


