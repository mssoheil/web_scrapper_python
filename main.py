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
        if href == None:
            continue

        if keyword in href:

            if href not in uniqueUrls:
                uniqueUrls.add(href)
                normalizedUrl = urljoin(url, href)

                list.append(normalizedUrl)


    return uniqueUrls

def checkUrls(urlList: list, keyword: str, goodList: set, badList: set):

    for url in urlList:
        try:
            res = get(url)
            if res.status_code == 200:
                if url not in goodList:
                    print(f"checking URL {url}")
                    goodList.add(url)
                    links = getAllLinks(url, keyword)
                    sublists = checkUrls(links, keyword, goodList, badList)

                    goodList.update(sublists["good"])
                    badList.update(sublists["bad"])
        except Exception as e:
            print(f"Error checking URL {url}: {e}")
            badList.add(url)

    return {"good": goodList, "bad": badList}

def writeToFile(goodUrls: set, badUrls: set):
    good = open("good_urls.txt", "w+")
    bad = open("bad_urls.txt", "w+")

    for url in goodUrls:
        good.write(url + "\n")
        

    for url in badUrls:
        bad.write(url + "\n")
        

targetUrl = input("what is the url? ")
keyword = input("what is the keyword? ")

goodList = set()
badList = set()

links = getAllLinks(targetUrl, keyword)

urlList = checkUrls(links, keyword, goodList, badList)

print("good -----", urlList["good"])
print("bad -----", urlList["bad"])

writeToFile(urlList["good"], urlList["bad"])



