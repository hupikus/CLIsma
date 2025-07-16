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

        siz = tuple(map(int, os.popen('stty size', 'r').read().split()))
        global screen_height
        screen_height = siz[0]
        global screen_width
        screen_width = siz[1]

        cls.Screenman = Screen(screen_width, screen_height, forceColor)

        cls.Cfg = Config()

        cls.Inpd = DeviceHandler()

        cls.Wm = Wm(cls.Screenman, cls.Inpd, desktop)
