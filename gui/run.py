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
    data.toolbarHeight = data.height / 8
    data.filters = [Filter("Distance", [253, 254, 260], 0),
                    Filter("Price", ["free", "$", "$$", "$$$"], 1)]
    recommendationList = generateRecommendationList(favorites=False)
    generateActivities(data, recommendationList)
    data.favoriteButton = FavoriteIcon()
    data.tileGrid = {"rows": 2, "cols" : 3}
    data.scrollY = 0
    data.scrollSpeed = 10
    data.drawingSmallTiles = True
    data.inBigTile = False
    data.usingFilter = False
    
def generateRecommendationList(favorites):
    filteredLocalActivities.storeCurrentSet(favorites)
    # recommendedLocalActivities.storeRecommendationList()
    recommendationList = recommendedLocalActivities.getRecommendationList()
    return recommendationList
    
def generateActivities(data, recommendationList):
    # recommendationList = recommendedLocalActivities.openRecommendationList()
    data.activities = [Tile(recommendationList[i][0], recommendationList[i][1], 
                       i) for i in range(len(recommendationList))]

def usingFilter(data):
    for filter in data.filters:
        if filter.isClicked:
            data.usingFilter = True
            return None
    data.usingFilter = False
    
def mousePressed(event, data):
    # interact with tiles
    if not data.usingFilter:
        if data.drawingSmallTiles:
            for activity in data.activities:
                if activity.clickInTile(data, event.x, event.y):
                    activity.smallTileIsClicked = True
                    data.drawingSmallTiles = False
                    data.inBigTile = True
                    break
        else:
            for activity in data.activities:
                if activity.smallTileIsClicked:
                    if not activity.clickInTile(data, event.x, event.y):
                        activity.smallTileIsClicked = False
                        data.drawingSmallTiles = True
                        data.inBigTile = False
                        break
            if data.inBigTile:
                for activity in data.activities:
                    if activity.smallTileIsClicked:
                        x0, y0, x1, y1 = activity.getBigTileCoordinates(data)
                        if activity.favoriteButton.clickInButton(data, event.x, event.y, x0, y0, x1, y1):
                                activity.favorite()
    # interact with filters
    for filter in data.filters:
        if filter.clickInFilter(data, event.x, event.y):
            filter.isClicked = not filter.isClicked
        if filter.isClicked:
            for i in range(len(filter.options)):
                if filter.clickInOption(data, event.x, event.y, i):
                    filter.selection = filter.options[i]
                    filteredLocalActivities.filters[filter.name] = filter.selection
                    newRecommendationList = generateRecommendationList(favorites=False)
                    generateActivities(data, newRecommendationList)
    usingFilter(data)
    # interact with favorites button
    x0, y0, x1, y1 = 0, 0, data.width, data.height
    if data.favoriteButton.clickInButton(data, event.x, event.y, x0, y0, x1, y1):
        data.favoriteButton.isClicked = not data.favoriteButton.isClicked
        newRecommendationList = generateRecommendationList(
                                    favorites=data.favoriteButton.isClicked)
        generateActivities(data, newRecommendationList)

def keyPressed(event, data):
    # scroll through tiles
    if event.keysym == "Up":
        if data.scrollY > 0:
            data.scrollY -= data.scrollSpeed
    elif event.keysym == "Down":
        data.scrollY += data.scrollSpeed

def timerFired(data):
    pass

def redrawAll(canvas, data):
    # draw large activity tiles
    for activity in data.activities:
        if activity.smallTileIsClicked:
            activity.drawBigTile(data, canvas)
    # draw small activity tiles
    if data.drawingSmallTiles:
        for activity in data.activities:
            activity.drawSmallTile(data, canvas)
    # draw toolbar
    canvas.create_rectangle(0, 0, data.width, data.toolbarHeight, 
                            fill = design.colors["toolbar"], width=0)
    # draw filters
    for filter in data.filters:
        filter.draw(data, canvas)
    # draw favorite button
    data.favoriteButton.draw(data, canvas, 0, 0, data.width, data.height)

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
        mousePressed(event, data)
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