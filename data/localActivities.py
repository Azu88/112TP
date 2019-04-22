import json

from webscraping.compilationWebsites import timeout

path = "data/session/baseSet.json"

def openBaseSet():
    with open(path, "r") as file:
        baseSet = json.load(file)
    for item in baseSet:
        print(item)
    
def createBaseSet(userCity=None):
    baseSet = timeout.getAllActivities(userCity)
    return baseSet
    
def storeBaseSet(userCity=None):
    baseSet = createBaseSet(userCity)
    with open(path, "w+") as file:
        json.dump(baseSet, file)