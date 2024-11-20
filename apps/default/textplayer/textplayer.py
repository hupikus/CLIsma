from type.colors import Colors
from apps.apphabit import apphabit

class textplayer(apphabit):
    
    def __init__(self, id, node, controller, height, width, params):
        #base
        self.id = id
        self.node = node

	    #input
        self.input_subscriptions = [controller.MouseEvents, controller.MouseWheelEvents]

        self.ui = self.node.ui
        file = open(params)
        text = file.readlines()
        text = [i[:-1] for i in text]
        self.ln = len(text)
        file.close()
        self.ui.art("text", text, 1, 0, attr = Colors.FXNormal, align = 0)
        #self.ui.textBox("text", text, 1, 0, height, width, align = 1)

        self.appname = params.split('/')[-1]
        self.displayappname = self.appname.center(width, ' ')

        self.scrollpos = 0
        
        #self.oblen = min(height - 1, self.ln - self.scrollpos)
    
    def draw(self):
        self.node.appendStr(0, 0, self.displayappname, Colors.FXBold)

    def onresize(self, height, width):
        self.space = ' ' * width
        self.displayappname = self.appname.center(width, ' ')
        self.ui.resize("text", height + self.scrollpos, width, type = "arts")
        #self.oblen = min(height - 1, self.ln)
    
    def scroll(self, id, delta):
        self.scrollpos = max(0, self.scrollpos + delta)
        self.ui.moveTo("text", 1 - self.scrollpos, 0)
