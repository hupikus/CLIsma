from loghandler import Loghandler
from worldglobals import worldglobals


class Layouts:

    def __init__(self, settings, ui):
        self.sett = settings
        self.ui = ui
        self.path = "zero"



        self.FPSlider = "60"

    def loadState(self, path):
        
        if path == "zero":
            self.ui.clickableArt("performance", self.sett.submenu, 0, 0, ["_____", "|  /|", "| o |", "I---I", " Performance "], align = 1)
            self.ui.clickableArt("input", self.sett.submenu, 0, 0, ["  \\  ", "/-/-\\", "| ! |", "\\___/", "    Input    "], align = 1)
            self.ui.clickableArt("customization", self.sett.submenu, 0, 0, ["  /\\  ", " _||_ ", "| || |", "|-\\/-|", "Customization"], align = 1)

            self.ui.list("list", ("input", "performance", "customization"), 0, 0, self.sett.height, self.sett.width, 1, 2, fitAll = True, vertical = False)

            self.ui.remove("back", type = "tapArts")

        else:
            if self.path == "zero":
                self.ui.clickableArt("back", self.sett.up, 0, 0, ["Back"])

            if path == "performance":
                self.ui.slider("FPS", self.FPSlider_update, 0, 0, 24, 11)
                self.ui.textLine("FPSTitle", "Set Framerate", 0, 0)

                self.ui.textLine("FPSText", "60", 0, 0)

                self.ui.list("list", ("FPSTitle", (True, "space", 2, 2), (True, "newline", 1), "FPS", (True, "glue", 1), "FPSText"), 3, 0, self.sett.height, self.sett.width, 1, 2, fitAll = True, vertical = False)
        self.path = path


    def clearState(self):
        self.ui.removeRecursive("list")
    
    #UI events

    def FPSlider_update(self, val):
        self.FPSlider = (val + 1) * 5
        worldglobals.framerate = self.FPSlider
        worldglobals.framedelta = 1 / self.FPSlider
        self.FPSlider = str(self.FPSlider)
        self.ui.setText("FPSText", self.FPSlider, type = "txts")
        Loghandler.Log(f"FPS changed to {self.FPSlider}")
    
            