import json

from data import filteredLocalActivities

path = "data/session/recommendationList.json"

numRecommendations = 10

def createRecommendationList():
    currentSet = filteredLocalActivities.openCurrentSet()
    recommendationList = []
    for activity in currentSet:
        entry = [activity, currentSet[activity]]
        recommendationList.append(entry)
        if len(recommendationList) == numRecommendations:
            break
    return recommendationList

def storeRecommendationList():
    recommendationList = createRecommendationList()
    with open(path, "w+") as file:
        json.dump(recommendationList, file)
        
def openRecommendationList():
    with open(path, "r") as file:
        recommendationList = json.load(file)
    return recommendationList