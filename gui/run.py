####################################
# Run GUI
####################################

from tkinter import *

from gui.design import *
from gui.toolbar import *
from gui.tiles import *
from data import recommendedLocalActivities

####################################

def init(data):
    data.toolbarHeight = data.height / 8
    data.filters = [Filter("Distance", []),
                    Filter("Price", [])]
    recommendationList = recommendedLocalActivities.openRecommendationList()
    data.activities = [Tile(recommendationList[i][0], recommendationList[i][1], 
                       i) for i in range(len(recommendationList))]
    data.tileGrid = {"rows": 2, "cols" : 3}
    data.scrollY = 0
    data.scrollSpeed = 10
    data.drawingSmallTiles = True
    
def mousePressed(event, data):
    if data.drawingSmallTiles:
        for activity in data.activities:
            if activity.clickInTile(data, event.x, event.y):
                activity.smallTileIsClicked = True
                data.drawingSmallTiles = False
                break
    else:
        for activity in data.activities:
            if activity.smallTileIsClicked:
                if not activity.clickInTile(data, event.x, event.y):
                    activity.smallTileIsClicked = False
                    data.drawingSmallTiles = True
                    break

def keyPressed(event, data):
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
    for i in range(len(data.filters)):
        data.filters[i].draw(data, canvas, i)

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