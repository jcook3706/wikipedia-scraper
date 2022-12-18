import requests
import time
import json
from bs4 import BeautifulSoup

lastTime= time.time()

def getLinks(urlEndpoint, links):
    global lastTime
    links[urlEndpoint] = []
    timeDelta = time.time()-lastTime
    #print(f'Time spent computing: {timeDelta}')
    lastTime = time.time()
    response = requests.get(f'https://en.wikipedia.org{urlEndpoint}')
    soup = BeautifulSoup(response.text, 'html.parser')
    timeDelta = time.time()-lastTime
    lastTime = time.time()
    # print(f'Time spent waiting for response: {timeDelta}')
    for link in soup.find_all('a'):
        linkStr = str(link.get('href'))
        if(linkStr.find(':') != -1):
            linkStr = linkStr[:linkStr.find(':')]
        if(validLink(linkStr)):
            links[urlEndpoint].append(linkStr)

def validLink(linkStr):
    if(linkStr[0:5] != '/wiki'):
        return False
    noList = ['/Wikipedia', '/File', '/Encyclopedia', '/Help', '/wiki/Special', '/wiki/Talk', '/Main_Page', '/Template', '/Free_content']
    for noWord in noList:
        if(linkStr.find(noWord) != -1):
            return False
    return True

def main():
    startTime = time.time()
    numToScrape = 1000
    depthToScrape = 2
    links = {}
    visited = []
    count = 0
    getLinks('/wiki/Web_scraping', links)
    # print(links)
    for i in range(depthToScrape):
        for key in list(links.keys()):
            for link in links[key]:
                if link not in visited:
                    getLinks(link, links)
                    visited.append(link)
                count+=1
                if(count%10 == 0):
                    print(count, ' wiki pages scraped')
                #time.sleep(2)
                if(count>numToScrape):
                    print(links.keys())
                    print(f'Average time per page: {(time.time()-startTime)/numToScrape}')
                    return
if __name__ == '__main__':
    main()