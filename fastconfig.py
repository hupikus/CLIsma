from singletons import Singletons
class Wmconfig:
    wm = Singletons.Wm
    @staticmethod
    def setTrailLength(val):
        Wmconfig.wm.trailength = val
        Wmconfig.wm.trail = [(0, 0) for i in range(val + 1)]

class DesktopConfig:
    desktop = Singletons.Wm.desktop

    patterns = ("line", "circle")
    @staticmethod
    def setSpawnPattern(name):
        ind = DesktopConfig.patterns.find(name)
        if ind >= 0:
            desktop.setmaxstep(ind)