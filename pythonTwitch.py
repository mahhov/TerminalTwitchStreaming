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
twitch = True
query = "dota2"
page = [0, 0, 0, 0]
usrInupt = ""
debug = False
mac = False
showDuration = False

def printHeader(title):
    print(bcolors.HEADER + title)
    print(" -- page {} --".format(page[0] + 1))
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
        print("{:4}:   {:60.60}  ({})".format(sum[0], sum[1], sum[2]))
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
            execute = "streamlink -np 'omxplayer' '{}' high".format(vid) 
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
    streams = v3.search.streams(query, 15, page[0] * 15)['streams']
    for i, stream in enumerate(streams):
        title = stream["channel"]["display_name"]
        viewers = stream["viewers"]
        streamUrl = stream["channel"]["url"]
        sums.append([i + 1, title, viewers, streamUrl])

def youtubeUrlRequest(type, params):
    return json.loads(urlopen('https://www.googleapis.com/youtube/v3/' + type + '?key=' + key + '&' + params).read().decode('utf-8'))

def parseYoutubeDuration(duration):
    duration = duration[2:]
    if (duration.find('M')  == - 1):
        return "0:0:" + duration[:-1]
    elif (duration.find('H') == -1):
        mMark = duration.find('M')
        return "0:" + duration[:mMark] + ":" + duration[mMark + 1:]
    else:
        hMark = duration.find('H')
        mMark = duration.find('M')
        return duration[:hMark] + ":" + duration[hMark + 1 : mMark] + ":" + duration[mMark + 1:]

def getYoutubeChannels():
    global page
    spaceQuery = query.replace(' ', '+')
    if (page[0] == 0):
        search = youtubeUrlRequest('search', 'part=snippet&type=video&maxResults=15&q=' + spaceQuery)
    else:
        search = youtubeUrlRequest('search', 'part=snippet&type=video&maxResults=15&q=' + spaceQuery + "&pageToken=" + page[1])
    page[2] = search['prevPageToken'] if 'prevPageToken' in search else 0
    page[3] = search['nextPageToken']
    for i, item in enumerate(search['items']):
        code = item['id']['videoId']
        title = item['snippet']['title']
        if (showDuration and i < 5):
            details = youtubeUrlRequest('videos', 'part=contentDetails&id=' + code)
            duration = parseYoutubeDuration(details['items'][0]['contentDetails']['duration'])
        else:
            duration = 0
        sums.append([i + 1, title, duration, code])

def makeQuery():
    global sums
    sums = []
    if (twitch):
        getTwitchChannels()
    else:
        getYoutubeChannels()

def changePage(v):
    global page
    if (page[0] + v >= 0):
        page[0] += v
        if (not twitch):
            if (v == 1):
                page[1] = page[3]
            else:
                page[1] = page[2]
    makeQuery()


def printHelp():
    print(" -- HELP PAGE -- ")
    print("q         : quit")
    print("t         : switch to twitch")
    print("t <query> : switch to and search twitch")
    print("y         : switch to youtube")
    print("y <query> : switch to and search youtube")
    print("/<query>  : search")
    print("n         : next page")
    print("p         : previous page")
    print("r         : refresh search")
    print("d         : toggle duration display (youtube only)")
    print("h         : help")
    print("")

def main():
    global twitch, page, query, showDuration
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
            page = [0, 0, 0, 0]
            makeQuery()
        elif (usrInput[0:2] == "t "):
            twitch = True
            page = [0, 0, 0, 0]
            query = usrInput[2:]
            makeQuery()
        elif (usrInput == "y"):
            twitch = False
            page = [0, 0, 0, 0]
            makeQuery()
        elif (usrInput[0:2] == "y "):
            twitch = False
            page = [0, 0, 0, 0]
            query = usrInput[2:]
            makeQuery()
        elif (usrInput[0] == "/"):
            query = usrInput[1:]
            makeQuery()
        elif (usrInput == "n"):
            changePage(1)
        elif (usrInput == "p"):
            changePage(-1)
        elif (usrInput == "r"):
            makeQuery()
        elif (usrInput == "d"):
            showDuration = not showDuration
        elif (usrInput == "h"):
            printHelp()
        else:
            try: 
                gotoSum(int(usrInput) - 1)
            except ValueError:
                pass
        displaySums()

main()

# showDuration levels
# go to page #
#twitch streaming green screen
#youtube json parse (fixed?)
#jpeg / screenshots
# subprocess exit