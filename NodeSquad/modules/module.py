class Module:
    # Basics

    def __init__(self, node):
        self.node = node
        self.height = node.height
        self.width = node.width
        self.controller = node.controller

    def draw(self, delta):
        pass

    def process(self, delta):
        pass

    def input(self, delta, controller):
        pass

    # Node events

    def resize(self, height, width):
        self.height = height
        self.width = width

    def collapse(self, collapse):
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
