import requests
import time
from bs4 import BeautifulSoup


def getLinks(urlEndpoint, links):
    links[urlEndpoint] = []
    response = requests.get('https://en.wikipedia.org?', urlEndpoint)
    soup = BeautifulSoup(response.text, 'html.parser')
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
    links = {}
    getLinks('/wiki/Web_scraping', links)
    print(links)

if __name__ == '__main__':
    main()