from .ui_element import UIElement
from type.colors import Colors
from integration.loghandler import Loghandler

class RadioButton(UIElement):
    """Generic radio button."""

    def Get(self):
        return self.value

    def init(self, event = None, x = 0, y = 0, enabled = False, off = "[ ]", on = "[*]"):
        if callable(event):
            self.user_event = event
        else:
            self.user_event = None
        self.event = self.click

        self.y = y
        self.x = x
        self.width = len(off)
        self.height = 1

        self.off = off
        self.on = on

        if enabled:
            self.content.append(on)
        else:
            self.content.append(off)

        self.value = bool(enabled)


        self.difference = []
        x = 0
        for x in range(min(self.width, len(on))):
            if off[x] != on[x]:
                self.difference.append(x)


        self.visible = True
        self.resizable = False
        self.interactable = True


    def click(self, widget, action, button, device):
        self.value = not self.value
        if self.value:
            self.content[0] = self.on
        else:
            self.content[0] = self.off
        if self.user_event:
            self.user_event(self, action, value)


    def _draw(self, py, px, pattr):

        draw_func = self.draw_func
        chgat_func = self.chgat_func

        starty = self.y + px
        startx = self.x + px

        style = self.style

        border = None
        normal = None

        if style:
            if self.pressed:
                border = style.border.interact
                normal = style.normal.interact
            elif self.hover:
                border = style.border.hover
                normal = style.normal.hover
            else:
                border = style.border.normal
                normal = style.normal.normal
        else:
            border = normal = Colors.FXNormal

        draw_func(starty, startx, self.content[0], border)
        if self.value:
            for dx in self.difference:
                chgat_func(starty, startx + dx, 1, normal)

        for child in self.children:
            if child.visible:
                child.draw(starty, startx, attr)

