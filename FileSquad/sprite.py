import sys
from pathlib import Path

from type.colors import Colors
from integration.loghandler import Loghandler

class SpriteData:

    def __init__(self):
        module = sys.modules[cls.__module__]
        Loghandler.Log(Path(module.__file__).resolve().parents[0])

    def FromAssets(self, path):
        appAsset = False
        if resource.startswith("app:/"):
            appAsset = True
        return self.FromFile(f"{resource}")

    def FromFile(self, path):
        pass


