####################################
# Ranking Functions
####################################

from data import favoriteActivities

####################################

tagCount = {}

# re-count frequency of activity tags appearing in the set of favorites
def updateTagCount():
    global tagCount
    tagCount = {}
    favorites = favoriteActivities.openFavoriteActivities()
    if favorites is not None:
        for activity in favorites:
            tags = favorites[activity]["categories"]
            if tags is not None:
                for tag in tags:
                    if tag in tagCount:
                        tagCount[tag] += 1
                    else:
                        tagCount[tag] = 1
    
# calculate score (tag count sum) corresponding to given list of activity tags
def getActivityScore(tags):
    score = 0
    if tags is not None:
        for tag in tags:
            if tag in tagCount:
                score += tagCount[tag]
    return score
    
# return list of activities sorted by score
def sortActivityList(activityList):
    activityList = sorted(activityList, key=lambda activity: activity[2])
    activityList.reverse()
    return activityList