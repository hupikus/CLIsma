class apphabit:

    preferred_height = 9
    preferred_width = 45

    # Basics

    def __init__(self, id, node, controller, height, width, params = None):
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

    # Node events

    def onresize(self, height, width):
        self.height = height
        self.width = width

    def oncollapse(self, collapse):
        pass

    def abort(self):
        pass


    # Input

    def press(self, devive_id, button, y, x):
        pass

    def click(self, device_id, button, y, x):
        pass

    def drag(self, device_id, button, stage, y, x):
        pass

    def scroll(self, device_id, delta):
        pass

    def keyPress(self, key):
        pass

    def keyRelease(self, key):
        pass

    def keyType(self, key):
        pass

    def midikeyPress(self, note, pressure):
        pass

    def midikeyRelease(self, note):
        pass
