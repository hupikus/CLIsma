from type.colors import Colors
_FXNormal = Colors.FXNormal

class StylePack():
    def __init__(self, normal = _FXNormal, hover = _FXNormal, interact = _FXNormal):
        self.normal = normal
        self.hover = hover
        self.interact = interact

class UIStyle():
    def __init__(self, normal = _FXNormal, background = _FXNormal, border = _FXNormal):
        self.normal = normal
        self.background = background
        self.border = border

DefaultStyle = UIStyle(
    normal = StylePack(),
    background = StylePack(),
    border = StylePack()
)
