import sys
import subprocess
import pafy
from urllib.request import urlopen
import json
try :
    from twitch.api import v3
except:
    print("please sudo pip3 install python-twitch")

class bcolors:
    HEADER = '\033[1m\033[93m'
    LINE1 = '\033[1m\033[97m'
    LINE2 = '\033[1m\033[0m'
    ENDC = '\033[0m'

key = 'AIzaSyAdkXuGc2f7xJg5FLTWBi2cRUhzAJD-eC0'
sums = [] # i, name, secondary, url
twitch = False
query = "dota2"
page = 0
usrInupt = ""
debug = False
mac = True

def printHeader(title):
    print(bcolors.HEADER + title)
    print(" -- page {} --".format(page + 1))
    print("-" * 50)

def displaySums():
    if (twitch):
        printHeader("TWITCH")
    else:
        printHeader("YOUTUBE")
    for i, sum in enumerate(sums):
        if (i % 2 == 0):
            print(bcolors.LINE1, end="")
        else:
            print(bcolors.LINE2, end="")
        print("{:4}:   {:20}  ({})".format(sum[0], sum[1], sum[2]))
    print(bcolors.ENDC)
    sys.stdout.flush()

def gotoSum(selection):
    if (selection < 0 or selection >= len(sums)):
        return
    selSum = sums[selection]
    print('going to {}'.format(selSum[1]))
    if (twitch):
        vid = selSum[3]
        if (mac):
            execute = "streamlink -np 'quicktime player' '{}' best".format(vid) 
        else:
            execute = "streamlink -np 'omxplayer' '{}' best".format(vid) 
    else:
        vid = pafy.new(selSum[3]).getbest().url
        if (mac):
            execute = "open -a 'quicktime player' '{}'".format(vid)
        else:
            execute = "omxplayer '{}'".format(vid)
    if (debug):
        print("execute : {}".format(execute))
    else:
        try:
            subprocess.call(execute, shell=True)
        except ValueError:
            print("error")
            print(ValueError)

def getTwitchChannels():
    global sums
    sums = []
    streams = v3.search.streams(query, 15, page * 15)['streams']
    for i, stream in enumerate(streams):
        title = stream["channel"]["display_name"]
        viewers = stream["viewers"]
        streamUrl = stream["channel"]["url"]
        sums.append([i + 1, title, viewers, streamUrl])

def getYoutubeChannels():
    global sums
    sums = []
    search = json.loads(urlopen("https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&key="+key+"&q="+query).read())
    for i, item in enumerate(search['items']):
        code = item['id']['videoId']
        title = item['snippet']['title']
        details = json.loads(urlopen("https://www.googleapis.com/youtube/v3/videos?part=contentDetails&key="+key+"&id="+code).read())
        duration = details['items'][0]['contentDetails']['duration']
        # video = pafy.new(code, basic = False) # video.getbest().url]
        sums.append([i + 1, title, duration, code])

def makeQuery():
    sums = []
    if (twitch):
        getTwitchChannels()
    else:
        getYoutubeChannels()

def main():
    global twitch, page, query
    makeQuery()
    displaySums()
    while(usrInupt == ""):
        usrInput = input(": ")
        if (len(usrInput) == 0):
            pass
        elif (usrInput == "q"):
            exit()
        elif (usrInput == "t"):
            twitch = True
            page = 0
            query = usrInput[1:]
            makeQuery()
        elif (usrInput == "y"):
            twitch = False
            page = 0
            query = usrInput[1:]
            makeQuery()
        elif (usrInput[0] == "/"):
            query = usrInput[1:]
            makeQuery()
        elif (usrInput == "n"):
            page += 1
        elif (usrInput == "p"):
            page -= 1 if page > 0 else 0
        elif (usrInput == "r"):
            makeQuery()
        else:
            try: 
                gotoSum(int(usrInput) - 1)
            except ValueError:
                pass
        displaySums()

main()