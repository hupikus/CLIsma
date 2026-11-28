from .ui_element import UIElement
from type.colors import Colors
from integration.loghandler import Loghandler

class Text(UIElement):

    def init(self, y = 0, x = 0, text = '', attr = Colors.FXNormal):
        self.y = y
        self.x = x
        self.resizable = False
        self.SetText(text)
        self.Refresh()
        self.content = [text]
        self.attr = attr
        self.visible = True

        self.input = self.input_children

        def Refresh(self):
            self.content = []
            height = 0
            width = 0
            for line in self.text.split('/n'):
                height += 1
                ln = len(line)
                if ln > width: width = ln
                self.content.append(line)
            self.height = height
            self.width = width

