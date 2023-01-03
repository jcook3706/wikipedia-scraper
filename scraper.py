import requests
import time
import json
import os
from multiprocessing import Pool
from bs4 import BeautifulSoup
from os.path import exists

lastTime= time.time()
count = 0
links = {}
visited = []
numProcesses = 8

def getLinks(urlEndpoint):
    global lastTime, visited
    thisPageLinks = (urlEndpoint, [])
    if urlEndpoint not in visited:
        response = requests.get(f'https://en.wikipedia.org{urlEndpoint}')
        soup = BeautifulSoup(response.text, 'html.parser')
        for link in soup.find_all('a'):
            linkStr = str(link.get('href'))
            if linkStr.find(':') != -1:
                linkStr = linkStr[:linkStr.find(':')]
            if validLink(linkStr) and linkStr not in thisPageLinks[1]:
                thisPageLinks[1].append(linkStr)
    return thisPageLinks

def validLink(linkStr):
    if(linkStr[0:5] != '/wiki'):
        return False
    noList = ['/Wikipedia', '/File', '/Encyclopedia', '/Help', '/wiki/Special', '/wiki/Talk', '/Main_Page', '/Template', '/Free_content', '/wiki/Category']
    for noWord in noList:
        if(linkStr.find(noWord) != -1):
            return False
    return True

def main():
    global count, links, visited
    startTime = time.time()
    numToScrape = 10000
    depthToScrape = 2
    if exists('links.txt') and exists('visited.txt'):
        links = json.load(open('links.txt'))
        visited = json.load(open('visited.txt'))
        os.remove('links.txt')
        os.remove('visited.txt')
    else:
        if exists('links.txt'):
            os.remove('links.txt')
        if exists('visited.txt'):
            os.remove('visited.txt')
        initLinks = getLinks('/wiki/Web_scraping')
        links[initLinks[0]] = initLinks[1]
    startNum = len(links.keys())
    bfsIterate(numToScrape, depthToScrape, links, visited, startNum)
    json.dump(links, open('links.txt', 'w'))
    json.dump(visited, open('visited.txt', 'w'))
    if(len(links.keys())-startNum > 0):
        print(f'Number of pages scraped this time: {len(links.keys())-startNum}')
        print(f'Average time per page: {(time.time()-startTime)/(len(links.keys())-startNum)}')
    else:
        print('No pages scraped')
    print(f'Total number of scraped pages: {len(links.keys())}')
    
def bfsIterate(numToScrape, depthToScrape, links, visited, startNum):
    global count, numProcesses
    for i in range(depthToScrape):
        for key in list(links.keys()):
            if key not in visited:
                print(f'Visiting the children of {key}')
                with Pool(16) as pool:
                    pageChunk = pool.map(getLinks, links[key])
                    for link in pageChunk:
                        if link[0] not in links.keys():
                            links[link[0]] = link[1]
                    pool.close()
                    pool.join()
                    print(f'Scraped so far: {len(links.keys())-startNum}')
                    if len(links.keys())-startNum>=numToScrape:
                        return
                visited.append(key)
        initLinks = getLinks('/wiki/Web_scraping')
        links[initLinks[0]] = initLinks[1]
    return
if __name__ == '__main__':
    main()