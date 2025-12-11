import os
import curses

from singletons import Singletons

from InputSquad.dev.device import Device
from integration.loghandler import Loghandler

class TermClick(Device):

    def open(self, device):
        pass
    
    def close(self, device):
        pass

    def lock(self, device):
        pass

    def readevent(self):
        ch = self.scr.getch()
        if ch == curses.KEY_MOUSE:
            m_id, x, y, z, state = curses.getmouse()
            self.x = x - self.x
            self.y = y - self.y
            btn = 0
            val = 0
            if state & curses.BUTTON1_PRESSED or state & curses.BUTTON1_RELEASED:
                btn = 1
                val = state & curses.BUTTON1_PRESSED
            if state & curses.BUTTON2_PRESSED or state & curses.BUTTON2_RELEASED:
                btn = 2
                val = state & curses.BUTTON2_PRESSED
            if state & curses.BUTTON3_PRESSED or state & curses.BUTTON3_RELEASED:
                btn = 3
                val = state & curses.BUTTON3_PRESSED
            self.state[0][btn] = val
    
    def start(self):
        self.y, self.x = [0], [0]
        self.wheel = [0]
        self.state = [[0, 0, 0]]

        self.scr = Singletons.Screenman.screen

