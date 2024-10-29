import os
import curses

from wm import Wm
from inpdevices import DeviceHandler
from screen import Screen
from globalconfig import Config

screen_height, screen_width = map(int, os.popen('stty size', 'r').read().split())

class Singletons:
    global screen_height
    global screen_width


    Screenman = Screen(screen_width, screen_height)

    Cfg = Config()

    Inpd = DeviceHandler()

    Wm = Wm(Screenman, Inpd)
