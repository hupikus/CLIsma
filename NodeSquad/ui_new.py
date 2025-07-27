#Original ui.py is a mess. I am planning to fully rewrite it.
from type.colors import Colors
from integration.loghandler import Loghandler

class UIElement:
    x = 0
    y = 0
    height = 0
    width = 0
    draw = [""]
    attr = Colors.FXNormal

class Button(UIElement):
    pass
