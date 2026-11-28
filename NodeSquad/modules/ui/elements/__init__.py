from type.colors import Colors
from integration.loghandler import Loghandler

class UIElement:
    """Parent class for UI element."""

    ui = None

    # Correct function to override.
    def init(self, *args, **kwargs):
        pass
    
    # Not this.
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

    # Public
    
    # This function makes UI element return its main value,
    # e.g. text in input field, press state in button, or position in slider.
    # Could be set as a reference to the function with more explicit name like GetText(), GetPosition();
    # This method should always work and never return garbage.
    def Get(self):
        return self.text

    # Add children to self
    def Add(self, ui):
        if isinstance(ui, UIElement):
            if ui.parent and ui in ui.parent.children:
                ui.parent.children.remove(ui)
            self.children.append(ui)

            ui.ui = self.ui
            ui.parent = self
            if self.is_canvas:
                ui.SetCanvas(self)
            else:
                ui.SetCanvas(self.canvas)


    # Change parent on self
    def SetParent(self, ui):
        if isinstance(ui, UIElement):
            ui.Add(self)

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

    # Simplified draw.
    def draw_children(self, py, px, pattr):
        starty = self.y + px
        startx = self.x + px
        for child in self.children:
            if child.visible:
                child.draw(starty, startx, pattr)

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

    # Simplified input.
    def input_children(self, py, px, controller, mouse_y, mouse_x):
        starty = self.y + px
        startx = self.x + px

        ray = False
        for child in reversed(self.children):
            if child.input(starty, startx, controller, mouse_y, mouse_x):
                ray = True
        
        return ray


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


from .canvas import Canvas
from .click_area import ClickArea
from .text import Text
from .button import Button
from .slider import Slider
from .radio_button import RadioButton
from .input_field import InputField
