from requests import get
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def getAllLinks(url:str, keyword: str):
    res = get(url)

    uniqueUrls = set()
    
    soup = BeautifulSoup(res.content, "html")
    
    list = []
    tags = soup.find_all("a")

    for item in tags:
        href = item.get("href")
        if keyword in href:

            if href not in uniqueUrls:
                uniqueUrls.add(href)
                normalizedUrl = urljoin(url, href)

                list.append(normalizedUrl)


    return uniqueUrls

def checkUrls(urlList: set, keyword: str):

    good = open("good_urls.txt", "w+")
    bad = open("bad_urls.txt", "w+")

    for url in urlList:
        try:
            res = get(url)
            if res.status_code == 200:
                good.write(url + "\n")
        except:
            bad.write(url + "\n")

    pass

targetUrl = input("what is the url? ")
keyword = input("what is the keyword? ")

links = getAllLinks(targetUrl, keyword)

checkUrls(links, keyword)

