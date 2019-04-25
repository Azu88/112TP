from gui import design
from gui import toolbar
from data import favoriteActivities

class Tile(object):
    marginOutside = 20
    
    def __init__(self, activityName, activityFeatures, gridIndex):
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
        self.gridIndex = gridIndex
        self.smallTileIsClicked = False
        self.bigTileIsClicked = False
        self.favoriteButton = toolbar.FavoriteIcon()
        self.isFavorite = self.checkIfFavorite()
        
    def checkIfFavorite(self):
        favorites = favoriteActivities.favoriteActivities
        if favorites is not None and self.activityName in favorites:
            return True
        else:
            return False
        
    def getSmallTileCoordinates(self, data):
        marginOutside = Tile.marginOutside
        gridRows, gridCols = data.tileGrid["rows"], data.tileGrid["cols"]
        tileWidth = (data.width - marginOutside * (gridCols + 1)) / gridCols
        tileHeight = (data.height - data.toolbarHeight - (
                                    marginOutside * (gridRows + 1))) / gridRows
        tileRow, tileCol = self.gridIndex // gridCols, self.gridIndex % gridCols
        x0 = marginOutside * (tileCol + 1) + tileWidth * tileCol 
        y0 = - data.scrollY + data.toolbarHeight + (
                    marginOutside * (tileRow + 1) + tileHeight * tileRow)
        x1 = marginOutside * (tileCol + 1) + tileWidth * (tileCol + 1)
        y1 = - data.scrollY + data.toolbarHeight + (
                    marginOutside * (tileRow + 1) + tileHeight * (tileRow + 1))
        return((x0, y0, x1, y1))
        
    def getBigTileCoordinates(self, data):
        marginOutside = 2 * Tile.marginOutside
        x0 = marginOutside
        y0 = data.toolbarHeight + marginOutside
        x1 = data.width - marginOutside
        y1 = data.height - marginOutside
        return((x0, y0, x1, y1))
        
    def clickInTile(self, data, eventX, eventY):
        if self.smallTileIsClicked:
            x0, y0, x1, y1 = self.getBigTileCoordinates(data)
        else:
            x0, y0, x1, y1 = self.getSmallTileCoordinates(data)
        if x0 <= eventX <= x1:
            if y0 <= eventY <= y1:
                return True
        return False
    
    def favorite(self):
        self.isFavorite = not self.isFavorite
        favoriteActivities.updateFavoriteActivities(self.activityName,
                                                    self.activityFeatures)
        
    def formatText(self, text, x0, x1, y0, y1, fontSize):
        formattedText = ""
        width = (x1 - x0) // (fontSize // 2)
        height = (y1 - y0) // fontSize
        originalText = text[:width * height].strip() + "..."
        # from hw3
        originalText += " "
        for line in range(height):
            i = width
            while i > 0:
                if 0 <= i < len(originalText) and originalText[i] == " ":
                    formattedText += originalText[0:i] + "\n"
                    originalText = originalText[i+1:]
                    i = width
                    if " " not in originalText:
                        break
                else:
                    i -= 1
        return formattedText
        
    def drawSmallTile(self, data, canvas):
        # design attributes
        font = design.fonts["tileText"] + " " + str(10)
        # coordinates of tile corners
        x0, y0, x1, y1 = self.getSmallTileCoordinates(data)
        tileWidth = x1 - x0
        tileHeight = y1 - y0
        # create tile
        canvas.create_rectangle(x0, y0, x1, y1, 
                                fill=design.colors["smallTile"], width=0)
        # create heading
        headingHeight = tileHeight * (1/4)
        headingX0 = int(x0)
        headingY0 = int(y0)
        headingX1 = int(x1)
        headingY1 = int(y0 + headingHeight)
        canvas.create_rectangle(headingX0, headingY0, headingX1, headingY1,
                                fill=design.colors["smallTileHeading"], width=0)
        title = self.activityName
        if len(title) > 25:
            title = title[:25] + "..."
        titleFontSize = int(tileWidth // 20)
        titleFont = design.fonts["tileText"] + " " + str(titleFontSize)
        canvas.create_text(headingX0 + (headingX1 - headingX0) / 2, 
                           headingY0 + (headingY1 - headingY0) / 2, 
                           anchor="center", font=titleFont,
                           fill=design.colors["tileText"],
                           text=title)
        # create contents
        contentsX0 = int(x0)
        contentsY0 = int(headingY1)
        contentsX1 = int(x1)
        contentsY1 = int(y1)
        contentsFontSize = int(tileWidth // 30)
        contentsFont = design.fonts["tileText"] + " " + str(contentsFontSize)
        description = self.description
        if description is None:
            description = "Description not available."
        canvas.create_text(contentsX0 + (contentsX1 - contentsX0) / 2, 
                           contentsY0 + (contentsY1 - contentsY0) / 2,
                           anchor="center", font=contentsFont, 
                           fill=design.colors["tileText"], 
                           text=self.formatText(description,
                                                contentsX0, contentsY0,
                                                contentsX1, contentsY1,
                                                contentsFontSize))
                                                
    def drawBigTile(self, data, canvas):
        # create tile
        x0, y0, x1, y1 = self.getBigTileCoordinates(data)
        canvas.create_rectangle(x0, y0, x1, y1, 
                                fill=design.colors["bigTile"], width=0)
        # create heading
        tileWidth = x1 - x0
        tileHeight = y1 - y0
        headingHeight = tileHeight * (1/4)
        headingX0 = int(x0)
        headingY0 = int(y0)
        headingX1 = int(x1)
        headingY1 = int(y0 + headingHeight)
        canvas.create_rectangle(headingX0, headingY0, headingX1, headingY1,
                                fill=design.colors["bigTileHeading"], width=0)
        title = self.activityName
        if len(title) > 25:
            title = title[:25] + "..."
        titleFontSize = int(tileWidth // 20)
        titleFont = design.fonts["tileText"] + " " + str(titleFontSize)
        canvas.create_text(headingX0 + (headingX1 - headingX0) / 2, 
                           headingY0 + (headingY1 - headingY0) / 2, 
                           anchor="center", font=titleFont,
                           fill=design.colors["tileText"],
                           text=title)
        favButtonColor = design.colors["bigTileFaveIcon"]
        if not self.isFavorite: favButtonColor = design.colors["filter"]
        self.favoriteButton.draw(data, canvas, x0, y0, x1, y1,
                                 color=favButtonColor,
                                 text="Favorite")