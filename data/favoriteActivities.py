import json

path = "data/favorites/favoriteActivities.json"

favoriteActivities = {}

# def openFavoriteActivities():
#     try:
#         with open(path, "r+") as file:
#             favoriteActivities = json.load(file)
#     except FileNotFoundError:
#         with open(path, "w+") as file:
#             json.dump(None, file)
#             favoriteActivities = json.load(file)
#     return favoriteActivities
#     
# def updateFavoriteActivities(activity, activityFeatures):
#     with open(path, "w+") as file:
#         try:
#             favoriteActivities = json.load(file)
#         except:
#             favoriteActivities = {}
#         if activity in favoriteActivities:
#             favoriteActivities.remove(activity)
#         else:
#             favoriteActivities[activity] = activityFeatures
#         json.dump(favoriteActivities, file)

def updateFavoriteActivities(activity, activityFeatures):
        if activity in favoriteActivities:
            del favoriteActivities[activity]
        else:
            favoriteActivities[activity] = activityFeatures