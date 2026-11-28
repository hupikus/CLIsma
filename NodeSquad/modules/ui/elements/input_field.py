from . import UIElement

from type.colors import Colors
from integration.loghandler import Loghandler
from type.keys import Keys

class InputField(UIElement):
    """Single line input prompt of given width."""

    def init(self, event = None, x = 0, y = 0, width = 24, border = True, style = None):
        if callable(event):
            self.user_event = event
        else:
            self.user_event = None

        self.text = ""
        self.text_len = 0
        self.GetText = self.Get

        self.cursor = 0
        self.selection = -1
        self.view = 0

        self.border = border
        self.border_visible = border

        self.y = y
        self.x = x
        self.SetWidth(width)
        self.height = 3 if border else 1

        self.SetStyle(style)
        self.attr = self.style.border

        self.visible = True
        self.post_draw = True

        self.interactable = True
        self.event = self.click


    def SetBorder(self, border):
        self.border = border

    def Resize(self, height, width):
        self.border_visible = (self.border and (height >= 3 and width >= 2))
        self.height = 1 if height < 3 else 3
        self.SetWidth(width)

    def SetWidth(self, width):
        self.width = width
        self.Refresh()

    def Refresh(self):
        self.text_len = len(self.text)
        if not self.border_visible:
            if self.border:
                self.content = [""]
            return

        self.content = [None, None, None]
        line = '─' * (self.width - 2)
        self.content[0] = '┌' +           line           + '┐'
        self.content[1] = '│' + (' ' * (self.width - 2)) + '│'
        self.content[2] = '└' +           line           + '┘'

    def postdraw(self, starty, startx, attr):
        y = starty
        x = startx

        maxlen = self.width

        if self.border_visible:
            y += 1
            x += 1
            maxlen -= 2

        attr = Colors.FXNormal
        if not self.border_visible:
            attr = attr | Colors.FXUnderline
        
        text = self.text

        xview = self.view

        if self.cursor - xview < 0 and xview > 0:
            self.view -= 1
        elif self.cursor - xview >= maxlen:
            self.view += 1
        xview = self.view

        mx = self.text_len
        if mx - xview >= self.width - 2:
            mx -= (mx - xview) - (self.width - 2)

        self.draw_func(y, x, text[xview:mx], attr)

        if self.canvas:
            if self.canvas.ui.keyboardFocus != self:
                return

        if self.selection == -1:
            self.chgat_func(y, x + self.cursor - xview, 1, Colors.FXReverse)
        else:
            p1 = self.cursor - xview
            p2 = self.selection - xview
            if self.selection < self.cursor:
                p1, p2 = p2, p1
            self.chgat_func(y, x + p1, p2 - p1 + 1, Colors.FXReverse)

    def click(self, widget, action, button, device):
        if self.canvas:
            self.canvas.setKeyboardFocus(self)


    def keyType(self, key):
        text_event = False

        shift = False
        ctrl = False
        if self.canvas:
            keys = self.canvas.ui.controller.keys.keys
            shift = bool(keys[Keys.KEY_LEFTSHIFT] | keys[Keys.KEY_RIGHTSHIFT])


        if Keys.isSymbol(key):
            t = Keys.GetInput(key, shift, allow_escape = False)
            if t:
                self.text = self.text[:self.cursor] + t + self.text[self.cursor:]
                self.cursor += 1
                self.text_len += 1
            text_event = True
        elif key == Keys.KEY_BACKSPACE:
            if self.cursor > 0 and self.text_len > 0:
                self.text = self.text[:self.cursor - 1] + self.text[self.cursor:]
                self.cursor -= 1
                self.text_len -= 1
                if self.view > 0:
                    self.view -= 1
            text_event = True
        elif key == Keys.KEY_DELETE:
            if self.cursor < self.text_len and self.text_len > 0:
                self.text = self.text[:self.cursor] + self.text[self.cursor + 1:]
                self.text_len -= 1
        elif key == Keys.KEY_UP:
            self.cursor = 0
        elif key == Keys.KEY_DOWN:
            self.cursor = self.text_len
        elif key == Keys.KEY_ENTER:
            self.canvas.releaseKeyboardFocus(self)
        

        if key == Keys.KEY_LEFT or key == Keys.KEY_RIGHT:
            if shift:
                if self.selection == -1:
                    self.selection = self.cursor
            else:
                self.selection = -1

            if key == Keys.KEY_RIGHT:
                self.cursor += 1
                if self.cursor > self.text_len:
                    self.cursor = self.text_len
            else:
                self.cursor -= 1
                if self.cursor < 0:
                    self.cursor = 0

        if text_event and self.user_event:
            self.user_event(self.text)

