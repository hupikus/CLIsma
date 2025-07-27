import os

class Singletons:

    # Screenman = None
    # Cfg = None
    # Inpd = None
    # Wm = None

    @classmethod
    def start(cls, forceColor, desktop):
        from WMSquad.wm import Wm
        from InputSquad.inpdevices import DeviceHandler
        from WMSquad.screen import Screen
        from globalconfig import Config
        from NodeSquad.appool import AppPool


        cls.appp = AppPool()

        cls.Screenman = Screen(forceColor)

        cls.Cfg = Config()

        cls.Inpd = DeviceHandler()

        cls.Wm = Wm(cls.Screenman, cls.Inpd, desktop)
