from copy import copy
from type.colors import Colors
from integration.loghandler import Loghandler
from .elements import *

class UI:
    # 2 attribute holders
    from .style import UIStyle, StylePack, DefaultStyle

    def __init__(self, node, args = ''):
        self.node = node
        self.controller = self.node.controller
        self.draw_func = node.appendStr
        self.chgat_func = node.setAttr

        self.canvases = []

        self.accent = node.accent
        self.normal = Colors.FXNormal

        self.DefaultStyle = copy(UI.DefaultStyle)
        self.DefaultStyle.border.normal = self.accent

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

    Canvas = elements.Canvas
    ClickArea = elements.ClickArea
    Text = elements.Text
    Button = elements.Button
    Slider = elements.Slider
    RadioButton = elements.RadioButton
    InputField = elements.InputField
