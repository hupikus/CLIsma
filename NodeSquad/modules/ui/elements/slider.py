from . import UIElement
from type.colors import Colors
from integration.loghandler import Loghandler

class Slider(UIElement):
    """Vertical or horizontal slider of given length."""

    def Get(self):
        return self.pos

    def init(self, event = None, y = 0, x = 0, vertical = False, length = 10, default = 4, handle_length = 1, style = None, handle = '*', line = ''):
        if callable(event):
            self.event = event
        self.y = y
        self.x = x
        self.length = length
        self.width = 1
        self.height = 1
        self.vertical = vertical

        if default < 0:
            default = 0
        elif default >= length:
            default = length - 1

        self.pos = default

        if line == '':
            if vertical:
                self.line = '│'
            else:
                self.line = '─'
        else:
            self.line = str(line)[0]
        self.handle = str(handle)[0]

        self.SetLength(length)
        self.SetHandleLength(handle_length)

        self.visible = True
        self.interactable = True


    def Resize(self, height, width):
        if self.vertical:
            self.SetLength(height)
        else:
            self.SetLength(width)

    def SetLength(self, length):
        if length <= 0: return
        dl = 0
        if self.vertical:
            dl = self.height - length
            self.height = length
        else:
            dl = self.width - length
            self.width = length
        self.length = length
        if dl != 0:
            self.Refresh()
    
    def SetHandleLength(self, length):
        if length > self.length:
            length = self.length
        self.handle_length = length

    def Refresh(self):
        line = self.line
        if self.vertical:
            y = len(self.content)
            ytarget = self.height
            content = self.content

            if y < ytarget:
                while y < ytarget:
                    content.append(line)
                    y += 1
            elif y > ytarget:
                while y > ytarget:
                    content.pop()
                    y -= 1
        else:
            self.content = [line * self.width]


    def draw(self, py, px, pattr):

        draw_func = self.draw_func
        chgat_func = self.chgat_func

        height = self.height
        width = self.width

        starty = self.y + px
        startx = self.x + px

        style = self.style

        border = None
        normal = None

        if style:
            if self.clicked or self.dragged:
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


        dy = 0
        for line in self.content:
            draw_func(starty + dy, startx, line, border)
            dy += 1

        handle_y = starty
        handle_x = startx

        if self.vertical:
            handle_y += self.pos
        else:
            handle_x += self.pos
        draw_func(handle_y, handle_x, self.handle, normal)

        for child in self.children:
            if child.visible:
                child.draw(starty, startx, attr)



    def input_handle(self, py, px, controller, mouse_y, mouse_x):
        starty = self.y + px
        startx = self.x + px

        #id = controller.id
        tag = self.tag

        buttons = controller.mouse_buttons
        button = 0

        event = False

        Actions = UI.Action
        action = Actions.Empty

        hover = self.hover

        for state in buttons:
            # Just clicked (state 3)
            if state == UI.Action.Click and hover:
                self.clicked = True
                if self.vertical:
                    self.pos = mouse_y - starty
                else:
                    self.pos = mouse_x - startx
                event = True
                action = state

            elif (state == Actions.StartDrag and hover) or (state == Actions.Drag and self.dragged):
                self.dragged = True
                if self.vertical:
                    self.pos = mouse_y - starty
                else:
                    self.pos = mouse_x - startx
                if self.pos < 0:
                    self.pos = 0
                elif self.pos >= self.length:
                    self.pos = self.length - 1
                event = True
                action = state

            elif state == Actions.EndDrag:
                self.dragged = False

            button += 1

        if event and self.event:
            self.event(widget = self, action = action, value = self.pos)



