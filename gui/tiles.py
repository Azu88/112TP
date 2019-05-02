####################################
# Activity Tile Class
####################################

import math
import webbrowser

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
        if self.description is not None:
            self.description = self.description.replace("\n\n", "\n")
        self.categories = activityFeatures["categories"]
        # drawing information
        self.favoriteButton = toolbar.FavoriteIcon("tile")
        self.gridIndex = gridIndex
        # drawing status
        self.smallTileIsClicked = False
        self.onScreen = True
        # data stored
        self.urlText = None
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
        
    # check if the user has clicked the activity's url and open webpage if so
    def clickInUrl(self, data, canvas, eventX, eventY):
        if self.urlText is None: return None
        x0, y0, x1, y1 = canvas.bbox(self.urlText)
        if x0 <= eventX <= x1:
            if y0 <= eventY <= y1:
                webbrowser.open(self.url)
    
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
        if self.description is None:
            description = "Description not available."
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
        headingFontSize = int((x1 - x0) // 
                             (5 * math.sqrt(len(self.activityName))))
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
            # description
        if self.description is None:
            description = "Description not available."
        else:
            descriptionCutoff = int(((x1 - x0) - 2 * marginInside) * 
                                (y1 - y0 - headingHeight) // (32 * contentsFontSize))
            description = self.description[:descriptionCutoff] + \
                          "..." * (len(self.description) > descriptionCutoff)
        canvas.create_text(((x0 + x1) / 2), ((y0 + headingHeight + y1) / 2),
                           anchor="center", font=contentsFont, 
                           fill=design.colors["tileText"], 
                           text=description,
                           width=((x1 - x0) - 2 * marginInside))
            # address
        if self.address is None or (
           self.address["streetAddress"] is None or self.address["city"] is None):
            address = "Address not available."
        else:
            address = self.address["streetAddress"] + "\n" + self.address["city"]
        canvas.create_text(((x0 + x1) / 4), ((y0 + headingHeight + y1) / 3),
                           anchor="center", font=contentsFont, 
                           fill=design.colors["tileText"], 
                           text=address, width=((x0 + x1) / 3))
            # distance
        if self.distance is None:
            distance = ""
        else:
            distance = "%.1f mi" % self.distance
        canvas.create_text(((x0 + x1) / 2), ((y0 + headingHeight + y1) / 3),
                           anchor="center", font=contentsFont, 
                           fill=design.colors["tileText"], 
                           text=distance)
            # price
        if self.priceRange is None:
            price = "Price not available."
        else:
            price = self.priceRange
        canvas.create_text((3 * (x0 + x1) / 4), ((y0 + headingHeight + y1) / 3),
                           anchor="center", font=contentsFont, 
                           fill=design.colors["tileText"], 
                           text=price)
            # url
        if self.url is None:
            url = "URL not available."
            urlFont = contentsFont
            canvas.create_text(((x0 + x1) / 2), (2 * (y0 + headingHeight + y1) / 3),
                               anchor="center", font=urlFont, 
                               fill=design.colors["tileText"], text=url)
        else:
            url = self.url
            urlFontSize = int((x1 - x0) // (8 * math.sqrt(len(self.url))))
            urlFont = design.fonts["tileText"] + " " + str(urlFontSize)
            self.urlText = canvas.create_text(((x0 + x1) / 2), 
                                              (2 * (y0 + headingHeight + y1) / 3),
                                              anchor="center", font=urlFont, 
                                              fill=design.colors["tileText"], 
                                              activefill=design.colors["urlHover"],
                                              text=url)
        # create favorite button
        if self.isFavorite:
            favButtonColor = design.colors["bigTileFaveIcon"]
        else:
            favButtonColor = design.colors["bigTile"]
        self.favoriteButton.draw(data, canvas, color=favButtonColor)