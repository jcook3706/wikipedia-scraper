import requests
import time
import json
import os
import threading
from bs4 import BeautifulSoup
from os.path import exists

lastTime= time.time()
numThreads = 4

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
        if(validLink(linkStr) and linkStr not in links[urlEndpoint]):
            links[urlEndpoint].append(linkStr)

def validLink(linkStr):
    if(linkStr[0:5] != '/wiki'):
        return False
    noList = ['/Wikipedia', '/File', '/Encyclopedia', '/Help', '/wiki/Special', '/wiki/Talk', '/Main_Page', '/Template', '/Free_content', '/wiki/Category']
    for noWord in noList:
        if(linkStr.find(noWord) != -1):
            return False
    return True

def main():
    startTime = time.time()
    numToScrape = 100
    depthToScrape = 2
    if not exists('links.txt'):
        links = {}
        visited = []
    else:
        links = json.load(open('links.txt'))
        visited = list(links.keys())
        os.remove('links.txt')
    if len(links.keys()) == 0:
        getLinks('/wiki/Web_scraping', links)
    # print(links)
    count = bfsIterate(numToScrape, depthToScrape, links, visited)
    # print(links.keys())
    json.dump(links, open('links.txt', 'w'))
    if(count > 0):
        print(f'Number of pages scraped this time: {count}')
        print(f'Average time per page: {(time.time()-startTime)/count}')
    else:
        print('No pages scraped')
    print(f'Total number of scraped pages: {len(links.keys())}')
    
def bfsIterate(numToScrape, depthToScrape, links, visited):
    count = 0
    for i in range(depthToScrape):
        for key in list(links.keys()):
            for i in range(0, len(links[key]), numThreads):
                if len(links[key])-i > numThreads and count+numThreads < numToScrape:
                    t1 = threading.Thread(target=getLinks, args=(links[key][i], links))
                    t2 = threading.Thread(target=getLinks, args=(links[key][i+1], links))
                    t3 = threading.Thread(target=getLinks, args=(links[key][i+2], links))
                    t4 = threading.Thread(target=getLinks, args=(links[key][i+3], links))
                    t1Flag = False
                    t2Flag = False
                    t3Flag = False
                    t4Flag = False
                    if links[key][i] not in visited:
                        t1.start()
                        t1Flag = True
                        visited.append(links[key][i])
                        count += 1
                    if links[key][i+1] not in visited:
                        t2.start()
                        t2Flag = True
                        visited.append(links[key][i+1])
                        count += 1
                    if links[key][i+2] not in visited:
                        t3.start()
                        t3Flag = True
                        visited.append(links[key][i+2])
                        count += 1
                    if links[key][i+3] not in visited:
                        t4.start()
                        t4Flag = True
                        visited.append(links[key][i+3])
                        count += 1
                    if t1Flag:
                        t1.join()
                    if t2Flag:
                        t2.join()
                    if t3Flag:
                        t3.join()
                    if t4Flag:
                        t4.join()
                else:
                    countCopy = count
                    for k in range(min(len(links[key])-i, numToScrape-countCopy)):
                        getLinks(links[key][i+k], links)
                        visited.append(links[key][i+k])
                        count+=1
                if(count%10 == 0 and count != 0):
                    print(count, ' wiki pages scraped')
                #time.sleep(2)
                if(count>=numToScrape):
                    return count
    return count

if __name__ == '__main__':
    main()