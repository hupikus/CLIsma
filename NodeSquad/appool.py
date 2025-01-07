import os

from userglobals import userglobals
from integration.loghandler import Loghandler

class AppPool:
    apps = {}

    def __init__(self):
        
        self.apps = os.listdir(userglobals.userpath + ".local/share/CLIsma/custom/apps/")

        i = len(self.apps) - 1
        if i >= 0:
            while i != 0:
                app = self.apps[i]
                Loghandler.Log(app)
                if not os.path.isdir(userglobals.userpath + ".local/share/CLIsma/custom/apps/" + app):
                    self.apps.pop(i)
                i -= 1

        self.apps += os.listdir("apps/default/")