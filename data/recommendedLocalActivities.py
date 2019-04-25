import json
import os

from data import filteredLocalActivities

path = "data/session/recommendationList.json"

numRecommendations = 10

def createRecommendationList():
    currentSet = filteredLocalActivities.openCurrentSet()
    recommendationList = []
    if currentSet is not None:
        for activity in currentSet:
            entry = [activity, currentSet[activity]]
            recommendationList.append(entry)
            if len(recommendationList) == numRecommendations:
                break
    return recommendationList

def storeRecommendationList():
    os.chmod("data/session", 0o777)
    recommendationList = createRecommendationList()
    with open(path, "w+") as file:
        json.dump(recommendationList, file)
        
def openRecommendationList():
    with open(path, "r") as file:
        recommendationList = json.load(file)
    return recommendationList
    
def getRecommendationList():
    recommendationList = createRecommendationList()
    return recommendationList