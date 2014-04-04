#python modules
import time

#logging module with different logging levels (see below)

#   0x0002 = print UI
LEVEL_UI = 0x0002

#   0x0010 = print critical errors
LEVEL_ERRORS = 0x0010

#   0x0020 = print commands (except 'cc')
LEVEL_COMMANDS = 0x0020

#   0x0040 = print cc commands
LEVEL_COMMAND_CC = 0x0040

#   0x0080 = starting and stopping threads
LEVEL_START_STOP_THREADS = 0x0080

#   0x0100 = changing color (communication with pi-blaster)
LEVEL_CHANGE_COLOR = 0x0100

#   0x0200 = logs of request actions
LEVEL_REQUESTS = 0x0200

#   0x0400 = constructor of a task
LEVEL_INIT_COMMAND = 0x0400

#   0x0800 = detailed command execution logs
LEVEL_COMMAND_DETAIL = 0x0800

#   0x1000 = information about the socket communication
LEVEL_SOCKET_COMMUNICATION = 0x1000

#   0x2000 = tracing security and authentication data
LEVEL_SECURITY = 0x2000

#   0x4000 = logs for addind and removing filters
LEVEL_FILTERS = 0x4000

#   0x8000 = logs for adding and removing filters
LEVEL_FILTER_ACTIONS = 0x4000



#set this variable to a value between 1 and 256 for debugging output
LOG_LEVEL = LEVEL_UI | LEVEL_ERRORS | LEVEL_COMMANDS | LEVEL_COMMAND_CC | LEVEL_INIT_COMMAND | LEVEL_START_STOP_THREADS | LEVEL_COMMAND_DETAIL | LEVEL_SOCKET_COMMUNICATION | LEVEL_SECURITY | LEVEL_FILTERS | LEVEL_FILTER_ACTIONS


def m(loglvl):
    """
    m=match
    returns true if configured logging level (log.LOG_LEVEL) matches the given 'loglvl'-parameter
    @rtype : True if 'loglevel'-parameter matches, otherwise False
    """
    global LOG_LEVEL
    return (loglvl & LOG_LEVEL) != 0x0


#prints the given message to stdout if loglevel mask matches the actual logging level, defined in LOG_LEVEL
#if no loglevel is given, a default loglevel of 0xFFFF (matches to all levels except 0x0000) is used
def l(msg, loglvl=0xFFFFF):
    """
    l=log
    if given 'loglvl'-parameter matches the current logging level, the 'msg' will be printed with the actual time as prefix
    @rtype : None
    """
    global LOG_LEVEL
    if (loglvl & LOG_LEVEL) != 0x0:
        print time.ctime(), ': ' , str(msg)
