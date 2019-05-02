####################################
# Timeout Webscraping Functions
####################################

import requests
import json
from bs4 import BeautifulSoup, Doctype
from bs4 import SoupStrainer

from webscraping import location

####################################

timeoutUrl = "https://www.timeout.com"

parser = "lxml"

userLocation = location.getUserLocation()

## get urls of all listed activities

def getCityResponse(userCity=None):
    if userCity is None:
        userCity = userLocation["city"]
    url = timeoutUrl + "/" + userCity.replace(" ", "").lower()
    timeout = requests.get(url)
    if timeout.status_code == 200:
        return timeout
    else: return None
    
navItemStrainer = SoupStrainer(lambda tagName, d: (
    tagName == "a" and "nav-item" in d.get("class", [])))

def getNavItems(userCity=None):
    navItems = set()
    cityResponse = getCityResponse(userCity)
    if cityResponse is None: return None
    cityParser = BeautifulSoup(cityResponse.text, "html.parser",
                               parse_only=navItemStrainer)
    for item in cityParser:
        if isinstance(item, Doctype):
            item.extract()
        elif item.get("href").startswith("/"):
            navItems.add(timeoutUrl + item.get("href"))
    return navItems

tileItemStrainer = SoupStrainer(lambda tagName, d: (
    tagName == "div" and "tile__content" in d.get("class", [])))

def getTileItems(navUrl):
    tileItems = set()
    city = navUrl.split("/")[3]
    pageResponse = requests.get(navUrl)
    pageParser = BeautifulSoup(pageResponse.text, parser,
                               parse_only=tileItemStrainer)
    # limit = 10
    for item in pageParser:
        # if len(tileItems) > limit: break
        if isinstance(item, Doctype):
            item.extract()
        else:
            for tag in item.find_all("a"):
                href = tag.get("href")
                if "#" not in href and href.startswith("/"):
                    if city in href:
                        tileItems.add(timeoutUrl + href)
    if len(tileItems) > 0:
        return tileItems
    else: return None

listedActivityStrainer = SoupStrainer(lambda tagName, d: (
    tagName == "div" and "card-content" in d.get("class", [])))

def getListedActivities(tileUrl):
    listedActivities = {}
    pageResponse = requests.get(tileUrl)
    pageParser = BeautifulSoup(pageResponse.text, parser,
                               parse_only=listedActivityStrainer)
    # limit = 10
    for item in pageParser:
        # if len(listedActivities) > limit: break
        if isinstance(item, Doctype):
            item.extract()
        else:
            for tag in item.find(class_="card-title").contents:
                if tag.string is not None and tag.string not in ["", "\n"]:
                    tagInfo = tag.get("data-tracking")
                    if tagInfo is not None:
                        tagInfo = json.loads(tagInfo).get("attributes", {})
                        if tagInfo.get("contentType") == "venue":
                            if tagInfo.get("contentName") is not None:
                                listedActivities[tagInfo.get(
                                                    "contentName")] = \
                                                    tagInfo.get("contentUrl")
    if len(listedActivities) > 0:
        return listedActivities
    else: return None

### get activity information for each listed activity

activityInfoStrainer = SoupStrainer(lambda tagName, d: (
    tagName == "script" and "application/ld+json" in d.get("type", [])) or (
    tagName == "table" and "listing_details" in d.get("class", [])) or (
    tagName == "div" and ("reviewBody" in d.get("itemprop", []) or 
                          "expander__content" in d.get("class", []))) or (
    tagName == "span" and ("flag--categories" in d.get("class", []) or
                           "flag--price" in d.get("class", []))))

def flattenParagraph(tag):
    if tag is None: return None
    text = ""
    for item in tag.descendants:
        if isinstance(item, str):
            if item != "\n" or (item == "\n" and not text.endswith("\n\n")):
                text += item
        elif item.name in ["p", "br"] and not text.endswith("\n\n"):
            text += "\n"
    return text.strip()

def addScriptInfo(activityScript, features):
    scriptInfo = json.loads(activityScript.string)
    features["placeName"] = scriptInfo.get("name")
    features["url"] = scriptInfo.get("@id")
    features["location"] = {"latitude" : scriptInfo.get(
                                    "geo", {}).get("latitude"),
                            "longitude" : scriptInfo.get(
                                        "geo", {}).get("longitude")}
    features["address"] = {"streetAddress" : scriptInfo.get(
                                        "address", {}).get("streetAddress"),
                        "city" : scriptInfo.get(
                                "address", {}).get("addressLocality")}
    features["priceRange"] = scriptInfo.get("priceRange")
    
def addDescription(activityParser, features):
    activityBody = activityParser.find_all("div", class_="expander__content")
    if len(activityBody) > 0:
        description = flattenParagraph(activityBody[-1])
    else:
        activityBody = activityParser.find("div", itemprop="reviewBody")
        if activityBody is None:
            description = None
        else:
            description = flattenParagraph(activityBody)
    features["description"] = description

def getActivityCategories(activityCategories):
    categoriesString = flattenParagraph(activityCategories).strip()
    categories = categoriesString.split(" ")
    index = 0
    while index < len(categories):
        item = categories[index]
        if item == "and":
            categories.pop(index)
        else:
            if item.endswith(","):
                categories[index] = item[:-1].lower()
            else:
                categories[index] = item.lower()
            index += 1
    if "Things to do" in categoriesString: # fix ["things", "to", "do"] split
        categories = ["things to do"] + categories[3:]
    categories = list(set(categories)) # to remove duplicate elements
    if len(categories) > 0:
        return categories
    else: return None

def getActivityInfo(activityUrl):
    if activityUrl is None: return None
    features = {}
    activityResponse = requests.get(activityUrl)
    activityParser = BeautifulSoup(activityResponse.text, parser,
                                   parse_only=activityInfoStrainer)
    # get features listed in script
    activityScript = activityParser.find("script", type="application/ld+json")
    if activityScript is None: return None
    else:
        addScriptInfo(activityScript, features)
    # calculate distance from user
    features["distance"] = location.getDistance(userLocation["latitude"],
                                                userLocation["longitude"],
                                        features["location"]["latitude"],
                                        features["location"]["longitude"],
                                        "miles")
    # get activity description
    addDescription(activityParser, features)
    # check if activity is free
    if features["priceRange"] is None:
        activityPrice = activityParser.find("span", class_="flag--price")
        if activityPrice is not None and (
                    flattenParagraph(activityPrice).strip().lower() == "free"):
            features["priceRange"] = "free"
    # get activity categories
    activityCategories = activityParser.find("span", class_="flag--categories")
    if activityCategories is None:
        categories = None
    else:
        categories = getActivityCategories(activityCategories)
    features["categories"] = categories
    # get opening hours from table
    # activityTable = activityParser.find("table", class_="listing_details")
    return features

## get all information for all listed activities

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
                            urlsSeen.add(activityUrl)
                            activityFeatures = getActivityInfo(activityUrl)
                            if activityFeatures is not None:
                                allActivities[activity] = activityFeatures 
        else:
            listedActivities = getListedActivities(navUrl)
            if listedActivities is not None:
                for activity in listedActivities:
                    activityUrl = listedActivities[activity]
                    if activityUrl not in urlsSeen:
                        urlsSeen.add(activityUrl)
                        activityFeatures = getActivityInfo(activityUrl)
                        if activityFeatures is not None:
                            allActivities[activity] = activityFeatures
    return allActivities