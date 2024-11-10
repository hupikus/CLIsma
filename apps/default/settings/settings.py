from apps.apphabit import apphabit
from type.colors import Colors
from .layouts import Layouts
class settings(apphabit):

    def start(self):
        #self.node.ui.art("icon1", ["----", "---", "--", "-"], 1, 0)
        #self.ui.clickableArt("icon1", self.submenu, 1, 0, ["-----  ", " --- ", "  -- ", "  -  "])
        #self.ui.slider("FPS", self.FPSlider_update, 5, 2, 24, 11)
        #self.ui.slider("FPS", self.FPSlider_update, 5, 2, 24, 11, railChar = '-', buttonChar = '*', buttonWidth = 5, railAttr = Colors.FXNormal, buttonAttr = Colors.FXNormal)
        #self.ui.textBox("tB", 'I want to introduce to you new UI element called "TextBox". It can make automatic line break for words longer than line', 6, 2, 8, 30, align = 1)

        #ui
        self.path = ["zero"]
        self.layout = "zero"

        self.state = Layouts(self, self.ui)

        self.state.loadState(self.layout)

        self.space = ' ' * self.width

    def __init__(self, id, node, controller, height, width, params):
        #base
        self.id = id
        self.node = node
        self.controller = controller
        self.height = height
        self.width = width

		#input
        self.input_subscriptions = [controller.MouseEvents, controller.KeyboardEvents]


        self.ui = self.node.ui


        self.start()


    def draw(self):
        for y in range(self.height):
            self.node.appendStr(y, 0, self.space)
        #self.node.appendStr(6, 0, str(*[self.ui.uis["lists"]]), Colors.FXReverse)
        #self.node.appendStr(0, 0, "Settings")

        #self.node.appendStr(1, 0, "Temportary settings")
        #self.node.appendStr(4, 0, "FPS limit")
        #self.node.appendStr(5, 27, self.FPSlider)

    def onresize(self, height, width):
        self.height = height
        self.width = width
        self.ui.resize("list", height, width, type = "lists")
        self.space = ' ' * self.width
        #self.ui.resize("tB", 0, round(width * 0.5))
    

    def submenu(self, name, button):
        if button == 0:
            self.path += [name]
            self.layout = name
            self.state.clearState()
            self.state.loadState(self.layout)
    

    def up(self, name, button):
        self.path = self.path[:-1]
        self.layout = self.path[-1]
        self.state.clearState()
        self.state.loadState(self.layout)
