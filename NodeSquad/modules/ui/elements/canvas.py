from .ui_element import UIElement
from type.colors import Colors
from integration.loghandler import Loghandler

class Canvas(UIElement):
    """Basic container for the other elements.
    Used as root, scene, layer or attribute container."""

    def Get(self):
        return len(self.children)

    def init(self, ui, y = 0, x = 0, height = 0, width = 0, clip = False):
        self.is_canvas = True
        self.ui = ui
        self.clip = clip
        self.y = y
        self.x = x
        self.height = height
        self.width = width
        self.children = []
        self.attr = Colors.FXNormal

        self.SetStyle()

        if clip:
            self.draw_func = self.draw_clip
            self.chgat_func = self.chgat_clip

            self.node_draw_func = ui.draw_func
            self.node_chgat_func = ui.chgat_func
        else:
            self.draw_func = ui.draw_func
            self.chgat_func = ui.chgat_func


    def draw(self):
        attr = self.attr
        y = self.y
        x = self.x
        for child in self.children:
            if child.visible:
                child.draw(y, x, attr)

    def input(self, mouse_y, mouse_x, controller):
        starty = self.y
        startx = self.x
        for child in self.children:
            child.input(starty, startx, controller, mouse_y, mouse_x)

        if self.ui.keyboardFocus:
            focus = self.ui.keyboardFocus
            clear_focus = False
            if not focus.hover and any(self.ui.controller.mouse_buttons):
                clear_focus = True
            if clear_focus:
                self.ui.keyboardFocus = None
        return False


    # If self.clip set to true, draws with clipping
    def draw_clip(self, y, x, text, attr = Colors.FXNormal):
        if y < self.y: return
        if y >= self.y + self.height: return
        tox = self.x + self.width
        if x >= tox: return

        ln = len(text)

        l_offcut = 0
        r_offcut = ln

        if x < self.x:
            l_offcut = self.x - x

        if x + ln >= tox:
            r_offcut -= x + ln - tox


        if l_offcut != 0 or r_offcut < ln:
            text = text[l_offcut:r_offcut]
            x += l_offcut
        self.node_draw_func(y, x, text, attr)

    # Changes attribute with clipping
    def chgat_clip(self, y, x, num, attr):
        if y < self.y: return
        if y >= self.y + self.height: return
        fromx = self.x
        tox = fromx + self.width
        if x >= tox: return

        if x < fromx:
            num -= fromx - x
            x = fromx

        if x + num > tox:
            num -= x + num - tox

        self.node_chgat_func(y, x, num, attr)

    def setKeyboardFocus(self, element):
        self.ui.keyboardFocus = element

    def releaseKeyboardFocus(self, element):
        if self.ui.keyboardFocus == element:
            self.ui.keyboardFocus = None

