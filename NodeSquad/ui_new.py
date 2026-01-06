from enum import Enum

from type.colors import Colors
from type.keys import Keys
from integration.loghandler import Loghandler

# Parent

class UIElement:
        ui = None

        # Public

        def __init__(self, *args, **kwargs):
            self.is_canvas = False
            self.parent = None
            self.canvas = None
            self.children = []

            self.tag = ""
            self.event = None

            self.y = 0
            self.x = 0
            self.height = 0
            self.width = 0
            self.align = 0
            self.resizable = True

            self.inconsistent_width = False
            self.lengths = []
            self.max_len = 0

            self.attr = Colors.FXNormal
            self.style_set = False
            self.SetStyle()

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
            
            self.post_draw = False
            
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

        # Add children to self
        def Add(self, ui):
            if isinstance(ui, UIElement):
                if ui.parent:
                    ui.parent.children.remove(ui)
                self.children.append(ui)

                ui.ui = self.ui
                ui.parent = self
                if self.is_canvas:
                    ui.SetCanvas(self)
                else:
                    ui.SetCanvas(self.canvas)

                #ui.SetStyle(self.style)

        # Assign self to canvas
        def SetCanvas(self, canvas, check = True):
            if not check or isinstance(canvas, UI.Canvas):
                changed = (not check or self.canvas != canvas)
                if changed:
                    self.canvas = canvas

                    # Canvas-specific behaviour
                    self.draw_func = canvas.draw_func
                    self.chgat_func = canvas.chgat_func
                    if not self.style_set:
                        self.SetStyle()

                    for child in self.children:
                        child.SetCanvas(canvas, check = False)

        # Detach self from parent (become ready for gc)
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

        def Resize(self, height, width):
            if not self.resizable: return
            self.height = height
            self.width = width
            self.Refresh()


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

        def SetStyle(self, style = None):
            if not isinstance(style, UI.UIStyle):
                self.style_set = True
                if self.parent and self.parent.style_set:
                    self.style = self.parent.style
                elif self.canvas:
                    self.style = self.canvas.ui.DefaultStyle
                else:
                    self.style = UI.DefaultStyle
                    self.style_set = False
            else:
                self.style = style
                self.style_set = True


        # Common Operators (like content generation)

        def Refresh(self):
            pass

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
            attr = 0

            if self.style: # Uses stylesheet
                if self.hover and self.visible:
                    if self.focused:
                        attr = self.style.border.interact
                    else:
                        attr = self.style.border.hover
                else:
                    attr = self.style.border.normal
            elif self.attr:
                attr = self.attr

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

            if self.post_draw:
                self.postdraw(starty, startx, attr)

            for child in self.children:
                if child.visible:
                    child.draw(starty, startx, attr)

        def postdraw(self, starty, startx, attr):
            pass


        def input(self, py, px, controller, mouse_y, mouse_x):
            starty = self.y + px
            startx = self.x + px

            ray = False
            for child in reversed(self.children):
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


        # input listeners
        def keyPress(self, key):
            pass

        def keyRelease(self, key):
            pass

        def keyType(self, key):
            pass

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

        self.keyboardFocus = None

    def draw(self, delta):
        for canvas in self.canvases:
            canvas.draw()

    def input(self, delta, controller):
        y = controller.mouse_y - self.node.from_y
        x = controller.mouse_x - self.node.from_x
        for canvas in reversed(self.canvases):
            if canvas.input(y, x, controller):
                return

    def abort(self):
        for canvas in self.canvases:
            canvas.Remove()
        self.canvases.clear()

    def CreateCanvas(self, y = 0, x = 0, height = 0, width = 0, clip = False):
        if height == 0:
            height = self.node.width
        if width == 0:
            width = self.node.width
        canvas = self.Canvas(self, y, x, height, width, clip)
        self.canvases.append(canvas)
        return canvas


    # Input listeners

    def keyPress(self, key):
        if not self.keyboardFocus: return True
        self.keyboardFocus.keyPress(key)

    def keyRelease(self, key):
        if not self.keyboardFocus: return True
        self.keyboardFocus.keyRelease(key)

    def keyType(self, key):
        if not self.keyboardFocus: return True
        self.keyboardFocus.keyType(key)

    # UI elements
    # Implemented:
    # Canvas; Layer; Button; TextLine; Slider; RadioButton; ClickArea;

    # Yet to be implemented:
    # Sprite; WrappedText; InputBox;
    # ListView; GridView; ScrollView; SequenceView.

    
    # Basic container for the other elements. Used as root, scene or attribute container.
    class Canvas(UIElement):

        def init(self, ui, y = 0, x = 0, height = 9, width = 15, clip = False):
            self.is_canvas = True
            self.ui = ui
            self.clip = clip
            self.y = y
            self.x = x
            self.height = height
            self.width = width
            self.children = []
            self.attr = Colors.FXNormal

            self.SetStyle()

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

            if self.ui.keyboardFocus:
                focus = self.ui.keyboardFocus
                clear_focus = False
                if not focus.hover and any(self.ui.controller.mouse_buttons):
                    clear_focus = True
                if clear_focus:
                    self.ui.keyboardFocus = None
            return False


        # Hijacks all draw requests and clips them, if set to clip = True

        def draw_clip(self, y, x, text, attr = Colors.FXNormal):
            if y < self.y: return
            if y >= self.y + self.height: return
            tox = self.x + self.width
            if x >= tox: return

            ln = len(text)

            l_offcut = 0
            r_offcut = ln

            if x < self.x:
                l_offcut = self.x - x

            if x + ln >= tox:
                r_offcut -= x + ln - tox


            if l_offcut != 0 or r_offcut < ln:
                text = text[l_offcut:r_offcut]
                x += l_offcut
            self.node_draw_func(y, x, text, attr)


        def chgat_clip(self, y, x, num, attr):
            if y < self.y: return
            if y >= self.y + self.height: return
            fromx = self.x
            tox = fromx + self.width
            if x >= tox: return

            if x < fromx:
                num -= fromx - x
                x = fromx

            if x + num > tox:
                num -= x + num - tox

            self.node_chgat_func(y, x, num, attr)

        def setKeyboardFocus(self, element):
            self.ui.keyboardFocus = element

        def releaseKeyboardFocus(self, element):
            if self.ui.keyboardFocus == element:
                self.ui.keyboardFocus = None

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


    # ClickArea. invisible. provides basic events for clicks within a rectangular area.
    class ClickArea(UIElement):

        def init(self, event = None, y = 0, x = 0, height = 3, width = 6):
            self.event = event
            self.y = y
            self.x = x
            self.height = height
            self.width = width

            self.visible = False
            self.sprite = None
            self.draw = self.draw_children

        # TODO sprite draw function
        def SetSprite(self, sprite):
            if self.sprite:
                self.sprite.visible = True
                self.sprite = None
            if sprite:
                if isinstance(sprite, UIElement):
                    self.sprite = sprite

            self.visible = bool(self.sprite)
            if self.visible:
                sprite.visible = False
                self.draw = UIElement.draw
            else:
                self.draw = self.draw_children

        def draw_children(self, py, px, pattr):
            starty = self.y + px
            startx = self.x + px
            for child in self.children:
                if child.visible:
                    child.draw(starty, startx, pattr)



    # Button. Provides click reaction
    class Button(UIElement):

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

    # Text line. Simplest UI.
    class TextLine(UIElement):

        def init(self, y = 0, x = 0, text = '', attr = Colors.FXNormal):
            text = text.replace('\n', '')

            self.y = y
            self.x = x
            self.height = 1
            self.width = len(text)
            self.Refresh()
            self.resizable = False


            self.attr = attr
            #Loghandler.Log(self.parent)

            def Refresh(self):
                self.content = [self.text]


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

            self.Resize(length, 1)

            self.visible = True
            self.interactable = True


        def Resize(self, height, width):
            dl = 0
            if self.vertical:
                dl = self.height - height
                self.height = height
            else:
                dl = self.width - width
                self.width = width
            if dl != 0:
                self.Refresh()

        def SetLength(self, length):
            dl = 0
            if self.vertical:
                dl = self.height - height
                self.height = length
            else:
                dl = self.width - width
                self.width = length
            if dl != 0:
                self.Refresh()

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


    # Single line input prompt of given width.
    class InputField(UIElement):

        def init(self, event = None, x = 0, y = 0, width = 24, border = True, style = None):
            if callable(event):
                self.user_event = event
            else:
                self.user_event = None

            self.text = ""
            self.cursor = 0
            self.selection = -1

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


        def Resize(self, height, width):
            self.border_visible = (self.border and (height >= 3 and width >= 2))
            self.height = 1 if height < 3 else 3
            self.SetWidth(width)

        def SetWidth(self, width):
            self.width = width
            self.Refresh()

        def Refresh(self):
            if not self.border_visible:
                if self.border:
                    self.content = [""]
                return

            self.content = [None, None, None]
            line = '─' * (self.width - 2)
            self.content[0] = '┌' +           line           + '┐'
            self.content[1] = '│' + (' ' * (self.width - 2)) + '│'
            self.content[2] = '└' +           line           + '┘'

        def GetText(self):
            return self.text
            

        def postdraw(self, starty, startx, attr):
            y = starty
            x = startx
            if self.border_visible:
                y += 1
                x += 1
            maxlen = self.width
            text = self.text

            attr = Colors.FXNormal
            if not self.border_visible:
                attr = attr | Colors.FXUnderline

            self.draw_func(y, x, text, attr)

            if self.canvas:
                if self.canvas.ui.keyboardFocus != self:
                    return

            if self.selection == -1:
                self.chgat_func(y, x + self.cursor, 1, Colors.FXReverse)
            else:
                p1 = self.cursor
                p2 = self.selection
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
                text_event = True
            elif key == Keys.KEY_BACKSPACE:
                if self.cursor > 0 and len(self.text) > 0:
                    self.text = self.text[:self.cursor - 1] + self.text[self.cursor:]
                    self.cursor -= 1
                text_event = True
            elif key == Keys.KEY_UP:
                self.cursor = 0
            elif key == Keys.KEY_DOWN:
                self.cursor = len(self.text)
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
                    ln = len(self.text)
                    if self.cursor > ln:
                        self.cursor = ln
                else:
                    self.cursor -= 1
                    if self.cursor < 0:
                        self.cursor = 0

            if text_event and self.user_event:
                self.user_event(self.text)
