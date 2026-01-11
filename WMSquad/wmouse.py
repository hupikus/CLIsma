from type.colors import Colors
#import sys
from worldglobals import worldglobals as wg
from integration.loghandler import Loghandler
import curses

class WmMouse:

    def __init__(self, id, controller, display, wm, trailength, isReversed = False):
        self.id = id
        self.controller = controller
        self.control = controller[id]
        self.wm = wm

        self.display = display
        self.screen_height = display.height
        self.screen_width = display.width

        self.last_draw_y = 0
        self.last_draw_x = 0
        self.last_draw_attr = 0

        #customization
        self.speed = 1
        self.isReversed = isReversed
        self.update_trail(trailength)

        self.color = 0
        self.visible = False

        self.cursor_symbol = {"base":" ", "select":"^", "text":"I", "resize_hor":"<>", "resize_ver":"|"}
        self.hold_timeout = wg.hold_time * wg.inputrate
        self.mouse_cursor = "base"

        self.buttons = [0, 0, 0]
        self.hasDelta = False

        #node management
        self.moving_node = False
        self.move_type = -1
        self.drag_on_node = None

        #focus and focused input
        self.focus = None




    def draw(self):
        if not self.visible: return
        display = self.display

        for i in self.range[1]:
            self.trail[i] = self.trail[i - 1]
        self.trail[0] = (self.control.mouse_y, self.control.mouse_x)
        r = self.trailength
        if self.trail[0] == self.trail[r]: r = 0

        for i in range(r + 1):
            if i > 0 and self.trail[i] == self.trail[i - 1]: continue
            mouse_last_y = self.trail[i][0]
            mouse_last_x = self.trail[i][1]
            if mouse_last_x > self.wm.screen_width - 1: mouse_last_x = self.wm.screen_width - 1
            #sys.stdout.write(f"\033[{mouse_last_y};{mouse_last_x}H{'#'}")
            color = self.color
            attr = display.root.inch(mouse_last_y, mouse_last_x)
            attr_reversed = attr & Colors.FXReverse != 0

            pair_number = (attr & curses.A_COLOR) >> 8
            fg, bg = Colors.getPairColors(pair_number)            

            reverse = True

            if self.last_draw_y == mouse_last_y and self.last_draw_x == mouse_last_x:
                color = self.last_draw_attr
            else:
                self.last_draw_y = mouse_last_y
                self.last_draw_x = mouse_last_x

                if color == 0:
                    color = attr

                    if attr_reversed:
                        reverse = False
                        color = Colors.getColorPair(foreground = Colors.FXWhite, background = Colors.FXBlack)
                    elif pair_number == 63:
                        color = Colors.colorPair(56)
                    elif fg == bg:
                            color = Colors.getColorPair(foreground = Colors.FXBlack, background = bg)
                    elif pair_number == 37: # Fallback pair
                            color = Colors.FXNormal
                else:
                    cursor_pair = (color & curses.A_COLOR) >> 8
                    cursor_fg, cursor_bg = Colors.getPairColors(cursor_pair)
                    if (attr_reversed and cursor_fg == Colors.FXWhite) or (bg == cursor_fg):
                        reverse = False
                        color = Colors.getColorPair(foreground = Colors.FXWhite, background = Colors.FXBlack)

                if reverse:
                    color = color | Colors.FXReverse

                self.last_draw_attr = color

            display.root.chgat(mouse_last_y, mouse_last_x, 1, color)



    def input(self, delta):

        #aliases
        ctr = self.control
        wm = self.wm
        dev_id = self.id

        y_edge, x_edge = wm.decoration_preset.edgeThick
        y_head = wm.decoration_preset.headThick

        top_corner_size = wm.decoration_preset.topCornerRadius
        bottom_corner_size = wm.decoration_preset.bottomCornerRadius

        # Apply movement

        speed = delta * 100

        dy = ctr.mouse_dy * ctr.mouse_speed * speed
        dx = ctr.mouse_dx * ctr.mouse_speed * speed

        ctr.mouse_dy, ctr.mouse_dx = 0, 0

        ctr.mouse_ry = max(min(ctr.mouse_ry + dy, self.screen_height - 1), 0)
        ctr.mouse_rx = max(min(ctr.mouse_rx + dx, self.screen_width - 1), 0)
        ctr.mouse_y = round(ctr.mouse_ry)
        ctr.mouse_x = round(ctr.mouse_rx)

        ctr.mouse_rdy = ctr.mouse_y - ctr.mouse_last_y
        ctr.mouse_rdx = ctr.mouse_x - ctr.mouse_last_x

        ctr.mouse_last_y = ctr.mouse_y
        ctr.mouse_last_x = ctr.mouse_x

        self.hasDelta = ctr.mouse_rdy != 0 or ctr.mouse_rdx != 0
        if not self.visible and self.hasDelta:
            self.visible = True
        

        # Mouse buttons
        handler = [0, 0, 0]


        # 0:  "none"
        # 1:  "pressed"
        # 2:  "held"
        # 3:  "released" (sends "clicked")

        # 4:  "drag started" | "long hold started"
        # 5:  "drag"
        # 6:  "drag finished" | "long hold finished"

        # -1  (post-release)

        # 1, 3 and 4-6 provoke node events
        
        for i in range(3):
            if ctr.raw_mouse_buttons[i] == 1:

                if ctr.mouse_buttons[i] == 0:
                    self.buttons[i] = 1
                    ctr.mouse_buttons[i] = 1
                elif ctr.mouse_buttons[i] == 1:
                    self.buttons[i] = 2
                    ctr.mouse_buttons[i] = 2
                    self.hold_timeout = wg.hold_time * wg.inputrate

                elif self.hasDelta or self.buttons[i] > self.hold_timeout:

                    if ctr.mouse_buttons[i] != 5:

                        if ctr.mouse_buttons[i] == 2:
                            ctr.mouse_buttons[i] = 4
                        elif ctr.mouse_buttons[i] == 4:
                            ctr.mouse_buttons[i] = 5
                else:
                    self.buttons[i] += 1

                handler[i] = ctr.mouse_buttons[i]
            elif self.buttons[i] > 0:

                self.buttons[i] = 0
                if ctr.mouse_buttons[i] == 5:
                    ctr.mouse_buttons[i] = 6
                else:
                    ctr.mouse_buttons[i] = 3
                    wm.last_clicked = dev_id
                handler[i] = ctr.mouse_buttons[i]
            elif ctr.mouse_buttons[i] == 3 or ctr.mouse_buttons[i] == 6:
                self.buttons[i] = 0
                ctr.mouse_buttons[i] = 0
                handler[i] = -1



        my = ctr.mouse_y
        mx = ctr.mouse_x
        order = wm.order


        node = None
        node_id = -1

        if self.moving_node:
            node = self.moving_node
            node_id = order
        elif self.drag_on_node:
            node = self.drag_on_node
        else:
            # Loop through nodes in reverse draw order
            ig = 0
            with wm.lock:
                for node in reversed(order):
                    if not node or not node.interactable: continue
                    break_cycle = False

                    node_hover = (
                        my >= node.from_y - y_head and
                        my <= node.to_y + y_edge and

                        mx >= node.from_x - x_edge and
                        mx <= node.to_x + x_edge
                    )
                    #Loghandler.Log(f"ID {ig}: {node_hover}")
                    ig += 1
                    if node_hover:
                        break

            #Loghandler.Log(f"END: {node_id}")


        focus_changed = False
        for btn in range(3): # (1, 0, 2)
            mouse_event = handler[btn]
            #if mouse_event == 0 or mouse_event == -1: continue

            if node:
                win_hover = (
                    my >= node.from_y and
                    my <= node.to_y and

                    mx >= node.from_x and
                    mx <= node.to_x
                )

                border_hover = not win_hover

                corner_hover = False


                small_corners = (
                        (node.height + 2 < bottom_corner_size + top_corner_size) or
                        (node.width + 2 < max(top_corner_size, bottom_corner_size) * 2)
                    )
                if small_corners:
                    # Resort to 1 cell wide corners
                    corner_hover = (my < node.from_y or my > node.to_y) and (mx < node.from_x or mx > node.to_x)
                else:
                    corner_hover = border_hover and (
                        (
                            my <= node.from_y - y_head + top_corner_size - 1 and
                            (
                                mx <= node.from_x - x_edge + top_corner_size - 1 or
                                mx >= node.to_x + x_edge - top_corner_size + 1
                            )
                        ) or (
                            my >= node.to_y + y_edge - bottom_corner_size + 1 and
                            (
                                mx <= node.from_x - x_edge + bottom_corner_size - 1 or
                                mx >= node.to_x + x_edge - bottom_corner_size + 1
                            )
                        )
                    )

                side_hover = border_hover and not corner_hover


                head_hover = side_hover and (my < node.from_y)

                # Bring focus
                if mouse_event == 1 or mouse_event == 4:
                    if self.focus != node:
                        self.focus = node
                        focus_changed = True

                # On press: Prepare for drag, send event
                if mouse_event == 1:
                    if border_hover and btn == 0:
                        # Resize | Move
                        if not node.is_fullscreen and node.windowed:
                            horizontal_hover = (mx < node.from_x or mx > node.to_x)
                            bottom_hover = False
                            if small_corners:
                                bottom_hover = (my > node.to_y)
                            else:
                                bottom_hover = (my > node.from_y - y_head + top_corner_size)
                            right_hover = False

                            # Focus and move
                            self.moving_node = node
                            if bottom_hover:
                                self.move_type = 2
                                right_hover = (mx > node.from_x - x_edge + bottom_corner_size)
                            else:
                                self.move_type = 0
                                right_hover = (mx > node.from_x - x_edge + top_corner_size)

                            if border_hover and (horizontal_hover or corner_hover):
                                if side_hover:
                                    if right_hover:
                                        self.move_type = 1
                                    else:
                                        self.move_type = 3
                                else:
                                    # Change first digit
                                    # 00 -> 10/30; 02 -> 12/32
                                    if right_hover:
                                        self.move_type += 10
                                    else:
                                        self.move_type += 30
                    elif win_hover:
                        node.press(dev_id, btn, my, mx)

                # On click: Bring focus, send event
                elif mouse_event == 3:
                    if win_hover:
                        node.click(dev_id, btn, my, mx)
                    elif head_hover:
                        # Send click event to the decorator
                        if btn == 0: # Left button click
                            if ctr.mouse_x == node.to_x - 1:
                                Loghandler.Log("close " + node.app.name)
                                node.abort()
                            elif ctr.mouse_x == node.to_x - 3:
                                node.toggle_maximize()
                            elif ctr.mouse_x == node.to_x - 5:
                                node.hide(True)
                        elif btn == 2: # Middle button click
                            node.abort()
                            Loghandler.Log("close " + node.app.name)

                # On drag start: Bring focus, (send event | resize | drag)
                if mouse_event == 4:
                    if self.moving_node and btn == 0:
                        # Unmaximize
                        if self.moving_node.is_maximized:
                                self.moving_node.toggle_maximize()
                                self.moving_node.moveTo(-1, ctr.mouse_x - self.moving_node.width // 2)
                    elif win_hover:
                        node.drag(dev_id, btn, ctr.startDragEvent, my, mx)
                        self.drag_on_node = node

                elif mouse_event == 5:
                    if self.hasDelta or True:
                        if self.moving_node:
                            if btn == 0:
                                if self.move_type == 0:
                                    # Drag
                                    self.moving_node.move(ctr.mouse_rdy, ctr.mouse_rdx)
                                elif self.move_type == 2:
                                    self.moving_node.reborder(2, ctr.mouse_rdy)
                                elif self.move_type <= 3:
                                    self.moving_node.reborder(self.move_type, ctr.mouse_rdx)
                                else:
                                    self.moving_node.reborder(self.move_type // 10, ctr.mouse_rdx)
                                    self.moving_node.reborder(self.move_type % 10, ctr.mouse_rdy)
                        elif self.drag_on_node:
                            node.drag(dev_id, btn, ctr.dragEvent, my, mx)
                elif mouse_event == 6:
                    if self.drag_on_node:
                        node.drag(dev_id, btn, ctr.endDragEvent, my, mx)
                        self.drag_on_node = None
                    elif btn == 0 and self.moving_node:
                        self.moving_node = None

    
                # Scroll
                if ctr.mouse_wheel != 0:
                    if win_hover:
                        node.scroll(id, ctr.mouse_wheel)


        if handler[0] == -1:
            if self.moving_node and self.move_type == 0 and ctr.mouse_y == 0 and ctr.mouse_x < self.screen_width - 5:
                if not self.moving_node.is_maximized:
                    self.moving_node.toggle_maximize()
            self.moving_node = False
            self.move_type = -1


        if focus_changed:
            node_id = wm.order.index(self.focus)
            if node_id != 0:
                wm.order[-1], wm.order[node_id] = wm.order[node_id], wm.order[-1]

        wm.active[dev_id] = self.focus

        if node:
            node.input(delta, ctr)





    #settings
    def update_trail(self, length):
        self.trailength = length
        self.trail = [(0, 0) for i in range(length + 1)]

        #cache
        self.range = []
        if self.isReversed:
            self.range.append((1, 0, 2))
        else:
            self.range.append(range(3))
        self.range.append(range(length, 0, -1))

    def abort(self):
        pass
