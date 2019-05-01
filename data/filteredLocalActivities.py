####################################
# Current Set Functions
####################################

import json

from data import localActivities, favoriteActivities

####################################

path = "data/session/currentSet.json"

categories = ["Attractions", "Bakeries", "Bars", "Hotels", "Museums", 
              "Music", "Parks", "Restaurants", "Shopping", "Sports"]

filters = {"Distance" : None,
           "Price" : None,
           "Category" : None}

# check if given activity passes user's filter settings
def passesFilters(filters, features):
    for filter in filters:
        if filters[filter] is None: continue
        elif filter == "Distance":
            if features["distance"] is not None:
                if features["distance"] > filters[filter]:
                    return False
        elif filter == "Price":
            if features["priceRange"] is not None:
                if features["priceRange"] != filters[filter]:
                    return False
        elif filter == "Category":
            if features["categories"] is not None:
                if filters[filter].lower() not in features["categories"]:
                    return False
    return True

# generate current set of filtered local activities
def createCurrentSet(onlyFavorites):
    baseSet = localActivities.openBaseSet()
    currentSet = None
    if baseSet is None:
        return currentSet
    elif not onlyFavorites and set(filters.values()) == set([None]):
        currentSet = baseSet
    else:
        currentSet = {}
        if onlyFavorites:
            favorites = favoriteActivities.openFavoriteActivities()
            if favorites is None: return None
        for activity in baseSet:
            if onlyFavorites:
                if activity not in favorites:
                    continue
            features = baseSet[activity]
            if passesFilters(filters, features):
                currentSet[activity] = features
    if len(currentSet) > 0:
        return currentSet
    else: return None
    
# create current set and write to a file
def storeCurrentSet(favorites=False):
    currentSet = createCurrentSet(favorites)
    with open(path, "w+") as file:
        json.dump(currentSet, file)
    
# open current set file and return contents
def openCurrentSet():
    with open(path, "r") as file:
        currentSet = json.load(file)
    return currentSet