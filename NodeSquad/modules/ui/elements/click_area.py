from . import UIElement
from type.colors import Colors
from integration.loghandler import Loghandler

class ClickArea(UIElement):
    """Click Area. Invisible.
    Provides basic events for clicks within a rectangular area."""

    def Get(self):
        return self.clicked

    def init(self, event = None, y = 0, x = 0, height = 3, width = 6, match_parent = False):
        self.event = event
        self.y = y
        self.x = x
        self.height = height
        self.width = width

        self.visible = False
        self.draw = self.draw_children

        self.match_parent = match_parent
        if match_parent:
            self._super = super()
            self.input = self.input_match


    def input_match(self, *args, **kwargs):
        # Pre input
        self.height = self.parent.height
        self.width = self.parent.width

        # Parent input
        self._super.input(args, kwargs)

