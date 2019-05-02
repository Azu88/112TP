####################################
# Run GUI
####################################

from tkinter import *

from gui.design import *
from gui.toolbar import *
from gui.tiles import *
from data import filteredLocalActivities, recommendedLocalActivities

####################################

def init(data):
    # design attributes
    data.toolbarHeight = data.height / 8
    data.tileGrid = {"rows": 2, "cols" : 3}
    data.scrollSpeed = 10
    # drawing status
    data.drawingSmallTiles = True
    data.usingFilter = False
    data.scrollY = 0
    # toolbar
    data.filters = [Filter("Distance", [1, 5, 10, 25, 50, 100], 0),
                    Filter("Price", ["free", "$", "$$", "$$$"], 1),
                    Filter("Category", filteredLocalActivities.categories, 2)]
    data.favoriteButton = FavoriteIcon("toolbar")
    # generate activities to display
    rank.updateTagCount()
    generateActivities(data)
    
def generateActivities(data, onlyFavorites=False):
    filteredLocalActivities.storeCurrentSet(onlyFavorites)
    recommendedLocalActivities.storeRecommendationList()
    recommendationList = recommendedLocalActivities.openRecommendationList()
    data.activities = [Tile(recommendationList[i][0], recommendationList[i][1], 
                       i) for i in range(len(recommendationList))]
    
## check drawing status

# check if any filters are currently open
def usingFilter(data):
    for filter in data.filters:
        if filter.isClicked:
            data.usingFilter = True
            return None
    data.usingFilter = False
    
# check if a small tile has been clicked
def smallTileClicked(data, eventX, eventY):
    for activity in data.activities:
        if activity.onScreen and activity.clickInTile(data, eventX, eventY):
            data.drawingSmallTiles = False # stop drawing small tiles
            activity.smallTileIsClicked = True
            return None
    
# check for user interaction with big tile
def bigTileClicked(data, canvas, eventX, eventY):
    for activity in data.activities:
        if activity.smallTileIsClicked:
            # check if current big tile should be exited
            if not activity.clickInTile(data, eventX, eventY):
                data.drawingSmallTiles = True # start drawing small tiles
                activity.smallTileIsClicked = False
                break
            else:                        
                # check if current big tile's favorite button has been clicked
                if activity.favoriteButton.clickInButton(data, eventX, eventY):
                    activity.favorite()
                # check if current activity's url has been clicked
                activity.clickInUrl(data, canvas, eventX, eventY)
    
## respond to user actions

# respond to user interaction with filters
def updateFilters(data, eventX, eventY):
    for filter in data.filters:
        # check for click in filter
        if filter.clickInFilter(data, eventX, eventY):
            filter.isClicked = not filter.isClicked
        # check for click in options & update user selection accordingly
        if filter.isClicked: 
            for i in range(len(filter.options)):
                if filter.clickInOption(data, eventX, eventY, i):
                    # if the selected option is clicked, reset filter setting
                    if filter.options[i] == filter.selection:
                        filter.selection = None
                    # if a different option is clicked, change filter setting
                    else:
                        filter.selection = filter.options[i]
                    # regenerate activities to display
                    filteredLocalActivities.filters[filter.name] = filter.selection
                    generateActivities(data, onlyFavorites=data.favoriteButton.isClicked)
    usingFilter(data)
    
def mousePressed(event, data, canvas):
    # interact with tiles
    if not data.usingFilter:
        # if small tiles are currently displayed, check if one has been clicked
        if data.drawingSmallTiles:
            smallTileClicked(data, event.x, event.y)
        # if a big tile is currently displayed, check for user interaction
        else:
            bigTileClicked(data, canvas, event.x, event.y)
    # interact with filters
    updateFilters(data, event.x, event.y)
    # interact with favorites button
    if data.favoriteButton.clickInButton(data, event.x, event.y):
        data.favoriteButton.isClicked = not data.favoriteButton.isClicked
        generateActivities(data, onlyFavorites=data.favoriteButton.isClicked)
        data.scrollY = 0
        
def keyPressed(event, data):
    # scroll through tiles
    if data.drawingSmallTiles:
        if event.keysym == "Up":
            if data.scrollY > 0:
                data.scrollY -= data.scrollSpeed
        elif event.keysym == "Down":
            data.scrollY += data.scrollSpeed
        # check which tiles are currently being displayed
        for activity in data.activities:
            activity.checkIfOnScreen(data)
    
def timerFired(data):
    pass

## draw canvas

def redrawAll(canvas, data):
    # draw large activity tiles
    for activity in data.activities:
        if activity.smallTileIsClicked:
            activity.drawBigTile(data, canvas)
    # draw small activity tiles
    if data.drawingSmallTiles:
        for activity in data.activities:
            if activity.onScreen:
                activity.drawSmallTile(data, canvas)
    # draw toolbar
    canvas.create_rectangle(0, 0, data.width, data.toolbarHeight, 
                            fill = design.colors["toolbar"], width=0)
    # draw filters
    for filter in data.filters:
        filter.draw(data, canvas)
    # draw favorite button
    data.favoriteButton.draw(data, canvas)

####################################
# adapted from https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
####################################

# run the application gui
def runApp(width=800, height=600):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data, canvas)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    # data.timerDelay = 1000 # milliseconds
    root = Tk()
    root.title("Bored?")
    root.resizable(width=False, height=False) # prevents resizing window
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    redrawAllWrapper(canvas, data)
    # timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed