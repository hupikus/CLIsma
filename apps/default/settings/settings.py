from apps.apphabit import apphabit
from worldglobals import worldglobals
from loghandler import Loghandler
class settings(apphabit):

    def start(self):
        #self.node.ui.art("icon1", ["----", "---", "--", "-"], 1, 0)
        #self.ui.clickableArt("icon1", self.submenu, 1, 0, ["-----  ", " --- ", "  -- ", "  -  "])
        self.ui.slider("FPS", self.FPSlider_update, 5, 2, 24, 11)

    def __init__(self, id, node, controller, height, width, params):
        #base
        self.id = id
        self.node = node
        self.controller = controller
        self.height = height
        self.width = width


        self.preferred_height = 20
        self.preferred_width = 60

		#input
        self.input_subscriptions = [controller.MouseEvents, controller.KeyboardEvents]


        self.ui = self.node.ui

        self.FPSlider = "60"

        self.start()


    def draw(self):
        self.node.appendStr(0, 0, "Settings")

        self.node.appendStr(1, 0, "Temportary settings")
        self.node.appendStr(4, 0, "FPS limit")
        self.node.appendStr(5, 27, self.FPSlider)

    def FPSlider_update(self, val):
        self.FPSlider = (val + 1) * 5
        worldglobals.framerate = self.FPSlider
        worldglobals.framedelta = 1 / self.FPSlider
        self.FPSlider = str(self.FPSlider)
        Loghandler.Log(f"FPS changed to {self.FPSlider}")
