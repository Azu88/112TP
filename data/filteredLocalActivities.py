import json

from data import localActivities

path = "data/session/currentSet.json"

filters = {"Distance" : 254,
           "Price" : "free"}

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
    return True

def createCurrentSet():
    baseSet = localActivities.openBaseSet()
    currentSet = None
    if baseSet is None:
        return currentSet
    elif set(filters.values()) == set([None]):
        currentSet = baseSet
    else:
        currentSet = {}
        for activity in baseSet:
            features = baseSet[activity]
            if passesFilters(filters, features):
                currentSet[activity] = features
    if len(currentSet) > 0:
        return currentSet
    else: return None
    
def storeCurrentSet():
    currentSet = createCurrentSet()
    with open(path, "w+") as file:
        json.dump(currentSet, file)
    
def openCurrentSet():
    pass