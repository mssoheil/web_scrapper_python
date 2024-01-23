from requests import get
from bs4 import BeautifulSoup

def getPage(url:str):
    res = get(url)
    
    soup = BeautifulSoup(res.content, "html")
    
    list = []
    tags = soup.find_all("a")

    for item in tags:
        print(item.get("href"))
    return list


print(getPage(input("what is the url? ")))