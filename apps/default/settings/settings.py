from type.colors import Colors
from .layouts import Layouts

from NodeSquad.modules.window import Window
class settings(Window):

    def start(self):
        #self.node.ui.art("icon1", ["----", "---", "--", "-"], 1, 0)
        #self.ui.clickableArt("icon1", self.submenu, 1, 0, ["-----  ", " --- ", "  -- ", "  -  "])
        #self.ui.slider("FPS", self.FPSlider_update, 5, 2, 24, 11)
        #self.ui.slider("FPS", self.FPSlider_update, 5, 2, 24, 11, railChar = '-', buttonChar = '*', buttonWidth = 5, railAttr = Colors.FXNormal, buttonAttr = Colors.FXNormal)

        #ui
        self.path = ["zero"]
        self.layout = "zero"

        self.state = Layouts(self, self.ui)

        self.state.loadState(self.layout)

        self.space = ' ' * self.width

    def __init__(self, node, args = ''):
        # Base
        self.node = node
        self.controller = node.controller
        self.height = node.height
        self.width = node.width

	# Input
        self.input_subscriptions = [
            self.controller.MouseEvents,
            self.controller.KeyboardEvents
        ]


        self.ui = node.ui


        self.start()


    def draw(self, delta):
        for y in range(self.height):
            self.node.appendStr(y, 0, self.space)
        #self.node.appendStr(6, 0, str(*[self.ui.uis["lists"]]), Colors.FXReverse)
        #self.node.appendStr(0, 0, "Settings")

        #self.node.appendStr(1, 0, "Temportary settings")
        #self.node.appendStr(4, 0, "FPS limit")
        #self.node.appendStr(5, 27, self.FPSlider)

    def click(self, device_id, button, y, x):
        if button == 1:
            if self.layout != "zero":
                self.up('', 0, 0)

    def resize(self, height, width):
        self.height = height
        self.width = width
        self.ui.resize("list", height, width, type = "lists")
        self.space = ' ' * self.width
        #self.ui.resize("tB", 0, round(width * 0.5))


    def submenu(self, name, button, device_id):
        if button == 0:
            self.path += [name]
            self.layout = name
            self.state.clearState()
            self.state.loadState(self.layout)


    def up(self, name, button, device_id):
        self.path = self.path[:-1]
        self.layout = self.path[-1]
        self.state.clearState()
        self.state.loadState(self.layout)
