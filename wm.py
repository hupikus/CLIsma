import sys
import os
import threading
import time

from mouse import Mice
from screen import Screen
from node import Node
from controller import Controller

class Wm:

	def newNode(self, parent_path, class_name, y, x, height, width, params):
		#node owes a window class
		parent_path += '.' + class_name + '.' + class_name
		node = Node(self.id, self, self.display, y, x, height, width, parent_path, class_name, params)
		self.nodes.append(node)
		self.order.append(self.id)
		self.id += 1
		self.orderlen += 1
		return node.win

	def closeNode(self, node):
		if not node.ready_to_close:
			node.win.abort()
		

	def delNode(self, node):
		del node.win
		#self.nodes.remove(node)
		self.nodes[node.id] = False
		self.order.remove(node.id)
		self.orderlen -= 1
		del node


	def shutdown(self):
		self.shutdown_ready = True


	def _mouse(self):
		while self.isMouse:
			#mouse_input
			self.mouse.process()

			#self.mouse_buttons = self.mouse.state

			self.mouse_delta_x = int(self.mouse.x) - self.control.mouse_x
			self.mouse_delta_y = int(self.mouse.y) - self.control.mouse_y
			self.control.mouse_lastx = self.control.mouse_x
			self.control.mouse_lasty = self.control.mouse_y
			self.control.mouse_x += self.mouse_delta_x
			self.control.mouse_y += self.mouse_delta_y

			self.holdelta += abs(self.mouse.dx) + abs(self.mouse.dy)
			#self.mouse.speed = min(max(self.mouse_speed * 0.7 + self.acc, self.mouse_speed * 0.7), self.mouse_speed * 1.8) * 0.6
			self.acc += (abs(self.mouse.dx + self.mouse.dy) * self.mouse_speed * 0.6 - self.acc) / 5

			self.hasDelta = True
			#mouse_display
			#if self.trail[1] != self.trail[0]:
			#	self.desktop.updateb(self.trail[2][1])
			#self.display.root.addstr(mouse_y, mouse_x, self.cursor_symbol[self.mouse_cursor])


	def __init__(self, display, inpd):

		#display
		self.screen_width = display.width
		self.screen_height = display.height
		self.display = display


		self.shutdown_ready = False

		#mouse
		#self.isMouse = os.path.exists("/dev/input/mice") or os.path.exists("/dev/input/mouse0")
		self.isMouse = len(inpd.mouses) > 0
		self.isMouse = True
		self.mouse_job = False
		if self.isMouse:
			self.cursor_symbol = {"base":"#", "select":"^", "text":"I", "resize_hor":"<>", "resize_ver":"^\nV"}
			self.holdout = 36
			self.mouse_cursor = "base"
			#self.mouse_speed = 0.8
			#self.mouse_speed = 0.44
			self.mouse_speed = 0.23
			self.mouse = Mice(self.screen_width, self.screen_height, self.mouse_speed, inpd)
			self.mouse_delta_x = 0
			self.mouse_delta_y = 0
			self.trail = [[0, 0], [0, 0], [0, 0]]
			self.mouse_buttons = [0, 0, 0]
			self.holdelta = 0
			self.acc = 0
			self.hasDelta = False
		else:
			self.mouse = 0

		#auto
		self.nodes = []
		self.id = 0
		self.error = 0
		self.control = Controller(self.mouse)

		#draw and click order
		self.order = []
		self.orderlen = 0

		#startup nodes
		#self.newNode(&Desktop)
		self.desktop = self.newNode("apps.default", "desktop", 0, 0, self.screen_height, self.screen_width, '')
		self.desktop.wm = self
		self.desktop.node.is_fullscreen = True

		self.newNode("apps.default", "default", 7, 7, 2, 65, '')
		#self.log = self.newNode("apps.default", "log", 18, 12, 5, 45, '')

		self.newNode("apps.default", "error", 18, 12, 5, 45, '-t "Stable Error"')

		#threading
		self.input_thread = threading.Thread(target=self._mouse)
		#mouse x and y delta. Not via evdev, but from /dev/input/mice. Mouse buttons from that file is often unreadable. Legacy
		self.input_thread.start()

		#window management
		self.moving_node = False
		self.move_type = -1

		#focus and focused input
		self.focus_id = 0




	def _mouse_draw(self):
		self.display.root.addstr(self.mouse.y, self.mouse.x, self.cursor_symbol[self.mouse_cursor])
		if self.mouse_delta_x and self.mouse_delta_y:
			self.trail[1] = self.trail[0]
			self.trail[0] = [self.control.mouse_x, self.control.mouse_y]
			self.display.root.addstr(self.trail[0][1], self.trail[0][0], self.cursor_symbol[self.mouse_cursor])
		return 0


#if mouse pressed (get mouse state from mouse class), do not handle clicked event untill click ends
#increment self mouse state till it became greater than hold timeout
#if not pressed anymore, set event handler to certain state
#0 ("none"), 1 ("clicked"), 2 ("hold"), 3 ("release"), 4 ("dragstart"), 5 ("drag"), 6 ("enddrag")
#only 1, 3, 4 and 6 are handler events
#for all 3 mouse buttons
#mouse wheel is in the input class
#pointer is in wm class because pointer is used to be a window, described in a method

	def _mouse_click(self):
		handler = [0, 0, 0]
		self.mouse.state_update()
		for i in range(3):
			if self.mouse.state[i] == 1:
				if self.control.mouse_buttons[i] == 0:
					self.mouse_buttons[i] = 1
					self.control.mouse_buttons[i] = 1
					handler[i] = 1
				elif self.control.mouse_buttons[i] == 1:
					self.mouse_buttons[i] = 2
					self.control.mouse_buttons[i] = 2
					self.holdelta = 0
				elif self.mouse_buttons[i] > self.holdout or self.holdelta > 2:
					if self.control.mouse_buttons[i] != 5:
						if self.control.mouse_buttons[i] == 2:
							self.control.mouse_buttons[i] = 4
							handler[i] = 4
						elif self.control.mouse_buttons[i] == 4:
							self.control.mouse_buttons[i] = 5
				else:
					self.mouse_buttons[i] += 1
			elif self.mouse_buttons[i] > 0:
				self.mouse_buttons[i] = 0
				if self.control.mouse_buttons[i] == 5:
					handler[i] = 6
					self.control.mouse_buttons[i] = 6
				else:
					handler[i] = 3
					self.control.mouse_buttons[i] = 3
			elif self.control.mouse_buttons[i] == 3 or self.control.mouse_buttons[i] == 6:
				self.mouse_buttons[i] = 0
				self.control.mouse_buttons[i] = 0
				handler[i] = -1

		focus_changed = False
		if handler[0] == 3:
			#left mouse button click
			for id in self.order[::-1]:
				node = self.nodes[id]
				if node:
					if self.mouse.y >= node.from_y - 1 and self.mouse.y <= node.to_y + 1 and self.control.mouse_x >= node.from_x and self.control.mouse_x <= node.to_x + 1:
						if self.mouse.y >= node.from_y:
							#click
							if self.focus_id != id:
								self.focus_id = id
								if id != 0:
									focus_changed = True
							node.click(0, self.mouse.y, self.mouse.x)
							break
						elif self.mouse.x == node.to_x:
							node.abort()
							break
		elif handler[0] == 1:
			#start of drag
			for id in self.order[::-1]:
				node = self.nodes[id]
				if node and not node.is_fullscreen and node.windowed:
					if self.mouse.x >= node.from_x and self.mouse.y == node.from_y - 1 and self.mouse.x < node.to_x:
						#focus and move
						if self.focus_id != id:
								self.focus_id = id
								if id != 0:
									focus_changed = True
						self.moving_node = node
						self.move_type = 0
						break
					elif self.mouse.y >= node.from_y - 1 and self.mouse.y < node.to_y and (self.mouse.x == node.to_x + 1 or self.mouse.x == node.from_x - 1):
						#focus and move right or left side
						if self.mouse.x == node.to_x + 1:
							self.move_type = 1
						else:
							self.move_type = 3

						if self.focus_id != id:
								self.focus_id = id
								if id != 0:
									focus_changed = True
						self.moving_node = node
						break
					elif self.mouse.x >= node.from_x and self.mouse.x <= node.to_x and self.mouse.y == node.to_y + 1:
						#focus and move bottom side
						if self.focus_id != id:
								self.focus_id = id
								if id != 0:
									focus_changed = True
						self.moving_node = node
						self.move_type = 2
						break

		elif self.moving_node and self.control.mouse_buttons[0] == 5 and self.hasDelta:
			if self.move_type == 0:
				#drag
				self.moving_node.move(self.mouse_delta_y, self.mouse_delta_x)
			elif self.move_type == 2:
				self.moving_node.reborder(2, self.mouse_delta_y)
			else:
				self.moving_node.reborder(self.move_type, self.mouse_delta_x)
		elif handler[0] == -1:
			self.moving_node = False
			self.move_type = -1
		

		if focus_changed:
			id_ind = self.order.index(self.focus_id)
			self.order[-1], self.order[id_ind] = self.order[id_ind], self.order[-1]


		#self.display.root.addstr(10, 5, str(self.mouse.state))
		self.display.root.addstr(10, 5, str(self.control.mouse_buttons))
		self.display.root.addstr(12, 5, str(self.mouse.relstate))
		self.hasDelta = False
		return 0


	def decoration(self, node):
		if not node.is_fullscreen and node.windowed:
			if node.from_y - 1 < self.screen_height:
				space = round((node.width / 2) - 0.5)
				bts = ''
				if node.width >= 3:
					bts = "- x"
				elif node.width > 1:
					bts = 'x'
				x_offcut = node.from_x
				if x_offcut < 0:
					x_offcut *= -1
					self.display.root.addstr(max(node.from_y - 1, 0), 0, ('_' * min(max(0, node.width - len(bts)), self.screen_width - node.from_x) + bts)[x_offcut:])
					#self.display.root.addstr(max(node.from_y - 1, 0), 0, (node.name.center(min(max(0, node.width - len(bts)), self.screen_width - node.from_x) - 1, '_') + bts)[x_offcut:])
				else:
					self.display.root.addstr(max(node.from_y - 1, 0), x_offcut, '_' * min(max(0, node.width - len(bts)), self.screen_width - node.from_x) + bts)
					#self.display.root.addstr(max(node.from_y - 1, 0), x_offcut, node.name.center(min(max(0, node.width - len(bts)), self.screen_width - node.from_x) - 10, '_') + bts)

	def abort(self):
		
		if self.isMouse:
			self.isMouse = False
			self.mouse.abort()
			self.input_thread._stop()
			#self.input_thread.join()


	def draw(self):
		#draw all nodes
		for id in self.order:
			node = self.nodes[id]
			if node:
				self.error += node.draw()
				self.decoration(node)

		#draw mouse
		if self.isMouse:
			self._mouse_click()
			self.error += self._mouse_draw()

		return self.error

	def process(self):

		#proces mouse buttons
		if self.isMouse:
			self._mouse_click()

		for id in self.order:
			node = self.nodes[id]
			if node:
				if node.ready_to_close:
					self.delNode(node)
				else:
					node.process()

		return self.error
