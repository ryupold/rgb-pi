# this file will be used by the config.sh script to easily set-up the server
# and the configuration of the RGB-channels of your LED stripes.
# It's also able to install pi-blaster and configure communication with xbmc.

#python modules
import string
import os
import time

#rgb-pi modules
import defaultconfig


#config parameters
CONFIG = {
    'RED_PINS':'[5]',
    'GREEN_PINS':'[2]',
    'BLUE_PINS':'[6]',

    'MIN_VALUE':'0.08',

    'SERVER_PORT':'4321',

    'ENABLE_XBMC_REMOTE':'0',
    'XBMC_HOST':'127.0.0.1',
    'XBMC_PORT':'80'
}
#contains a string with the contents of the config file
configData = ''

#clears console
def cls():
    os.system(['clear','cls'][os.name == 'nt'])


def messageBoxAnyKey():
    raw_input("\npress any key to continue...")

#shows a message box with question and the choices 'y' for yes and 'n' for no
#returns 1 if yes was chosen and 0 if no, otherwise it loops til one of them was chosen
def messageBoxYesNo(question):
    while 1:
        answer = string.lower(raw_input(question + ' (y | n): '))
        if answer == 'y': return 1
        if answer == 'n': return 0

#shows a message box with a question for an integer number
#returns the
def messageBoxINT(question, min=-2147483648, max=2147483647):
    while 1:
        try:
            answer = int(raw_input(question + ': '))
            if answer < min or answer > max:
                raise ValueError
            else:
                return answer
        except ValueError:
            print 'please input an integer between '+str(min)+' and '+str(max)


def messageBoxChoose(question, **answers):
    choises = ''
    for key in answers:
        choises += '\n'+key+ ': '+answers[key]

    while 1:
        cls()
        answer = string.lower(raw_input(question+'\n'+choises+'\n: '))
        for key in answers:
            if(answer == string.lower(key)):
                return answer


def showMenu():
    choises = {'1':'install/uninstall pi-blaster (nessasary to control LEDs)',
               '2':'configure LED-channels',
               '3':'configure server',
               '4':'configure xbmc remote control',
               '5':'exit'
              }

    return messageBoxChoose('Welcome to the RGB-Pi configuration!\nChoose the configuration steps you want to proceed with:', **choises)

def ledConfig():
    pass

#reads the config file (if not existent, it's created with the data of the 'defaultconfig.py')
#checks if config data is complete and contains only valid data. if not it tries to autocorrect the data
def readConfig():
    cFile = open('config.py', 'r+')
    global configData
    configData = cFile.read()

    global CONFIG
    for k in CONFIG:
        index = configData.find(k)
        if index == -1:
            configData += '\n'+k+' = '+CONFIG[k]
        # TODO: autocorrect data

    cFile.close()

def writeConfig():
    cFile = open('config.py', 'r+')
    global configData
    cFile.write(configData)
    cFile.close()

def createConfig():
    exit = 0
    while not exit:
        menuitem = showMenu()

        if menuitem == '1':
            choises = {'1':'install pi-blaster',
                       '2':'uninstall pi-blaster'}
            a = messageBoxChoose('choose the next operation', **choises)

            if '1' == a:
                print 'installing pi-blaster (with --pcm option...)'
                time.sleep(1)
                os.system("sudo make -C ../pi-blaster/ install")
            elif a == '2' :
                print 'uninstalling pi-blaster'
                time.sleep(1)
                os.system("sudo make -C ../pi-blaster/ uninstall")

            messageBoxAnyKey()

        if menuitem == '2':
            stripes = messageBoxINT('How many LED-stripes do you have?\n(If two stripes are connected to the same channels, they count as one)')
            readConfig()

        if menuitem == '3':
            readConfig()

        if menuitem == '4':
            pass

        if menuitem == '5':
            exit = 1

# start
createConfig()