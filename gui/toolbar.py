####################################
# Toolbar Element Classes
####################################

import math

from gui import design

####################################

class Filter(object):
    
    def __init__(self, name, options, filterIndex):
        # filter information
        self.name = name
        self.options = options
        # drawing information
        self.filterIndex = filterIndex
        # drawing status
        self.isClicked = False
        # data stored
        self.selection = None
        
## calculate button coordinates
        
    # calculate corner coordinates of the filter button
    def getFilterCoordinates(self, data):
        marginOutside = data.toolbarHeight // 5
        filterIndex = self.filterIndex
        buttonWidth = data.width // 8
        x0 = marginOutside * (filterIndex + 1) + buttonWidth * filterIndex
        y0 = marginOutside
        x1 = marginOutside * (filterIndex + 1) + buttonWidth * (filterIndex + 1)
        y1 = data.toolbarHeight - marginOutside
        return ((x0, y0, x1, y1))
        
    # calculate corner coordinates of the given filter option
    def getOptionCoordinates(self, data, i):
        x0, y0, x1, y1 = self.getFilterCoordinates(data)
        optionX0 = x0
        optionY0 = y1 + (y1 - y0) * (i)
        optionX1 = x1
        optionY1 = y1 + (y1 - y0) * (i + 1)
        return ((optionX0, optionY0, optionX1, optionY1))
        
## check attributes
        
    # return True if the user has clicked inside the filter button
    def clickInFilter(self, data, eventX, eventY):
        x0, y0, x1, y1 = self.getFilterCoordinates(data)
        if x0 <= eventX <= x1:
            if y0 <= eventY <= y1:
                return True
        return False
    
    # return True if the user has clicked inside the given filter option
    def clickInOption(self, data, eventX, eventY, i):
        optionX0, optionY0, optionX1, optionY1 = self.getOptionCoordinates(data, i)
        if optionX0 <= eventX <= optionX1:
            if optionY0 <= eventY <= optionY1:
                return True
        return False
    
## draw buttons
    
    def drawDropdown(self, data, canvas):
        # coordinates of button corners
        x0, y0, x1, y1 = self.getFilterCoordinates(data)
        # fonts
        fontSize = int(data.width // 80)
        font = design.fonts["filterText"] + " " + str(fontSize)
        # create options
        for i in range(len(self.options)):
            option = self.options[i]
            # design attributes
            color = design.colors["filterDropdown"]
            if option == self.selection:
                color = design.colors["filterSelected"]
            # coordinates of option corners
            optionX0, optionY0, optionX1, optionY1 = self.getOptionCoordinates(data, i)
            # create box
            canvas.create_rectangle(optionX0, optionY0, optionX1, optionY1,
                                    fill=color, width=0,
                                    activefill=design.colors["filterHover"])
            # create label
            label = str(option)
            if self.name == "Distance":
                label += " mi"
            canvas.create_text((optionX0 + (x1 - x0) / 2),
                               (optionY0 + (y1 - y0) / 2), 
                                anchor="center", font=font, 
                                fill=design.colors["filterText"], text=label)
        
    def draw(self, data, canvas):
        # design attributes
        marginInside = data.width // 80
        # coordinates of button corners
        x0, y0, x1, y1 = self.getFilterCoordinates(data)
        # fonts
        fontSize = int(data.width // 80)
        font = design.fonts["filterText"] + " " + str(fontSize)
        # create button
        canvas.create_rectangle(x0, y0, x1, y1, 
                                fill=design.colors["filter"], width=0)
        # create text
        canvas.create_text(((x0 + x1) / 2), ((y0 + y1) / 2),
                           anchor="center", font=font, 
                           fill=design.colors["filterText"], text=self.name)
        # draw dropdown options
        if self.isClicked:
            self.drawDropdown(data, canvas)

####################################

class FavoriteIcon(object):
    
    def __init__(self, mode):
        self.name = "Favorites"
        self.isClicked = False
        self.mode = mode
    
    # given coordinates of container, calculate corner coordinates of button
    def getCoordinates(self, data):
        if self.mode == "toolbar":
            x0, y0, x1, y1 = 0, 0, data.width, data.toolbarHeight
        elif self.mode == "tile":
            marginOutside = data.width // 20
            x0 = marginOutside
            y0 = data.toolbarHeight + marginOutside
            x1 = data.width - marginOutside
            y1 = data.toolbarHeight + marginOutside + (
                 (data.height - 2 * marginOutside - data.toolbarHeight) / 4)
        marginInside = data.toolbarHeight // 5
        buttonWidth = data.toolbarHeight - 2 * marginInside
        buttonX0 = x1 - marginInside - buttonWidth
        buttonY0 = (y0 + y1 - buttonWidth) / 2
        buttonX1 = x1 - marginInside
        buttonY1 = (y0 + y1 + buttonWidth) / 2
        return(buttonX0, buttonY0, buttonX1, buttonY1)
    
    # return True if the user has clicked inside the button's bounding box
    def clickInButton(self, data, eventX, eventY):
        buttonX0, buttonY0, buttonX1, buttonY1 = self.getCoordinates(data)
        if buttonX0 <= eventX <= buttonX1:
            if buttonY0 <= eventY <= buttonY1:
                return True
        return False
    
    # draw a 5-point star in the given bounding box
    def drawStar(self, canvas, x0, y0, x1, y1, color):
        l = (y1 - y0) * math.sqrt(1 + (math.tan(math.pi / 10)) ** 2)
        lTip = (y1 - y0 - (l * math.cos(math.pi / (10/3)))) / math.cos(math.pi / 10)
        p1x, p1y = ((x0 + x1) / 2), (y0)
        p2x, p2y = ((x0 + x1) / 2 - lTip * math.sin(math.pi / 10)), \
                   (y0 + lTip * math.cos(math.pi / 10))
        p3x, p3y = (x0), (y1 - l * math.cos(math.pi / (10/3)))
        p4x, p4y = ((x0 + x1) / 2 - lTip * math.cos(math.pi / (20/3))
                                  + lTip * math.sin(math.pi / (20/3))), \
                   (y1 - lTip * math.cos(math.pi / 10))
        p5x, p5y = ((x0 + x1) / 2 - l * math.sin(math.pi / 10)), (y1)
        p6x, p6y = ((x0 + x1) / 2), (y1 - lTip * math.sin(math.pi / (20/3)))
        p7x, p7y = ((x0 + x1) / 2 + l * math.sin(math.pi / 10)), (y1)
        p8x, p8y = ((x0 + x1) / 2 + lTip * math.cos(math.pi / (20/3))
                                  - lTip * math.sin(math.pi / (20/3))), \
                   (y1 - lTip * math.cos(math.pi / 10))
        p9x, p9y = ((x1), (y1 - l * math.cos(math.pi / (10/3))))
        p10x, p10y = ((x0 + x1) / 2 + lTip * math.sin(math.pi / 10)), \
                     (y0 + lTip * math.cos(math.pi / 10))
        if self.mode == "toolbar":
            if self.isClicked:
                color = design.colors["filterSelected"]
            else:
                color = design.colors["filter"]
            canvas.create_polygon(p1x, p1y, p2x, p2y, p3x, p3y, p4x, p4y, p5x, p5y,
                                  p6x, p6y, p7x, p7y, p8x, p8y, p9x, p9y, p10x, p10y,
                                  fill=color, activefill=design.colors["filterHover"])
        elif self.mode == "tile":
            canvas.create_polygon(p1x, p1y, p2x, p2y, p3x, p3y, p4x, p4y, p5x, p5y,
                                  p6x, p6y, p7x, p7y, p8x, p8y, p9x, p9y, p10x, p10y,
                                  fill=color)
        
    def draw(self, data, canvas, color=None):
        # design attributes
        marginInside = 10
        # coordinates of button corners
        buttonX0, buttonY0, buttonX1, buttonY1 = self.getCoordinates(data)
        # create button
        self.drawStar(canvas, buttonX0, buttonY0, buttonX1, buttonY1, color)