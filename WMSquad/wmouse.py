
from type.colors import Colors
#import sys
from worldglobals import worldglobals as wg
from integration.loghandler import Loghandler

class WmMouse:

    def __init__(self, id, inpd, display, wm, trailength, isReversed = False):
        self.id = id
        self.inpd = inpd
        #self.control = inpd.controller[id]
        self.wm = wm

        self.display = display
        self.screen_height = display.height
        self.screen_width = display.width

        #customization
        self.isReversed = isReversed
        self.update_trail(trailength)

        self.color = 0

        #device
        self.mouse = inpd.mouse_class

        self.cursor_symbol = {"base":" ", "select":"^", "text":"I", "resize_hor":"<>", "resize_ver":"|"}
        self.holdout = wg.hold_time * wg.inputrate
        self.mouse_cursor = "base"

        self.buttons = [0, 0, 0]
        self.hasDelta = False

        self.control = inpd.listen_to_mouse(self.input, [id])

        #node management
        self.moving_node = False
        self.move_type = -1
        self.drag_on_node = -1

        #focus and focused input
        self.focus_id = 0




    def draw(self):
        for i in self.range[1]:
            self.trail[i] = self.trail[i - 1]
        self.trail[0] = (self.control.mouse_y, self.control.mouse_x)
        r = self.trailength
        if self.trail[0] == self.trail[r]: r = 0
        for i in range(r + 1):
            if i > 0 and self.trail[i] == self.trail[i - 1]: continue
            mouse_last_y = self.trail[i][0]
            mouse_last_x = self.trail[i][1]
            #sys.stdout.write(f"\033[{mouse_last_y};{mouse_last_x}H{'#'}")
            self.display.root.addstr(mouse_last_y, mouse_last_x, self.display.root.instr(mouse_last_y, mouse_last_x, 1), Colors.FXReverse | self.color)
            #self.display.root.addstr(mouse_last_y, mouse_last_x, '#')
        return 0



    def input(self):

        #aliases
        ctr = self.control
        wm = self.wm
        devid = self.id

        #mouse relativies

        dy = ctr.mouse_dy * ctr.mouse_speed
        dx = ctr.mouse_dx * ctr.mouse_speed

        ctr.mouse_dy, ctr.mouse_dx = 0, 0

        ctr.mouse_ry = max(min(ctr.mouse_ry + dy, self.screen_height - 1), 0)
        ctr.mouse_rx = max(min(ctr.mouse_rx + dx, self.screen_width - 1), 0)
        ctr.mouse_y = round(ctr.mouse_ry)
        ctr.mouse_x = round(ctr.mouse_rx)

        ctr.mouse_rdy = ctr.mouse_y - ctr.mouse_last_y
        ctr.mouse_rdx = ctr.mouse_x - ctr.mouse_last_x

        ctr.mouse_last_y = ctr.mouse_y
        ctr.mouse_last_x = ctr.mouse_x


        self.hasDelta = abs(ctr.mouse_rdy) + abs(ctr.mouse_rdx) != 0

        #mouse buttons
        handler = [0, 0, 0]


        #0 ("none"), 1 ("clicked"), 2 ("held"), 3 ("released"), 4 ("dragstarted"), 5 ("drag"), 6 ("dragended"), -1 ("post-release")
        #only 1, 3, 4 and 6 are handler events
        for i in self.range[0]:
            if ctr.raw_mouse_buttons[i] == 1:

                if ctr.mouse_buttons[i] == 0:
                    self.buttons[i] = 1
                    ctr.mouse_buttons[i] = 1
                    handler[i] = 1
                elif ctr.mouse_buttons[i] == 1:
                    self.buttons[i] = 2
                    ctr.mouse_buttons[i] = 2
                    self.holdout = wg.hold_time * wg.inputrate

                elif self.hasDelta or self.buttons[i] > self.holdout:

                    if ctr.mouse_buttons[i] != 5:

                        if ctr.mouse_buttons[i] == 2:
                            ctr.mouse_buttons[i] = 4
                            handler[i] = 4
                        elif ctr.mouse_buttons[i] == 4:
                            ctr.mouse_buttons[i] = 5
                else:
                    self.buttons[i] += 1

            elif self.buttons[i] > 0:

                self.buttons[i] = 0
                if ctr.mouse_buttons[i] == 5:
                    handler[i] = 6
                    ctr.mouse_buttons[i] = 6
                else:
                    handler[i] = 3
                    ctr.mouse_buttons[i] = 3
                    wm.last_clicked = devid
            elif ctr.mouse_buttons[i] == 3 or ctr.mouse_buttons[i] == 6:
                self.buttons[i] = 0
                ctr.mouse_buttons[i] = 0
                handler[i] = -1
        #end of buttons behaviour
        #Loghandler.Log(str(ctr.mouse_buttons))

        focus_changed = False
        for i in self.range[0]:
            if handler[i] == 3:
                #mouse click
                for id in wm.order[::-1]:
                    node = wm.nodes[id]
                    if node:
                        if ctr.mouse_y >= node.from_y - 1 and ctr.mouse_y <= node.to_y and ctr.mouse_x >= node.from_x and ctr.mouse_x <= node.to_x:
                            if self.focus_id != id:
                                self.focus_id = id
                                if id != 0:
                                    focus_changed = True
                            if ctr.mouse_y >= node.from_y:
                                #click
                                node.click(devid, i, ctr.mouse_y, ctr.mouse_x)
                                break
                            else:
                                if i == 0: # left button click
                                    if ctr.mouse_x == node.to_x:
                                        Loghandler.Log("close " + node.app.name)
                                        node.abort()
                                    elif ctr.mouse_x == node.to_x - 2:
                                        node.toggle_maximize()
                                    elif ctr.mouse_x == node.to_x - 4:
                                        node.hide(True)
                                elif i == 1: #right button click
                                    pass
                                else: # middle button click
                                    node.abort()
                                    Loghandler.Log("close " + node.app.name)
                            break

            elif handler[i] == 4:
                if self.moving_node:
                    #custom behaviour (like custom size) for startdrag event
                    if self.moving_node.is_maximized:
                            self.moving_node.toggle_maximize()
                            self.moving_node.moveTo(-1, ctr.mouse_x - (self.moving_node.width >> 1))
                    #end
                for id in wm.order[::-1]:
                    node = wm.nodes[id]
                    if ctr.mouse_y >= node.from_y and ctr.mouse_y <= node.to_y and ctr.mouse_x >= node.from_x and ctr.mouse_x <= node.to_x:
                        node.drag(id, i, ctr.startDragEvent, ctr.mouse_y, ctr.mouse_x)
                        #node.drag(id, i, ctr.dragEvent, ctr.mouse_rdy, ctr.mouse_rdx)
                        self.drag_on_node = node.id
                        #Loghandler.Log("node drag on " + str(node.id))
                        break

            elif self.drag_on_node >= 0:
                node = wm.nodes[self.drag_on_node]
                if node:
                    if ctr.mouse_buttons[i] == 5 and self.hasDelta:
                        node.drag(self.drag_on_node, i, ctr.dragEvent, ctr.mouse_rdy, ctr.mouse_rdx)
                    elif handler[i] == 6:
                        node.drag(self.drag_on_node, i, ctr.endDragEvent, ctr.mouse_rdy, ctr.mouse_rdx)
                        self.drag_on_node = -1
                    #if handler[i] == 6:

        if ctr.mouse_wheel != 0:
            for id in wm.order[::-1]:
                node = wm.nodes[id]
                if ctr.mouse_y >= node.from_y and ctr.mouse_y <= node.to_y and ctr.mouse_x >= node.from_x and ctr.mouse_x <= node.to_x + 1:
                    node.scroll(id, ctr.mouse_wheel)
                    break


        if handler[0] == 1:
            #start of drag
            for id in wm.order[::-1]:
                node = wm.nodes[id]
                breaky = False
                if node and not node.is_fullscreen and node.windowed:
                    if ctr.mouse_x >= node.from_x and ctr.mouse_y >= node.from_y and ctr.mouse_y <= node.to_y and ctr.mouse_x <= node.to_x:
                        break
                    else:
                        if ctr.mouse_x > node.from_x and ctr.mouse_y == node.from_y - 1 and ctr.mouse_x < node.to_x:
                            #focus and move
                            if self.focus_id != id:
                                    self.focus_id = id
                                    if id != 0:
                                        focus_changed = True
                            self.moving_node = node
                            self.move_type = 0
                            break
                        elif ctr.mouse_y >= node.from_y - 1 and ctr.mouse_y <= node.to_y + 1 and (ctr.mouse_x == node.to_x + 1 or ctr.mouse_x == node.from_x - 1):
                            #focus and move right or left side
                            if ctr.mouse_x == node.to_x + 1:
                                self.move_type = 1
                            else:
                                self.move_type = 3

                            if self.focus_id != id:
                                    self.focus_id = id
                                    if id != 0:
                                        focus_changed = True
                            self.moving_node = node
                            breaky = True
                        if ctr.mouse_x >= node.from_x - 1 and ctr.mouse_x <= node.to_x + 1 and ctr.mouse_y == node.to_y + 1:
                            #focus and move bottom side
                            if self.focus_id != id:
                                    self.focus_id = id
                                    if id != 0:
                                        focus_changed = True
                            if self.move_type == -1 or self.moving_node != node:
                                self.move_type = 2
                            elif self.move_type == 1:
                                self.move_type = 21
                            elif self.move_type == 3:
                                self.move_type = 23
                            else:
                                self.move_type = 2
                            self.moving_node = node
                            break
                if breaky:
                    break


        if self.moving_node and ctr.mouse_buttons[0] == 5 and self.hasDelta:
            if self.move_type == 0:
                #drag
                self.moving_node.move(ctr.mouse_rdy, ctr.mouse_rdx)
            elif self.move_type == 2:
                self.moving_node.reborder(2, ctr.mouse_rdy)
            else:
                self.moving_node.reborder(self.move_type % 10, ctr.mouse_rdx)
                if self.move_type > 20:
                    self.moving_node.reborder(2, ctr.mouse_rdy)
        elif handler[0] == -1:
            if self.moving_node and self.move_type == 0 and ctr.mouse_y == 0 and ctr.mouse_x < self.screen_width - 5:
                if not self.moving_node.is_maximized:
                    self.moving_node.toggle_maximize()
            self.moving_node = False
            self.move_type = -1


        if focus_changed:
            id_ind = wm.order.index(self.focus_id)
            wm.order[-1], wm.order[id_ind] = wm.order[id_ind], wm.order[-1]

        wm.active[devid] = self.focus_id

        return 0


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
