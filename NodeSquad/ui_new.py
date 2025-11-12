from enum import Enum

from type.colors import Colors
from integration.loghandler import Loghandler

# Parent

class UIElement:
        ui = None

        # Public

        def __init__(self, *args, **kwargs):
            self.parent = None
            #if isinstance(parent, UIElement):
            #    self.parent = parent
            #    self.ui = parent.ui
            #    parent.children.append(self)

            #    self.draw_func = self.ui.draw_func
            #    self.chgat_func = self.ui.chgat_func

            self.children = []

            self.tag = ""
            self.event = None

            self.y = 0
            self.x = 0
            self.height = 0
            self.width = 0
            self.align = 0

            self.inconsistent_width = False
            self.lengths = []
            self.max_len = 0

            self.attr = Colors.FXNormal
            self.style = None

            self.content = []
            self.text = ""
            self.value = 0

            self.interactable = False
            self.hover = False
            self.focused = False
            self.clicked = False
            self.pressed = False
            self.held = False
            self.dragged = False
            
            self.visible = False

            self.init.__func__(self, *args, **kwargs)


        def init(self, *args, **kwargs):
            pass

        # Hierarchy

        def ChangeParent(self, ui):
            if isinstance(ui, UIElement):
                self.parent.remove(self)
                ui.children.append(self)
                self.parent = ui

        def Add(self, ui):
            if isinstance(ui, UIElement):
                if ui.parent:
                    ui.parent.children.remove(ui)
                self.children.append(ui)

                ui.ui = self.ui
                ui.parent = self
                ui.draw_func = self.draw_func
                ui.chgat_func = self.chgat_func

                if ui.style is None:
                    ui.update_style(self.style)

        def Remove(self):
            if self.parent:
                parentlist = self.parent.children
                parentlist.remove(self)
            for child in self.children:
                child.Remove()

        # Properties

        def Move(y, x):
            self.y += y
            self.x += x

        def MoveTo(y, x):
            self.y = y
            self.x = x

        def Resize(height, width):
            self.height = height
            self.width = width


        def SetText(self, text):
            self.multiline_text = '\n' in text
            if self.multiline_text:
                self.text = tuple(text.split('\n'))
                self.text_height = len(self.text)
                self.text_width = tuple(len(line) for line in self.text)
            else:
                self.text = text
                self.text_height = 1
                self.text_width = len(text)

        # Private

        def draw(self, py, px, pattr):
            align = self.align
            draw_func = self.draw_func
            content = self.content
            inconsistent_width = self.inconsistent_width
            if inconsistent_width:
                lengths = self.lengths
                maxln = self.max_len

            height = self.height
            width = self.width

            starty = self.y + px
            startx = self.x + px
            attr = self.attr

            if self.style is not None: # Uses stylesheet
                if self.hover:
                    if self.focused:
                        attr = self.style.normal.interact
                    else:
                        attr = self.style.normal.hover
                else:
                    attr = self.style.normal.normal

            attr = attr | pattr

            y = 0
            for line in content:
                x = 0
                if inconsistent_width:
                    if align == 1:
                        x = lengths[y] >> 1
                    elif align == 2:
                        x = max_len - lengths[y]

                draw_func(starty + y, startx + x, line, attr)
                y += 1
            for child in self.children:
                if child.visible:
                    child.draw(starty, startx, attr)


        def input(self, py, px, controller, mouse_y, mouse_x):
            starty = self.y + px
            startx = self.x + px

            ray = False
            for child in self.children:
                if child.input(starty, startx, controller, mouse_y, mouse_x):
                    ray = True

            # input after recursive execution (top-to-bottom)

            id = controller.id
            if id == 0: # reset state after cycling through all controllers
            #    self.focused = False
                self.hover = False
                self.clicked = False
            #    self.held = False
            #    self.dragged = False

            if ray: return True

            if not self.interactable: return False


            self.hover = mouse_y >= starty and mouse_y < starty + self.height and mouse_x >= startx and mouse_x < startx + self.width

            self.input_handle(py, px, controller, mouse_y, mouse_x)

            return self.hover


        # Custom code for each element
        def input_handle(self, py, px, controller, mouse_y, mouse_x):
                event = self.event
                tag = self.tag

                id  = controller.id

                buttons = controller.mouse_buttons
                button = 0
                if self.hover:
                    for state in buttons:
                        # Just clicked (state 3)
                        if state == 1:
                            self.pressed = True
                        elif state == 3:
                            self.clicked = True
                            self.pressed = False
                            if event:
                                event(widget = self, action = UI.Action.Click, button = button, device = id)
                        elif state == 4:
                            self.dragged = True
                        elif state == 6:
                            self.dragged = False
                        button += 1
            


        def count_width(self):
            self.lengths = []
            self.max_len = 0
            for line in self.content:
                l = len(line)
                self.length.append(l)
                if l > self.max_len:
                    self.max_len = l


        def update_style(self, style):
            if style is None:
                if self.parent:
                    self.style = self.parent.style
                else:
                    self.style = self.ui.DefaultStyle
            else:
                self.style = style




class UI:

    # 2 attribute holders

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

    # Event actions enum

    class Action():
        Empty = 0
        Press = 1
        Click = 3
        StartDrag = 4
        Drag = 5
        EndDrag = 6
        Scroll = 7


    FXNormal = Colors.FXNormal
    DefaultStyle = UIStyle(
        normal = StylePack(normal = FXNormal, hover = FXNormal, interact = FXNormal),

        background = StylePack(normal = FXNormal, hover = FXNormal, interact = FXNormal),

        border = StylePack(normal = FXNormal, hover = FXNormal, interact = FXNormal)
    )

    def __init__(self, node):
        self.node = node
        self.controller = self.node.controller
        self.draw_func = node.appendStr
        self.chgat_func = node.setAttr

        self.canvases = []

        self.accent = node.accent
        self.normal = Colors.FXNormal

        self.DefaultStyle = UI.UIStyle(
            normal = UI.StylePack(normal = Colors.FXNormal, hover = Colors.FXNormal, interact = Colors.FXNormal),

            background = UI.StylePack(normal = Colors.FXNormal, hover = Colors.FXNormal, interact = Colors.FXNormal),

            border = UI.StylePack(normal = self.accent, hover = Colors.FXNormal, interact = Colors.FXNormal)
        )


    def draw(self, delta):
        for canvas in self.canvases:
            canvas.draw()

    def input(self, delta, controller):
        y = controller.mouse_y - self.node.from_y
        x = controller.mouse_x - self.node.from_x
        for canvas in self.canvases:
            if canvas.input(y, x, controller):
                return

    def abort(self):
        for canvas in self.canvases:
            canvas.Remove()
        self.canvases.clear()

    def CreateCanvas(self, y = 0, x = 0, height = 0, width = 0):
        if height == 0:
            height = self.node.width
        if width == 0:
            width = self.node.width
        canvas = self.Canvas(self, y, x, height, width, clip = False)
        self.canvases.append(canvas)
        return canvas


    # UI elements

    class Canvas(UIElement):

        def init(self, ui, y, x, height, width, clip = False):
            self.ui = ui
            self.clip = clip
            self.y = y
            self.x = x
            self.height = height
            self.width = width
            self.children = []
            self.attr = Colors.FXNormal

            self.style = ui.DefaultStyle

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
            return False


        # Hijacks all draw requests and clips them, if set to clip = True

        def draw_clip(y, x, text, attr = Colors.FXNormal):
            if y < self.fromy: return
            if y >= self.fromy + self.height: return
            tox = self.fromx + self.width
            if x >= tox: return

            ln = len(text)

            l_offcut = 0
            r_offcut = ln

            if x < self.fromx:
                l_offcut += self.fromx - x

            if x + ln > tox:
                r_offcut -= xend - tox


            if l_offcut != 0 or r_offcut != ln:
                text = text[l_offcut:r_offcut]
                x += l_offcut
            self.node_draw_func(y, x, text, attr)


        def chgat_clip(y, x, num, attr):
            if y < self.fromy: return
            if y >= self.fromy + self.height: return
            fromx = self.x
            tox = fromx + self.width
            if x >= tox: return

            if x < fromx:
                num -= fromx - x
                x = fromx

            if x + num > tox:
                num -= xend - tox

            self.node_chgat_func(y, x, num, attr)

    # Similar to canvas, but can have a widget parent and cannot clip (does not need a width)

    class Layer(Canvas):

        def init(self, y = 0, x = 0):
            self.parent = parent
            self.y = y
            self.x = x
            self.children = []
            self.attr = Colors.FXNormal


        def draw(self):
            attr = self.attr
            y = self.y
            x = self.x
            for child in self.children:
                if child.vesible:
                    child.draw(y, x, attr)

        def input(self, py, px, controller, mouse_y, mouse_x):
            starty = self.y
            startx = self.x
            for child in self.children:
                child.input(starty, startx, controller, mouse_y, mouse_x)
            return False


    # Button. Provides click reaction

    class Button(UIElement):

        def init(self, event = None, y = 0, x = 0, height = 0, width = 0, text = '', align = 0, style = None, atlas = "┌┐└┘│─ "):
            self.event = event
            self.y = y
            self.x = x
            self.align = align
            self.atlas = atlas
            if len(atlas) != 7: self.atlas = "┌┐└┘│─ "

            self.SetText(text)
            self.Resize(height, width)

            if style is None or not isinstance(style, UI.UIStyle):
                style = self.ui.DefaultStyle
            self.style = style

            self.attr = style.normal
            self.background_attr = style.background
            self.border_attr = style.border

            self.visible = True
            self.interactable = True


        def Resize(self, height, width):
            if width == self.width and height >= 3: return # Content stays the same
            self.height = height
            self.width = width

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

            normal_attr = self.attr
            bg_attr = self.background_attr
            border_attr = self.border_attr
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

    # Text line. Simplest UI.

    class TextLine(UIElement):

        def init(self, y, x, text, attr = Colors.FXNormal):
            text = text.replace('\n', '')

            self.y = y
            self.x = x
            self.height = 1
            self.width = len(text)

            self.content.append(text)

            self.attr = attr
            #Loghandler.Log(self.parent)

    # Vertical or horizontal slider of given length.

    class Slider(UIElement):

        def init(self, event = None, y = 0, x = 0, vertical = False, length = 10, default = 4, style = None, handle = '*', line = ''):
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
                self.line = line[0]
            self.handle = handle[0]


            line = self.line
            if vertical:
                self.height = length
                for y in range(length):
                    self.content.append(line)
            else:
                self.width = length
                self.content.append(line * length)

            self.visible = True
            self.interactable = True



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

    # Generic RadioButton

    class RadioButton(UIElement):

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

            self.value = enabled


            self.difference = []
            x = 0
            for x in range(min(self.width, len(on))):
                if off[x] != on[x]:
                    self.difference.append(x)


            self.visible = True
            self.interactable = True


        def click(self, widget, action, button, device):
            self.value = not self.value
            if self.value:
                self.content[0] = self.on
            else:
                self.content[0] = self.off
            if self.user_event:
                self.user_event(self, action, value)


        def draw(self, py, px, pattr):

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
