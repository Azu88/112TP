import requests
import json
from bs4 import BeautifulSoup
from bs4 import SoupStrainer

from webscraping import location

timeoutUrl = "https://www.timeout.com"

def getCityResponse(userCity=None):
    if userCity is None:
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
    if cityResponse is None: return None
    cityParser = BeautifulSoup(cityResponse.text, "html.parser",
                               parse_only=SoupStrainer("a"))
    for item in cityParser.find_all(class_="nav-item"):
        if item.get("href").startswith("/"):
            navItems.add(timeoutUrl + item.get("href"))
    return navItems

def getTileItems(navUrl):
    tileItems = set()
    city = navUrl.split("/")[3]
    pageResponse = requests.get(navUrl)
    pageParser = BeautifulSoup(pageResponse.text, "html.parser",
                               parse_only=SoupStrainer("div"))
    for item in pageParser.find_all(class_="tile__content"):
        for tag in item.find_all("a"):
            href = tag.get("href")
            if "#" not in href and href.startswith("/"):
                if city in href:
                    tileItems.add(timeoutUrl + href)
    if len(tileItems) > 0:
        return tileItems
    else: return None

def getListedActivities(tileUrl):
    listedActivities = {}
    pageResponse = requests.get(tileUrl)
    pageParser = BeautifulSoup(pageResponse.text, "html.parser",
                               parse_only=SoupStrainer("div"))
    for item in pageParser.find_all(class_="card-content"):
        for tag in item.find(class_="card-title").contents:
            if tag.string is not None and tag.string not in ["", "\n"]:
                tagInfo = tag.get("data-tracking")
                if tagInfo is not None:
                    tagInfo = json.loads(tagInfo)["attributes"]
                    if tagInfo["contentType"] == "venue":
                            listedActivities[tagInfo["contentName"]] = \
                                            tagInfo["contentUrl"]
    if len(listedActivities) > 0:
        return listedActivities
    else: return None

def getActivityInfo(activityUrl):
    return activityUrl

def getAllActivities(userCity=None):
    allActivities = {}
    urlsSeen = set()
    navItems = getNavItems(userCity)
    if navItems is None: return None
    for navUrl in navItems:
        tileItems = getTileItems(navUrl)
        if tileItems is not None:
            for tileUrl in tileItems:
                listedActivities = getListedActivities(tileUrl)
                if listedActivities is not None:
                    for activity in listedActivities:
                        activityUrl = listedActivities[activity]
                        if activityUrl not in urlsSeen:
                            allActivities[activity] = activityUrl
                            urlsSeen.add(activityUrl)
        else:
            listedActivities = getListedActivities(navUrl)
            if listedActivities is not None:
                for activity in listedActivities:
                    activityUrl = listedActivities[activity]
                    if activityUrl not in urlsSeen:
                        allActivities[activity] = getActivityInfo(activityUrl)
                        urlsSeen.add(activityUrl)
    return allActivities