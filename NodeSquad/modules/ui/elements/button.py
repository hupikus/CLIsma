from . import UIElement
from type.colors import Colors
from integration.loghandler import Loghandler

class Button(UIElement):
    """Button. Provides click reaction"""

    def Get(self):
        return self.clicked

    def init(self, event = None, y = 0, x = 0, height = 5, width = 12, text = '', align = 1, style = None, atlas = "┌┐└┘│─ "):
        self.event = event
        self.y = y
        self.x = x
        self.align = align
        self.atlas = atlas
        if len(atlas) != 7: self.atlas = "┌┐└┘│─ "

        self.SetText(text)
        self.Resize(height, width)

        self.SetStyle(style)

        self.attr = self.style.normal

        self.visible = True
        self.interactable = True


    def Resize(self, height, width):
        #if width == self.width and height >= 3: return # Content stays the same
        if height < 3 or width < 3: return
        self.height = height
        self.width = width
        self.Refresh()

    def Refresh(self):
        height = self.height
        width = self.width

        alignFunc = str.ljust
        if self.align == 1: alignFunc = str.center
        elif self.align == 2: alignFunc = str.rjust

        atlas = self.atlas
        if width < 2:
            self.content = [atlas[4] for i in range(4)]
            self.width = 1
        elif height < 3:
            self.content = [(atlas[5] * width + '') for i in range(4)]
            self.height = 1
        else:

            wm2 = atlas[5] * (width - 2)

            self.content = [
                atlas[0] + wm2 + atlas[1],                    #top border
                atlas[4] + atlas[6] * (width - 2) + atlas[4], #center
                atlas[2] + wm2 + atlas[3]                     #bottom border
            ]


    def draw(self, py, px, pattr):
        if not self.visible: return

        draw_func = self.draw_func
        chgat_func = self.chgat_func

        align = self.align
        content = self.content

        height = self.height
        width = self.width

        starty = self.y + px
        startx = self.x + px

        normal_attr = self.style.normal
        bg_attr = self.style.background
        border_attr = self.style.border
        if self.hover:
            if self.focused:
                normal_attr = normal_attr.interact
                bg_attr = bg_attr.interact
                border_attr = border_attr.interact
            else:
                normal_attr = normal_attr.hover
                bg_attr = bg_attr.hover
                border_attr = border_attr.hover

        else:
            normal_attr = normal_attr.normal
            bg_attr = bg_attr.normal
            border_attr = border_attr.normal

        normal_attr = normal_attr | pattr
        bg_attr = bg_attr | pattr
        border_attr = border_attr | pattr

        attr = normal_attr

        y = 0
        if width < 2:
            # Draw vertical border only
            while y < height:
                draw_func(starty + y, startx, content[0], border_attr)
                y += 1
        elif height < 3:
            # Draw horizontal border only
            while y < height:
                draw_func(starty + y, startx, content[0], border_attr)
                y += 1
        else:
            # Draw normally
            vertical_border = self.atlas[4]
            center = content[1]

            draw_func(starty + y, startx, content[0], border_attr) # Top border
            y = 1

            while y < height - 1: # Center
                draw_func(starty + y, startx, center, bg_attr)
                chgat_func(starty + y, startx, 1, border_attr)
                chgat_func(starty + y, startx + width - 1, 1, border_attr)
                y += 1

            draw_func(starty + y, startx, content[2], border_attr) # Bottom border

            if not self.multiline_text:
                draw_func(starty + (height >> 1), startx + (width - self.text_width >> 1), self.text, normal_attr) #Text
            else:
                h = self.text_height
                w = self.text_width
                text = self.text

                y = starty + (height - h >> 1)
                line = 0
                while line < h: # and y < maxy:
                    draw_func(y + line, startx + (width - w[line] >> 1), text[line], normal_attr) #Text
                    line += 1

        for child in self.children:
            if child.visible:
                child.draw(starty, startx, attr)

