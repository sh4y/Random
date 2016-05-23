import urllib2
import re
import sys

name = 'shows.txt'
if len(sys.argv) > 1:
    name = str(sys.argv[1])
    
shows = []
def extractName(string):
    return re.findall('<span class="tv_episode_name"> - (.*)<\/span>', string)[0]

def extractLatestEpisode(string):
    return re.findall('E([0-9]+)', string)[0]

def extractLink(string):
    return 'primewire.ag' + re.findall('a href="(.*)">E[0-9][0-9]*', string)[0]

def greatestIndex(lst):
    m = 0
    for i in range(0, len(lst)):
        if lst[i] > lst[m]:
            m = i
    return m

def printList(lst):
    for i in lst:
        print(i)

if name == 'new.txt':
    PRINT_LINKS = True
else:
    PRINT_LINKS = False
    
f = open(name, 'r')
for line in f:
    shows.append(line.strip('\n'))
    
for url in shows:
    print('--------------------------------------------------------------------------------------------')
    page = urllib2.urlopen(url).read()
    links = []
    episodes = []
    dates = []

    for date in re.findall('<span class="tv_episode_airdate"> - (.*)<\/span>', page):
        dates.append(date)
    newest = greatestIndex(dates)
    i = 0
    for item in re.findall('<div class="tv_episode_item".*<\/span>', page):
        links.append(extractLink(item))
        episodes.append(item)
        i += 1
        if i-1 == newest:
            print("Episode name: " + extractName(item))
            print("Episode number: " + extractLatestEpisode(item))
            print(extractLink(item))
            print("Date: " + dates[newest])
    if PRINT_LINKS:
        printList(links)
