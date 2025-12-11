import os
import curses

from singletons import Singletons

from InputSquad.dev.device import Device
from integration.loghandler import Loghandler

class TermClick(Device):

    def open(self, device):
        pass
    
    def close(self, device):
        curses.mousemask(0)

    def abort(self):
        self.close(0)

    def edit(self, devices):
        pass

    def lock(self, device):
        pass

    def readevent(self):
        ch = stdscr.getch()
        try:
            m_id, x, y, z, state = curses.getmouse()
            self.y[0] = y - self.gy
            self.x[0] = x - self.gx
            self.gy = y
            self.gx = x
            btn = 0
            val = 0


            if (state & curses.BUTTON1_PRESSED) or (state & curses.BUTTON1_RELEASED):
                btn = 0
                val = 1 if (state & curses.BUTTON1_PRESSED) else 0
            if (state & curses.BUTTON2_PRESSED) or (state & curses.BUTTON2_RELEASED):
                btn = 1
                val = 1 if (state & curses.BUTTON2_PRESSED) else 0
            if (state & curses.BUTTON3_PRESSED) or (state & curses.BUTTON3_RELEASED):
                btn = 2
                val = 1 if (state & curses.BUTTON3_PRESSED) else 0
            self.state[0][btn] = val
        except:
            pass
    
    def start(self):
        self.gy, self.gx = 0, 0
        self.y, self.x = [0], [0]
        self.wheel = [0]
        self.state = [[0, 0, 0]]

        self.scr = Singletons.Screenman.screen
        curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)
