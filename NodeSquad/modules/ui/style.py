from type.colors import Colors

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

_FXNormal = Colors.FXNormal
DefaultStyle = UIStyle(
    normal = StylePack(normal = _FXNormal, hover = _FXNormal, interact = _FXNormal),

    background = StylePack(normal = _FXNormal, hover = _FXNormal, interact = _FXNormal),

    border = StylePack(normal = _FXNormal, hover = _FXNormal, interact = _FXNormal)
    )
