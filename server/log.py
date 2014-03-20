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

#   0x0100 = changing color
LEVEL_CHANGE_COLOR = 0x0100

#   0x0200 = answer to an received request
LEVEL_ANSWER = 0x0200





#set this variable to a value between 1 and 256 for debugging output
LOG_LEVEL = LEVEL_UI + LEVEL_ERRORS + LEVEL_COMMANDS + LEVEL_COMMAND_CC + LEVEL_CHANGE_COLOR + LEVEL_ANSWER



#prints the given message to stdout if loglevel mask matches the actual logging level, defined in LOG_LEVEL
#if no loglevel is given, a default loglevel of 0xFFFF (matches to all levels except 0x0000) is used
def l(msg, loglvl=0xFFFF):
    global LOG_LEVEL
    if (loglvl & LOG_LEVEL) != 0x0:
        print str(msg)
