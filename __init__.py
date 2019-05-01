####################################
# Main File
####################################

import datetime

from gui import run
from data import localActivities

####################################

# wait for webscraping to finish
# print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
# print("webscraping...")
# localActivities.storeBaseSet("Philadelphia")
# print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

# run GUI
run.runApp()