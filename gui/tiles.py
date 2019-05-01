####################################
# Activity Tile Class
####################################

from gui import design
from gui import toolbar
from data import favoriteActivities, rank

####################################

class Tile(object):
    
    def __init__(self, activityName, activityFeatures, gridIndex):
        # activity information
        self.activityName = activityName
        self.activityFeatures = activityFeatures
        self.placeName = activityFeatures["placeName"]
        self.url = activityFeatures["url"]
        self.location = activityFeatures["location"]
        self.address = activityFeatures["address"]
        self.priceRange = activityFeatures["priceRange"]
        self.distance = activityFeatures["distance"]
        self.description = activityFeatures["description"]
        self.categories = activityFeatures["categories"]
        # drawing information
        self.favoriteButton = toolbar.FavoriteIcon()
        self.gridIndex = gridIndex
        # drawing status
        self.smallTileIsClicked = False
        self.onScreen = True
        # data stored
        self.isFavorite = self.checkIfFavorite()
        
## calculate tile coordinates
        
    # calculate corner coordinates of the activity's small tile
    def getSmallTileCoordinates(self, data):
        marginOutside = data.width // 40
        gridRows, gridCols = data.tileGrid["rows"], data.tileGrid["cols"]
        tileWidth = (data.width - marginOutside * (gridCols + 1)) / gridCols
        tileHeight = (data.height - data.toolbarHeight -
                     (marginOutside * (gridRows + 1))) / gridRows
        tileRow, tileCol = self.gridIndex // gridCols, self.gridIndex % gridCols
        x0 = marginOutside * (tileCol + 1) + tileWidth * tileCol 
        y0 = marginOutside * (tileRow + 1) + tileHeight * tileRow + \
             data.toolbarHeight - data.scrollY
        x1 = marginOutside * (tileCol + 1) + tileWidth * (tileCol + 1)
        y1 = marginOutside * (tileRow + 1) + tileHeight * (tileRow + 1) + \
             data.toolbarHeight - data.scrollY
        return((int(x0), int(y0), int(x1), int(y1)))
        
    # calculate corner coordinates of the activity's big tile
    def getBigTileCoordinates(self, data):
        marginOutside = data.width // 20
        x0 = marginOutside
        y0 = data.toolbarHeight + marginOutside
        x1 = data.width - marginOutside
        y1 = data.height - marginOutside
        return((int(x0), int(y0), int(x1), int(y1)))
        
## check attributes
        
    # return True if the activity is in the user's favorites
    def checkIfFavorite(self):
        favorites = favoriteActivities.openFavoriteActivities()
        if favorites is not None and self.activityName in favorites:
            return True
        else:
            return False
        
    # return True if the activity's small tile is currently on screen
    def checkIfOnScreen(self, data):
        x0, y0, x1, y1 = self.getSmallTileCoordinates(data)
        self.onScreen = (y0 <= data.height) and (y1 >= data.toolbarHeight)
    
    # return True if the user has clicked inside the activity's current tile
    def clickInTile(self, data, eventX, eventY):
        if eventY < data.toolbarHeight: return False
        if self.smallTileIsClicked:
            x0, y0, x1, y1 = self.getBigTileCoordinates(data)
        else:
            x0, y0, x1, y1 = self.getSmallTileCoordinates(data)
        if x0 <= eventX <= x1:
            if y0 <= eventY <= y1:
                return True
        return False
    
## modify attributes
    
    # add or remove activity to/from the user's favorites
    def favorite(self):
        self.isFavorite = not self.isFavorite
        favoriteActivities.updateFavoriteActivities(self.activityName,
                                                    self.activityFeatures)
        rank.updateTagCount()
        
## draw tiles
        
    def drawSmallTile(self, data, canvas):
        # design attributes
        marginInside = data.width // 40
        # coordinates of tile corners
        x0, y0, x1, y1 = self.getSmallTileCoordinates(data)
        # fonts
        headingFontSize = int((x1 - x0) // 20)
        headingFont = design.fonts["tileText"] + " " + str(headingFontSize)
        contentsFontSize = int((x1 - x0) // 30)
        contentsFont = design.fonts["tileText"] + " " + str(contentsFontSize)
        # create tile
        canvas.create_rectangle(x0, y0, x1, y1, 
                                fill=design.colors["smallTile"], width=0)
        # create heading
        headingHeight = (y1 - y0) * (1/4)
        canvas.create_rectangle(x0, y0, x1, (y0 + headingHeight),
                                fill=design.colors["smallTileHeading"], width=0)
        # create heading text
        headingCutoff = int((x1 - x0) // 9)
        heading = self.activityName[:headingCutoff] + \
                  "..." * (len(self.activityName) > headingCutoff)
        canvas.create_text(((x0 + x1) / 2), (y0 + headingHeight / 2), 
                           anchor="center", font=headingFont,
                           fill=design.colors["tileText"], text=heading)
        # create contents
        if self.description is None: description = "Description not available."
        else:
            descriptionCutoff = int(((x1 - x0) - marginInside) * 
                                (y1 - y0) // (18 * contentsFontSize))
            description = self.description[:descriptionCutoff] + \
                          "..." * (len(self.description) > descriptionCutoff)
        canvas.create_text(((x0 + x1) / 2), ((y0 + headingHeight + y1) / 2),
                           anchor="center", font=contentsFont, 
                           fill=design.colors["tileText"], 
                           text=description, width=((x1 - x0) - marginInside))
                           
    def drawBigTile(self, data, canvas):
        # design attributes
        marginInside = data.width // 40
        # coordinates of tile corners
        x0, y0, x1, y1 = self.getBigTileCoordinates(data)
        tileHeight = y1 - y0
        # fonts
        headingFontSize = int((x1 - x0) // len(self.activityName))
        headingFont = design.fonts["tileText"] + " " + str(headingFontSize)
        contentsFontSize = int((x1 - x0) // 50)
        contentsFont = design.fonts["tileText"] + " " + str(contentsFontSize)
        # create tile
        canvas.create_rectangle(x0, y0, x1, y1, 
                                fill=design.colors["bigTile"], width=0)
        # create heading
        headingHeight = tileHeight * (1/4)
        canvas.create_rectangle(x0, y0, x1, (y0 + headingHeight),
                                fill=design.colors["bigTileHeading"], width=0)
        # create heading text
        heading = self.activityName
        canvas.create_text(((x0 + x1) / 2), (y0 + headingHeight / 2), 
                           anchor="center", font=headingFont,
                           fill=design.colors["tileText"], text=heading)
        # create contents
        canvas.create_text(((x0 + x1) / 2), ((y0 + headingHeight + y1) / 2),
                           anchor="center", font=contentsFont, 
                           fill=design.colors["tileText"], 
                           text=self.description,
                           width=((x1 - x0) - marginInside))
        # create favorite button
        favButtonColor = design.colors["bigTileFaveIcon"]
        if not self.isFavorite: favButtonColor = design.colors["filter"]
        self.favoriteButton.draw(data, canvas, x0, y0, x1, y1,
                                 color=favButtonColor, text="Favorite")