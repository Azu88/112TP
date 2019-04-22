import requests
from bs4 import BeautifulSoup

from webscraping import location

timeoutUrl = "https://www.timeout.com"

def getCityResponse(userCity=None):
    if userCity == None:
        userCity = location.getUserLocation()["city"]
    url = timeoutUrl + "/" + userCity.replace(" ", "").lower()
    timeout = requests.get(url)
    if timeout.status_code == 404:
        return None
    else:
        return timeout

def getNavItems(userCity=None):
    navItems = set()
    cityResponse = getCityResponse(userCity)
    cityParser = BeautifulSoup(cityResponse.text, "html.parser")
    for item in cityParser.find_all("a", class_="nav-item"):
        if item.get("href").startswith("/"):
            navItems.add(timeoutUrl + item.get("href"))
    return navItems

def getTileItems(navUrl):
    tileItems = set()
    pageResponse = requests.get(navUrl)
    pageParser = BeautifulSoup(pageResponse.text, "html.parser")
    for item in pageParser.find_all(class_="tile__content"):
        for tag in item.find_all("a"):
            href = tag.get("href")
            if "#" not in href and href.startswith("/"):
                    tileItems.add(timeoutUrl + href)
    if len(tileItems) > 0:
        return tileItems
    else: return None

def getListedActivities(tileUrl):
    listedActivities = set()
    pageResponse = requests.get(tileUrl)
    pageParser = BeautifulSoup(pageResponse.text, "html.parser")
    for item in pageParser.find_all("div", class_="card-content"):
        for tag in item.find(class_="card-title").contents:
            if tag.string is not None and tag.string not in ["", "\n"]:
                listedActivities.add(tag.string.strip())
    if len(listedActivities) > 0:
        return listedActivities
    else: return None

def getAllActivities(userCity=None):
    allActivities = {}
    navItems = getNavItems(userCity)
    for navUrl in navItems:
        tileItems = getTileItems(navUrl)
        if tileItems is not None:
            for tileUrl in tileItems:
                listedActivities = getListedActivities(tileUrl)
                if listedActivities is not None:
                    for activity in listedActivities:
                        allActivities[activity] = ""
        else:
            listedActivities = getListedActivities(navUrl)
            if listedActivities is not None:
                for activity in listedActivities:
                    allActivities[activity] = ""
    return allActivities