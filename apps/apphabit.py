class apphabit:

    preferred_height = 9
    preferred_width = 45

    #ABCS

    def __init__(self, id, node, controller, height, width, params):
        self.height = height
        self.width = width
        self.node = node
        self.controller = controller
        self.ui = self.node.ui

    def draw(self, delta):
        self.node.clear()

    def process(self, delta):
        pass

    def mouse(self, delta, controller):
        pass

    #NODE EVENTS

    def onresize(self, height, width):
        self.height = height
        self.width = width

    def oncollapse(self, collapse):
        pass

    def abort(self):
        pass

    #INPUT

    def click(self, device_id, button, y, x):
        pass

    def clickEnd(self, device_id, button, y, x):
        pass

    def drag(self, id, button, stage, y, x):
        pass

    def scroll(self, id, delta):
        pass

    def keyPress(self, key):
        pass

    def keyRelease(self, key):
        pass

    def midikeyPress(self, note, pressure):
        pass

    def midikeyRelease(self, note):
        pass
