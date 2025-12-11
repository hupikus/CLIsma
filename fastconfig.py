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


class Compatconfig:
    wm = Singletons.Wm

    @staticmethod
    def BFMode(val):
        wm = Compatconfig.wm
        desktop = wm.desktop.node
        wm.fbmode = val
        if val:
            desktop.width = wm.screen_width - 2
            desktop.from_x = 1
            desktop.to_x = wm.screen_width - 2
        else:
            desktop.width = wm.screen_width
            desktop.from_x = 0
            desktop.to_x = wm.screen_width
        desktop.win.onresize(wm.screen_height, desktop.width)
