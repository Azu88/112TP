####################################
# Recommendation List Functions
####################################

import json
import os

from data import filteredLocalActivities, rank

####################################

path = "data/session/recommendationList.json"

# generate recommendation list of filtered, ranked local activities
def createRecommendationList():
    currentSet = filteredLocalActivities.openCurrentSet()
    recommendationList = []
    if currentSet is not None:
        for activity in currentSet:
            tags = currentSet[activity]["categories"]
            score = rank.getActivityScore(tags)
            entry = [activity, currentSet[activity], score]
            recommendationList.append(entry)
        recommendationList = rank.sortActivityList(recommendationList)
    return recommendationList

# create recommendation list and write to a file
def storeRecommendationList():
    recommendationList = createRecommendationList()
    with open(path, "w+") as file:
        json.dump(recommendationList, file)
        
# open recommendation list file and return contents
def openRecommendationList():
    with open(path, "r") as file:
        recommendationList = json.load(file)
    return recommendationList