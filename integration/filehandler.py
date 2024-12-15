import os
from apps.apps import App
from integration.loghandler import Loghandler

class Filehandler:

    @staticmethod
    def appToUse(path):
        if os.path.isdir(path):
            return App("default/fileman")
        else:
            ext = path[-path[::-1].find('.'):]
            Loghandler.Log(ext)
            if ext == "mp3":
               return App("default/bangerplayer")
            else:
                return App("default/textplayer") 
        return None