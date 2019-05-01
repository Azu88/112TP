####################################
# Favorite Set Functions
####################################

import json

####################################

path = "data/favorites/favoriteActivities.json"
    
# open favorite set file and return contents
def openFavoriteActivities():
    try:
        with open(path, "r+") as file:
            favoriteActivities = json.load(file)
    except:
        with open(path, "w+") as file:
            json.dump(None, file)
            favoriteActivities = None
    return favoriteActivities
    
# add/remove given activity to/from favorite set
def updateFavoriteActivities(activity, activityFeatures):
    with open(path, "r+") as file:
        favoriteActivities = json.load(file)
    if favoriteActivities is None:
        favoriteActivities = {activity : activityFeatures}
    elif activity in favoriteActivities:
        del favoriteActivities[activity]
    else:
        favoriteActivities[activity] = activityFeatures
    with open(path, "w+") as file:
        json.dump(favoriteActivities, file)