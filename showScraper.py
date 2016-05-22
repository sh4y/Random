import urllib2
import re

shows = []

f = open('shows.txt', 'r')
for line in f:
    shows.append(line.strip('\n'))
    
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
        episodes.append(item)
        i += 1
        if i-1 == newest:
            print("Episode name: " + extractName(item))
            print("Episode number: " + extractLatestEpisode(item))
            print(extractLink(item))
            print("Date: " + dates[newest])
        
