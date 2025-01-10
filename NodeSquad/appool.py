import os

from userglobals import userglobals
from integration.loghandler import Loghandler
from apps.apps import App

class AppPool:
    apps = {}

    def __init__(self):

        self.systemApps = os.listdir("apps/default/")
        self.apps = self.systemApps[:]
        
        self.installedApps = os.listdir(userglobals.userpath + ".local/share/CLIsma/custom/apps/")

        i = len(self.installedApps) - 1
        if i >= 0:
            while i != 0:
                app = self.installedApps[i]
                if not os.path.isdir(userglobals.userpath + ".local/share/CLIsma/custom/apps/" + app):
                    self.installedApps.pop(i)
                i -= 1

        self.apps += self.installedApps
        Loghandler.Log('\n'.join(self.apps))
    
        self.appinst = {}
        for name in self.systemApps:
            self.appinst[name] = App("default/" + name)

        for name in self.installedApps:
            self.appinst[name] = App("external/" + name)

    def GetAppInstances(self):
        return self.appinst
    
    def GetAppInstance(self, name):
        return self.appinst[name]
    
    def AppInstalled(self, name):
        app = App(name)
        if app:
            self.appinst[name] = app
            return True
        else:
            return False
    
    def AppRemoved(self, name):
        del appinst[name]