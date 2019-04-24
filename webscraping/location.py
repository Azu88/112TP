####################################
# adapted from
# https://www.freecodecamp.org/forum/t/make-a-script-read-gps-geolocation/241607
####################################

import requests
import math

def getUserLocation():
    ipRequest = requests.get("https://get.geojs.io/v1/ip.json")
    userIp = ipRequest.json()["ip"]
    geoRequestUrl = "https://get.geojs.io/v1/ip/geo/" + userIp + ".json"
    geoRequest = requests.get(geoRequestUrl)
    geoData = geoRequest.json()
    userLocation = {"latitude" : float(geoData["latitude"]),
                    "longitude" : float(geoData["longitude"]),
                    "city" : geoData["city"]}
    return userLocation
    
####################################
# adapted from
# https://nathanrooy.github.io/posts/2016-09-07/haversine-with-python/
####################################

# apply Haversine formula to calculate distance between two coordinate points    
def getDistance(lat1, long1, lat2, long2, unit):
    if lat1 is None or long1 is None or lat2 is None or long2 is None:
        return None
    # formula
    r = 6371000 # radius of Earth in meters
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    deltaPhi = math.radians(lat2 - lat1)
    deltaLambda = math.radians(long2 - long1)
    a = math.sin(deltaPhi / 2.0) ** 2 + \
        math.cos(phi1) * math.cos(phi2) * \
        math.sin(deltaLambda / 2.0) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    # output in various units
    distance = {"meters" : r * c,
                "km" : (r * c) / 1000.0,
                "miles" : (r * c) * 0.000621371}
    return distance[unit]