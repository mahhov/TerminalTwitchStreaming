import pafy
from urllib.request import urlopen
import json
import os
import glob
import re

key = 'AIzaSyAdkXuGc2f7xJg5FLTWBi2cRUhzAJD-eC0'
playlistId = "PLameShrvoeYfp54xeNPK1fGxd2a7IzqU2"
#playlistId = "PLameShrvoeYfzOWuBX2bbER0LXD9EuxGx"
playlistTitle = "muzik2"
query = ""
sums = []
searchResaults = []
totalItems = 0

def youtubeSearch(query):
    url = 'https://www.googleapis.com/youtube/v3/' + query
    return json.loads(urlopen(url).read().decode('utf-8'))

def youtubeSearchPlaylists(query):
    return youtubeSearch('search?key=' + key + '&part=snippet&maxResults=20&type=playlist&q=' + query)
    
def youtubeSearchPlaylistItems(playlistId, page):
    return youtubeSearch('playlistItems?key=' + key + '&part=snippet&maxResults=50&playlistId=' + playlistId + '&pageToken=' + page)
    
def makeQueryOnePage(playlistId, page):
    global sums, totalItems
    search = youtubeSearchPlaylistItems(playlistId, page)
    totalItems = search['pageInfo']['totalResults']
    for item in search['items']:
        videoId = item['snippet']['resourceId']['videoId']
        title = item['snippet']['title']
        sums.append([videoId, title])
    if ('nextPageToken' in search):
        return search['nextPageToken']
    
def makeQuery():
    global sums
    sums = []
    spaceQuery = playlistId.replace(' ', '+')
    nextPage = makeQueryOnePage(spaceQuery, '')
    while (nextPage):
        nextPage = makeQueryOnePage(spaceQuery, nextPage)

def searchPlaylists():
    global searchResaults
    spaceQuery = query.replace(' ', '+')
    resaults = youtubeSearchPlaylists(spaceQuery)
    searchResaults = []
    for i, item in enumerate(resaults['items']):
         searchResaults.append([item['snippet']['title'], item['id']['playlistId']])

def selectResault(i):
    global playlistId, playlistTitle
    playlistTitle, playlistId = searchResaults[i]
    makeQuery()

def downloadPrinter(status, i, sum, additional = ''):
    print("{:12.12} {:5} of {:5}   -   {:11.11}   {:30.30}    {:.30}".format(status, i + 1, len(sums), sum[0], sum[1], additional))

def downloadPlaylist(video):
    if (video):
        print("downlaoding videos")
    else:
        print("downlaoding audios")
    if not os.path.exists(playlistTitle):
        os.makedirs(playlistTitle)
    failed = []
    for i, sum in enumerate(sums):
        try:
            fileName = re.sub('[^a-zA-Z0-9 ]', '', sum[1])
            fileFound = glob.glob(playlistTitle + '/' + fileName + '.*')
            if (fileFound):
                downloadPrinter('skipped', i, sum)
            else:
                downloadPrinter('downloading', i, sum)
                p = pafy.new(sum[0])
                if (video):
                    p.getbest().download(playlistTitle)
                else:
                    s = p.getbestaudio()
                    s.download(playlistTitle + '/' + fileName + '.' + s.extension)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            failed.append([i, sum])
            downloadPrinter('failed', i, sum, fileName)
    print("=" * 10 + "  {:5} failed  ".format(len(failed)) + "=" * 10)
    for fail in failed:
        downloadPrinter('failed', fail[0], fail[1])
    
def displayPlaylist():
    print("=" * 100)
    print("title {:30.30}".format(playlistTitle))
    print("id {:30.30}".format(playlistId))
    print("retrieved {:5} of {:5}".format(len(sums), totalItems))
    print()
    print("query {:20.20}".format(query))
    for i, item in enumerate(searchResaults):
        print("{:3} :: {:30.30}".format(i + 1, item[0]))
    
def printHelp():
    print(" -- HELP PAGE -- ")
    print("q         : quit")
    print("r         : refresh")
    print("/<query>  : search")
    print("h         : help")
    print("d         : download audio only")
    print("v         : download video")
    print("")

def main():
    global query
    makeQuery()
    displayPlaylist()
    while(True):
        usrInput = input(": ")
        if (len(usrInput) == 0):
            pass
        elif (usrInput == "q"):
            exit()
        elif (usrInput[0] == "/"):
            query = usrInput[1:]
            searchPlaylists()
        elif (usrInput == "r"):
            searchPlaylists()
        elif (usrInput == "h"):
            printHelp()
        elif (usrInput == "d"):
            downloadPlaylist(False)
        elif (usrInput == "v"):
            downloadPlaylist(True)
        else:
            try: 
                selectResault(int(usrInput) - 1)
            except ValueError:
                pass
        displayPlaylist()

main()
