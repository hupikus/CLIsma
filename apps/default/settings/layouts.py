from integration.loghandler import Loghandler
from worldglobals import worldglobals
from type.colors import Colors

from fastconfig import Wmconfig

from singletons import Singletons
class Layouts:

    def __init__(self, settings, ui):
        self.sett = settings
        self.ui = ui
        self.path = "zero"

        self.wm = Singletons.Wm

    def loadState(self, path):
        ui = self.ui
        newline = (True, "newline", 1)
        if path == "zero":
            ui.clickableArt("performance", self.sett.submenu, 0, 0, ["_____", "|  /|", "| o |", "I---I", " Performance "], align = 1)
            ui.clickableArt("input", self.sett.submenu, 0, 0, ["  \\  ", "/-/-\\", "| ! |", "\\___/", "    Input    "], align = 1)
            ui.clickableArt("customization", self.sett.submenu, 0, 0, ["  /\\  ", " _||_ ", "| || |", "|-\\/-|", "Customization"], align = 1)

            ui.list("list", ("input", "performance", "customization"), 0, 0, self.sett.height, self.sett.width, 1, 2, fitAll = True, vertical = False)

            ui.remove("back", type = "tapArts")

        else:
            if self.path == "zero":
                ui.clickableArt("back", self.sett.up, 0, 0, ["Back"])

            if path == "performance":
                #FPS slider
                ui.slider("FPS", self.FPSlider_update, 0, 0, 30, (5 // worldglobals.framerate) - 1)
                ui.textLine("FPSTitle", "Set Framerate", 0, 0)

                ui.textLine("FPSText", str(worldglobals.framerate), 0, 0)

                #process slider
                if worldglobals.processrate < 5:
                    rate = worldglobals.processrate - 1
                else:
                    rate = (worldglobals.processrate // 5) + 3
                ui.slider("TICK", self.TICKlider_update, 0, 0, 44, rate)
                ui.textLine("TICKTitle", "Set Tickrate", 0, 0)

                ui.textLine("TICKText", str(worldglobals.processrate), 0, 0)

                elements = (
                "FPSTitle", (True, "space", 2, 2), newline, "FPSText", (True, "glue", 1), "FPS",
                newline, "TICKTitle", (True, "space", 2, 2), newline, "TICKText", (True, "glue", 1), "TICK"
                )

                ui.list("list", elements, 3, 0, self.sett.height, self.sett.width, 1, 2, fitAll = True, vertical = False)

            elif path == "customization":

                #set mouse trail length
                ui.slider("TRAIL", self.trailider_update, 0, 0, 18, Wmconfig.wm.trailength)
                ui.textLine("TRAitle", "Set mouse cursor trail length", 0, 0)

                ui.textLine("TRAILext", str(Wmconfig.wm.trailength), 0, 0)

                #cursor color
                cursorColor = ()
                if Colors.colorPosibility:
                    ui.textLine("CursorColorTitle", "Cursor color", 0, 0)
                    txt = ["   " for i in (0, 0)]
                    for i in range(7):
                        ui.clickableArt("color" + str(i), self.set_cursor_color, 0, 0, txt, attr = Colors.colorPair(i) | Colors.FXReverse)
                    cursorColor = ("CursorColorTitle", newline, newline) + tuple("color" + str(i) for i in range(7))

                elements = (
                "TRAitle", newline, "TRAILext", (True, "glue", 1), "TRAIL", newline
                ) + cursorColor

                ui.list("list", elements, 3, 0, self.sett.height, self.sett.width, 1, 2, fitAll = True, vertical = False)

            elif path == "input":

                #set mouse trail length
                ui.slider("SPEED", self.mousepeed_update, 0, 0, 22, 11)
                ui.textLine("title", "Set mouse sensivity", 0, 0)

                ui.textLine("Lext", "1.0", 0, 0)

                elements = (
                "title", newline, "Lext", (True, "glue", 1), "SPEED"
                )

                ui.list("list", elements, 3, 0, self.sett.height, self.sett.width, 1, 2, fitAll = True, vertical = False)

        self.path = path


    def clearState(self):
        self.ui.removeRecursive("list")
    
    #UI events

    def FPSlider_update(self, val):
        FPSlider = (val + 1) * 5
        worldglobals.framerate = FPSlider
        worldglobals.framedelta = 1 / FPSlider
        FPSlider = str(FPSlider)
        self.ui.setText("FPSText", FPSlider, type = "txts")
        Loghandler.Log(f"FPS changed to {FPSlider}")
    
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
    
    def trailider_update(self, val):
        Wmconfig.setTrailLength(val)
        val = str(val)
        self.ui.setText("TRAILext", val, type = "txts")
        Loghandler.Log(f"Trail length changed to {val}")
    
    def mousepeed_update(self, val):
        realval = round(float(1.0 + (val - 11) * 0.2), 1)
        if val < 11:
            realval = round(float(val / 13) + 0.04, 2)
        self.ui.setText("Lext", str(realval), type = "txts")
        Wmconfig.setMouseSensivity(realval)
    
    def set_cursor_color(self, name, button, device_id):
        val = int(name[-1])
        wm = self.wm
        wm.pointers[device_id].color = Colors.colorPair(val)
            
