import os
import sys

from userglobals import userglobals
from integration.loghandler import Loghandler
from apps.app import App

class AppPool:
    apps = {}

    def __init__(self):

        self.default = os.listdir("apps/default/")
        external_path = userglobals.userpath + ".local/share/CLIsma/custom/apps/external/"
        self.apps = self.default.copy()
        if not os.path.exists(external_path):
            os.makedirs(external_path)
        self.external = os.listdir(external_path)

        i = len(self.external) - 1
        if i >= 0:
            while i != 0:
                app = self.installedApps[i]
                if not os.path.isdir(external_path + app):
                    self.external.pop(i)
                i -= 1

        self.apps += self.external
        #Loghandler.Log('\n'.join(self.apps))

        self.appinst = {}
        for name in self.default:
            self.appinst[name] = App("default/" + name)

        for name in self.external:
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
        return False

    def RemoveApp(self, name):
        del appinst[name]
