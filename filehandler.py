import os
from apps.apps import App

class Filehandler:

    @staticmethod
    def appToUse(path):
        if os.path.isdir(path):
            return App("default/fileman")
        else:
            ext = path[-path[::-1].find('.')]
            if ext == "txt":
               return App("default/textplayer")
            else:
                return App("default/textplayer") 
        return None