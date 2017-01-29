import sys
from twitch.api import v3
import subprocess

sums = []
def printChannels():
    streams = v3.search.streams('dota2')['streams']
    for i, stream in enumerate(streams):
    	sum = [i + 1, stream["channel"]["display_name"], stream["viewers"], stream["channel"]["url"]]
    	sums.append(sum)
    	print("{}   :   {}  ({})".format(sum[0], sum[1], sum[2]));
    sys.stdout.flush()

def gotoChannel(selection):
    selSum = sums[selection]
    print('going to {}'.format(selSum[1]))
    execute = "streamlink np 'omxplayer' twtich.tv/{}".format(selSum[3]) 
    subprocess.call([execute])



usrInupt = ""
while(usrInupt == ""):
    printChannels()
    usrInput = input(": ")
    if (usrInput == "q"):
        exit()
    else:
        try: 
            gotoChannel(int(usrInput) - 1)
        except ValueError:
            pass
