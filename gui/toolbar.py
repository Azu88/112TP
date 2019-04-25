from gui import design

class Filter(object):
    
    def __init__(self, name, options, filterIndex):
        self.name = name # name of filter ( "name" )
        self.options = options # dropdown options ( [option1, option2, ...] )
        self.filterIndex = filterIndex
        self.selection = None
        self.isClicked = False
        
    def clickInFilter(self, data, eventX, eventY):
        x0, y0, x1, y1 = self.getFilterCoordinates(data)
        if x0 <= eventX <= x1:
            if y0 <= eventY <= y1:
                return True
        return False
        
    def clickInOption(self, data, eventX, eventY, i):
        optionX0, optionY0, optionX1, optionY1 = self.getOptionCoordinates(data, i)
        if optionX0 <= eventX <= optionX1:
            if optionY0 <= eventY <= optionY1:
                return True
        return False
    
    def getFilterCoordinates(self, data):
        marginOutside = data.toolbarHeight / 5
        filterIndex = self.filterIndex
        buttonWidth = 100
        x0 = marginOutside * (filterIndex + 1) + buttonWidth * filterIndex
        y0 = marginOutside
        x1 = marginOutside * (filterIndex + 1) + buttonWidth * (filterIndex + 1)
        y1 = data.toolbarHeight - marginOutside
        return ((x0, y0, x1, y1))
        
    def getOptionCoordinates(self, data, i):
        x0, y0, x1, y1 = self.getFilterCoordinates(data)
        buttonWidth = x1 - x0
        buttonHeight = y1 - y0
        optionX0 = x0
        optionY0 = y1 + buttonHeight * (i)
        optionX1 = x1
        optionY1 = y1 + buttonHeight * (i + 1)
        return ((optionX0, optionY0, optionX1, optionY1))
    
    def drawDropdown(self, data, canvas):
        x0, y0, x1, y1 = self.getFilterCoordinates(data)
        buttonWidth = x1 - x0
        buttonHeight = y1 - y0
        for i in range(len(self.options)):
            option = self.options[i]
            optionX0, optionY0, optionX1, optionY1 = self.getOptionCoordinates(data, i)
            canvas.create_rectangle(optionX0, optionY0, optionX1, optionY1,
                                    fill=design.colors["filterDropdown"],
                                    width=1)
            textX = optionX0 + buttonWidth / 2
            textY = optionY0 + buttonHeight / 2
            font = design.fonts["filterText"] + " " + str(10)
            canvas.create_text(textX, textY, anchor="center", font=font, 
                           fill=design.colors["filterText"], text=option)
        
    def draw(self, data, canvas):
        # design attributes
        numFilters = len(data.filters)
        marginInside = 10
        buttonWidth = 100
        # coordinates of button corners
        x0, y0, x1, y1 = self.getFilterCoordinates(data)
        # create filter button
        canvas.create_rectangle(x0, y0, x1, y1, 
                                fill=design.colors["filter"], width=1)
        # create filter text
        textX = x0 + (x1 - x0) / 2
        textY = y0 + (y1 - y0) / 2
        font = design.fonts["filterText"] + " " + str(10)
        canvas.create_text(textX, textY, anchor="center", font=font, 
                           fill=design.colors["filterText"], text=self.name)
        # draw dropdown
        if self.isClicked:
            self.drawDropdown(data, canvas)
    
class FavoriteIcon(object):
    def __init__(self):
        self.name = "Favorites"
        self.isClicked = False
        
    def getCoordinates(self, data, x0, y0, x1, y1): # takes coordinates of container
        marginOutside = data.toolbarHeight / 5
        buttonWidth = 100
        buttonX0 = x1 - marginOutside - buttonWidth
        buttonY0 = y0 + marginOutside
        buttonX1 = x1 - marginOutside
        buttonY1 = y0 + data.toolbarHeight - marginOutside
        return(buttonX0, buttonY0, buttonX1, buttonY1)
        
    def clickInButton(self, data, eventX, eventY, x0, y0, x1, y1):
        buttonX0, buttonY0, buttonX1, buttonY1 = self.getCoordinates(data, x0, y0, x1, y1)
        if buttonX0 <= eventX <= buttonX1:
            if buttonY0 <= eventY <= buttonY1:
                return True
        return False
        
    def draw(self, data, canvas, x0, y0, x1, y1, color=design.colors["filter"], text=None):
        if text is None: text = self.name
        # design attributes
        marginInside = 10
        # coordinates of button corners
        buttonX0, buttonY0, buttonX1, buttonY1 = self.getCoordinates(data, x0, y0, x1, y1)
        # create filter button
        canvas.create_rectangle(buttonX0, buttonY0, buttonX1, buttonY1, 
                                fill=color, width=1)
        # create filter text
        textX = buttonX0 + (buttonX1 - buttonX0) / 2
        textY = buttonY0 + (buttonY1 - buttonY0) / 2
        font = design.fonts["filterText"] + " " + str(10)
        canvas.create_text(textX, textY, anchor="center", font=font, 
                           fill=design.colors["filterText"], text=text)