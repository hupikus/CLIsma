from singletons import Singletons
class Wmconfig:
    wm = Singletons.Wm

    @staticmethod
    def setTrailLength(val):
        wm = Wmconfig.wm
        wm.trailength = val
        wm.trail = [(0, 0) for i in range(val + 1)]
        for i in range(wm.pointer_count):
            wm.pointers[i].update_trail(val)

    @staticmethod
    def setMouseSensivity(val):
        Wmconfig.wm.control.mouse_speed = val * 0.18

    @staticmethod
    def setDesktopRefresh(val):
        Wmconfig.wm.desktop.refresh = val


class DesktopConfig:
    desktop = Singletons.Wm.desktop

    patterns = ("line", "circle")
    @staticmethod
    def setSpawnPattern(name):
        ind = DesktopConfig.patterns.find(name)
        if ind >= 0:
            desktop.setmaxstep(ind)
