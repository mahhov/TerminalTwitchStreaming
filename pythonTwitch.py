#!python3

import sys
import subprocess

try :
    from twitch.api import v3
except:
    print("please sudo pip3 install python-twitch")

sums = []
def printChannels(query = "dota2"):
    print(" -- page {} --".format(page + 1))
    streams = v3.search.streams('dota2', 15, page * 15)['streams']
    for i, stream in enumerate(streams):
        sum = [i + 1, stream["channel"]["display_name"], stream["viewers"], stream["channel"]["url"]]
        sums.append(sum)
        print("{}   :   {}  ({})".format(sum[0], sum[1], sum[2]))
        #print("      {}".format(sum[3]))
    sys.stdout.flush()

def gotoChannel(selection):
    if (selection < 0 or selection >= len(sums)):
        return
    selSum = sums[selection]
    print('going to {}'.format(selSum[1]))
    execute = "streamlink -np 'omxplayer' '{}' best".format(selSum[3]) 
    #print("execute : {}".format(execute))
    try:
        subprocess.call(execute, shell=True)
    except ValueError:
        print("error")
        print(ValueError)

page = 0
usrInupt = ""
while(usrInupt == ""):
    printChannels()
    usrInput = input(": ")
    if (len(usrInput) == 0):
        pass
    elif (usrInput == "q"):
        exit()
    elif (usrInput[0] == "/"):
        printChannels(usrInput[1:])
    elif (usrInput == "n"):
        page += 1
    elif (usrInput == "p"):
        page -= 1 if page > 0 else 0
    else:
        try: 
            gotoChannel(int(usrInput) - 1)
        except ValueError:
            pass
