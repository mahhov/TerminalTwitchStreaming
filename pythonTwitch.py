import sys
from twitch.api import v3
import subprocess

sums = []
def printChannels(query = "dota2"):
    print("25")
    streams = v3.search.streams(query, limit = 25, offset = 1 * page)['streams']
    for i, stream in enumerate(streams):
    	sum = [i + 1, stream["channel"]["display_name"], stream["viewers"], stream["channel"]["url"]]
    	sums.append(sum)
    	print("{}   :   {}  ({})".format(sum[0], sum[1], sum[2]));
    sys.stdout.flush()

def gotoChannel(selection):
    selSum = sums[selection]
    print('going to {}'.format(selSum[1]))
    execute = "streamlink np 'omxplayer' twtich.tv/{} best".format(selSum[3]) 
    subprocess.call([execute])

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
