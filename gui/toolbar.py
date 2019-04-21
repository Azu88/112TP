from gui import design

class Filter(object):
    
    def __init__(self, name, options):
        self.name = name # name of filter ( "name" )
        self.options = options # dropdown options ( [option1, option2, ...] )
        self.selection = None
        self.clicked = False
        
    def clicked(self, x, y):
        pass
        
    def draw(self, data, canvas, filterIndex):
        # design attributes
        numFilters = len(data.filters)
        marginInside = 10
        marginOutside = data.toolbarHeight / 5
        buttonWidth = 100
        # coordinates of button corners
        x0 = marginOutside * (filterIndex + 1) + buttonWidth * filterIndex
        y0 = marginOutside
        x1 = marginOutside * (filterIndex + 1) + buttonWidth * (filterIndex + 1)
        y1 = data.toolbarHeight - marginOutside
        # create filter button
        canvas.create_rectangle(x0, y0, x1, y1, 
                                fill=design.colors["filter"], width=0)
        # create filter text
        textX = x0 + (x1 - x0) / 2
        textY = y0 + (y1 - y0) / 2
        font = design.fonts["filterText"] + " " + str(10)
        canvas.create_text(textX, textY, anchor="center", font=font, 
                           fill=design.colors["filterText"], text=self.name)
    
class Icon(object):
    def __init__(self):
        pass
        
    def draw(self, data, canvas):
        pass