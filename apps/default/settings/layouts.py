from loghandler import Loghandler
from worldglobals import worldglobals

from fastconfig import Wmconfig

from singletons import Singletons
class Layouts:

    def __init__(self, settings, ui):
        self.sett = settings
        self.ui = ui
        self.path = "zero"

        self.wm = Singletons.Wm

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
                #FPS slider
                self.ui.slider("FPS", self.FPSlider_update, 0, 0, 24, 11)
                self.ui.textLine("FPSTitle", "Set Framerate", 0, 0)

                self.ui.textLine("FPSText", "60", 0, 0)

                #process slider
                self.ui.slider("TICK", self.TICKlider_update, 0, 0, 44, 11)
                self.ui.textLine("TICKTitle", "Set Tickrate", 0, 0)

                self.ui.textLine("TICKText", "100", 0, 0)

                elements = (
                "FPSTitle", (True, "space", 2, 2), (True, "newline", 1), "FPSText", (True, "glue", 1), "FPS",
                (True, "newline", 1), "TICKTitle", (True, "space", 2, 2), (True, "newline", 1), "TICKText", (True, "glue", 1), "TICK"
                )

                self.ui.list("list", elements, 3, 0, self.sett.height, self.sett.width, 1, 2, fitAll = True, vertical = False)
            elif path == "customization":

                #set mouse trail length
                self.ui.slider("TRAIL", self.Trailider_update, 0, 0, 18, 2)
                self.ui.textLine("TRAitle", "Set mouse cursor trail length", 0, 0)

                self.ui.textLine("TRAILext", "100", 0, 0)

                elements = (
                "TRAitle", (True, "newline", 1), "TRAILext", (True, "glue", 1), "TRAIL"
                )

                self.ui.list("list", elements, 3, 0, self.sett.height, self.sett.width, 1, 2, fitAll = True, vertical = False)

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
    
    def TICKlider_update(self, val):
        
        if val < 4:
            self.TickSlider = val + 1
        else:
            self.TickSlider = (val - 3) * 5
        worldglobals.processrate = self.TickSlider
        worldglobals.processdelta = 1 / self.TickSlider
        self.TickSlider = str(self.TickSlider)
        self.ui.setText("TICKText", self.TickSlider, type = "txts")
        Loghandler.Log(f"Tickrate changed to {self.TickSlider}")
    
    def Trailider_update(self, val):
        Wmconfig.setTrailLength(val)
        val = str(val)
        self.ui.setText("TRAILext", val, type = "txts")
        Loghandler.Log(f"Trail length changed to {val}")
    
            