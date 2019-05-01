####################################
# Base Set Functions
####################################

import json

from webscraping.compilationWebsites import timeout

####################################

path = "data/session/baseSet.json"

# generate base set of local activities
def createBaseSet(userCity=None):
    baseSet = timeout.getAllActivities(userCity)
    return baseSet
    
# create base set and write to a file
def storeBaseSet(userCity=None):
    baseSet = createBaseSet(userCity)
    with open(path, "w+") as file:
        json.dump(baseSet, file)
    
# open base set file and return contents
def openBaseSet():
    with open(path, "r") as file:
        baseSet = json.load(file)
    return baseSet