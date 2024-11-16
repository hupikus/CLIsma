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
        text = file.read()
        file.close()
        self.ui.textBox("text", text, 0, 0, height, width, align = 1)

        self.scrollpos = 0
    
    def onresize(self, height, width):
        self.space = ' ' * width
        self.ui.resize("text", height + self.scrollpos, width)
    
    def scroll(self, id, delta):
        self.scrollpos = max(0, self.scrollpos + delta)
        self.ui.moveTo("text", -self.scrollpos, 0)
