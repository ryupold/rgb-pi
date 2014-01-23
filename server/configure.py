# this file will be used by the config.sh script to easily set-up the server
# and the configuration of the RGB-channels of your LED stripes.
# It's also able to install pi-blaster and configure communication with xbmc.

#python modules
import string
import os
import time
import re

#rgb-pi modules



#config parameters
CONFIG = {
    'RED_PINS': '[5]',
    'GREEN_PINS': '[2]',
    'BLUE_PINS': '[6]',

    'MIN_VALUE': '0.08',

    'DELAY': '0.01',

    'SERVER_PORT': '4321',

    'ENABLE_XBMC_REMOTE': '0',
    'XBMC_HOST': '\"127.0.0.1\"',
    'XBMC_PORT': '80'
}
#contains a string with the contents of the config file
configData = ''


##### MESSAGE BOXES START #####

#clears console
def cls():
    os.system(['clear', 'cls'][os.name == 'nt'])


def messageBoxAnyKey():
    raw_input("\npress any key to continue...")

#shows a message box with question and the choices 'y' for yes and 'n' for no
#returns 1 if yes was chosen and 0 if no, otherwise it loops til one of them was chosen
def messageBoxYesNo(question):
    while 1:
        answer = string.lower(raw_input(question + ' (y | n): '))
        if answer == 'y': return 1
        if answer == 'n': return 0

#shows a message box with question and the choices 'r' for RED, 'g' for GREEN and 'b' for BLUE
#returns 'r', 'g' or 'b' corresponding to the pressed key.
#cycles questioning 'til the user answers with one of the 3 choises
def messageBoxRGB():
    while 1:
        answer = string.lower(raw_input('' + ' (r=RED | g=GREEN | b=BLUE): '))
        if answer == 'r': return 'r'
        if answer == 'g': return 'g'
        if answer == 'b': return 'b'

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
            print 'please input an integer between ' + str(min) + ' and ' + str(max)


def messageBoxChoose(question, **answers):
    choises = ''
    for key in answers:
        choises += '\n' + key + ': ' + answers[key]

    while 1:
        cls()
        answer = string.lower(raw_input(question + '\n' + choises + '\n: '))
        for key in answers:
            if (answer == string.lower(key)):
                return answer

##### MESSAGE BOXES END #####


##### READ/WRITE CONFIG START #####

#reads the config file (if not existent, it's created with the data of the 'defaultconfig'-file)
#checks if config data is complete and contains only valid data. if not it tries to autocorrect the data
def readConfig():
    if not os.path.exists('./config.py'):
        dcFile = open('defaultconfig', 'r+')
        cFile = open('config.py', 'w+')
        cFile.write(dcFile.read())
        cFile.close()
        dcFile.close()

    cFile = open('config.py', 'r+')
    global configData
    configData = cFile.read()
    neededCorrection = 0
    global CONFIG
    for k in CONFIG:
        index = configData.find(k)
        if index == -1:
            configData += '\n' + k + ' = ' + CONFIG[k]
            neededCorrection = 1
            index = configData.find(k)

        #this extracts a relevant config line with the format: 'key = value'
        line = configData[index:configData.find('\n', index)]
        regex = re.compile(r"\s*[a-zA-Z]\w*\s*=\s*\S+\s*")
        found = regex.search(line)

        if found is None: #not a valid config entry
            print "ERROR in line: " + line + " ... corrected"
            configData = configData.replace(line, k + ' = ' + CONFIG[k])
            line = k + ' = ' + CONFIG[k]
            neededCorrection = 1

        # set value of the key into the config array
        CONFIG[k] = line.split("=", 1)[1].strip()

    cFile.close()
    if neededCorrection:
        writeConfig()



def writeConfig():
    if not (configData is None) and len(configData) > 0:
        cFile = open('config.py', 'w+')
        global configData
        for k in CONFIG:
            index = configData.find(k)
            line = configData[index:configData.find('\n', index)]
            configData = configData.replace(line, k + ' = ' + CONFIG[k])

        cFile.write(configData)
        cFile.close()
    else:
        raise IOError('configData variable is empty!')

##### READ/WRITE CONFIG END #####

##### LED CONFIG START #####
def ledConfig():
    pass

##### LED CONFIG END #####


##### MENU START #####
def showMenu():
    choises = {'1': 'install/uninstall pi-blaster (nessasary to control LEDs)',
               '2': 'configure LED-channels',
               '3': 'configure server',
               '4': 'configure xbmc remote control',
               '5': 'exit'
    }

    return messageBoxChoose(
        'Welcome to the RGB-Pi configuration!\nChoose the configuration steps you want to proceed with:', **choises)




def createConfig():
    exit = 0
    while not exit:
        menuitem = showMenu()

        if menuitem == '1':
            choises = {'1': 'install pi-blaster',
                       '2': 'uninstall pi-blaster'}
            a = messageBoxChoose('choose the next operation', **choises)

            if '1' == a:
                print 'installing pi-blaster (with --pcm option...)'
                time.sleep(1)
                os.system("sudo make -C ../pi-blaster/ install")
            elif a == '2':
                print 'uninstalling pi-blaster'
                time.sleep(1)
                os.system("sudo make -C ../pi-blaster/ uninstall")

            messageBoxAnyKey()

        if menuitem == '2':
            readConfig()
            stripes = messageBoxINT(
                'How many LED-stripes do you have?\n(If two stripes are connected to the same channels, they count as one)')
            testA = [[1, 2, 3]]
            print testA[0][0]
            raw_input()

            for i in range(0, stripes):
                pass



        if menuitem == '3':
            readConfig()
            global configData

            messageBoxAnyKey()

        if menuitem == '4':
            pass

        if menuitem == '5':
            exit = 1

##### MENU END #####

# start
createConfig()