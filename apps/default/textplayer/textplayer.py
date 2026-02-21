from type.colors import Colors

from NodeSquad.modules.window import Window
class textplayer(Window):

    def readfile(self, filename):
        with open(filename, 'r') as file:
            text = file.readlines()
            text = [i[:-1] for i in text]
            self.ln = len(text)
        self.ui.art("text", text, 1, 0, attr = Colors.FXNormal, align = 0)
        #self.ui.textBox("text", text, 1, 0, height, width, align = 1)

        self.appname = filename.split('/')[-1]
        self.displayappname = self.appname.center(self.width, ' ')

        self.scrollpos = 0

        #self.oblen = min(height - 1, self.ln - self.scrollpos)

    def __init__(self, node, args = ''):
        #base
        self.node = node
        self.controller = node.controller
        self.height = node.height
        self.width = node.width


	# Input
        self.input_subscriptions = [self.controller.MouseEvents, self.controller.MouseWheelEvents]

        self.ui = self.node.ui

        self.appname = ''
        if args != '':
            self.readfile(args)
        else:
            self.ui.art("open", ["--------", "| open |", "--------"], self.width / 2 - 5, 3, attr = Colors.FXNormal)


    def draw(self, delta):
        if self.appname != '':
            self.node.appendStr(0, 0, self.displayappname, Colors.FXBold)

    def onresize(self, height, width):
        self.space = ' ' * width
        if self.appname != '':
            self.displayappname = self.appname.center(width, ' ')
            self.ui.resize("text", min(height + self.scrollpos, self.ln), width, type = "arts")
            #self.oblen = min(height - 1, self.ln)

    def scroll(self, id, delta):
        self.scrollpos = max(0, self.scrollpos + delta)
        self.ui.moveTo("text", 1 - self.scrollpos, 0)
