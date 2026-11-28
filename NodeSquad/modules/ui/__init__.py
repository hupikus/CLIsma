from enum import Enum

from type.colors import Colors
from type.keys import Keys
from integration.loghandler import Loghandler

from . import elements

class UI:

    # 2 attribute holders

    class StylePack():
        def __init__(self, normal, hover, interact):
            self.normal = normal
            self.hover = hover
            self.interact = interact

    class UIStyle():
        def __init__(self, normal, background, border):
            self.normal = normal
            self.background = background
            self.border = border

    # Event actions enum

    class Action():
        Empty = 0
        Press = 1
        Click = 3
        StartDrag = 4
        Drag = 5
        EndDrag = 6
        Scroll = 7


    FXNormal = Colors.FXNormal
    DefaultStyle = UIStyle(
        normal = StylePack(normal = FXNormal, hover = FXNormal, interact = FXNormal),

        background = StylePack(normal = FXNormal, hover = FXNormal, interact = FXNormal),

        border = StylePack(normal = FXNormal, hover = FXNormal, interact = FXNormal)
    )

    def __init__(self, node, args = ''):
        self.node = node
        self.controller = self.node.controller
        self.draw_func = node.appendStr
        self.chgat_func = node.setAttr

        self.canvases = []

        self.accent = node.accent
        self.normal = Colors.FXNormal

        self.DefaultStyle = UI.UIStyle(
            normal = UI.StylePack(normal = Colors.FXNormal, hover = Colors.FXNormal, interact = Colors.FXNormal),

            background = UI.StylePack(normal = Colors.FXNormal, hover = Colors.FXNormal, interact = Colors.FXNormal),

            border = UI.StylePack(normal = self.accent, hover = Colors.FXNormal, interact = Colors.FXNormal)
        )

        self.keyboardFocus = None

    def draw(self, delta):
        for canvas in self.canvases:
            canvas.draw()

    def input(self, delta, controller):
        y = controller.mouse_y - self.node.from_y
        x = controller.mouse_x - self.node.from_x
        for canvas in reversed(self.canvases):
            if canvas.input(y, x, controller):
                return

    def abort(self):
        for canvas in self.canvases:
            canvas.Remove()
        self.canvases.clear()

    def CreateCanvas(self, y = 0, x = 0, height = 0, width = 0, clip = False):
        if height == 0:
            height = self.node.width
        if width == 0:
            width = self.node.width
        canvas = self.Canvas(self, y, x, height, width, clip)
        self.canvases.append(canvas)
        return canvas


    # Input listeners

    def keyPress(self, key):
        if not self.keyboardFocus: return True
        self.keyboardFocus.keyPress(key)

    def keyRelease(self, key):
        if not self.keyboardFocus: return True
        self.keyboardFocus.keyRelease(key)

    def keyType(self, key):
        if not self.keyboardFocus: return True
        self.keyboardFocus.keyType(key)

    # UI elements
    # Implemented - sorted chronologically:
    # Canvas; Button; Text; Slider; RadioButton; ClickArea; InputField

    # Yet to be implemented:
    # Sprite; WrappedText; InputBox; ListView; GridView; ScrollView; SequenceView.
