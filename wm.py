import os
import gc

from screen import Screen
from node import Node
from apps.apps import App

from loghandler import Loghandler
from type.colors import Colors

from worldglobals import worldglobals as wg

class Wm:

	def newNode(self, parent_path, class_name, y, x, height, width, params, parent = None):
		#node owes a window class
		parent_path += '.' + class_name + '.' + class_name
		if parent:
			node = Node(self.id, self, self.display, y, x, height, width, parent_path, class_name, params, parent = parent)
		else:
			node = Node(self.id, self, self.display, y, x, height, width, parent_path, class_name, params)
		self.nodes.append(node)
		self.order.append(self.id)
		self.focus_id = self.id
		self.id += 1
		self.orderlen += 1
		return node.win


	def newNodeByApp(self, app, y, x, height, width, params, parent = None):
		if parent:
			node = Node(self.id, self, self.display, y, x, height, width, app.parent_path, app.class_name, params, app = app, parent = parent)
		else:
			node = Node(self.id, self, self.display, y, x, height, width, app.parent_path, app.class_name, params, app = app)
		self.nodes.append(node)
		self.order.append(self.id)
		self.focus_id = self.id
		self.id += 1
		self.orderlen += 1
		return node.win

	def closeNode(self, node):
		if not node.ready_to_close:
			node.win.abort()

	def delNode(self, node):
		#self.nodes.remove(node)
		self.nodes[node.id] = False
		self.order.remove(node.id)
		self.orderlen -= 1
		del node
		gc.collect()


	def shutdown(self):
		for node in self.nodes:
			if node:
				node.abort()
		self.shutdown_ready = True


	def __init__(self, display, inpd):

		#display
		self.screen_height = display.height
		self.screen_width = display.width
		self.display = display


		self.shutdown_ready = False


		#auto
		self.nodes = []
		self.id = 0
		self.error = 0
		self.control = inpd.controller

		#draw and click order
		self.order = []
		self.orderlen = 0

		self.drag_on_node = {}
		self.node_draglen = 0

		#startup nodes
		#self.newNode(&Desktop)
		self.desktop = self.newNode("apps.default", "desktop", 0, 0, self.screen_height, self.screen_width, '')
		self.desktop.wm = self
		self.desktop.node.is_fullscreen = True

		#self.newNode("apps.default", "default", 7, 7, 2, 65, '')
		#self.newNode("apps.default", "log", 18, 12, 5, 45, '')

		#self.newNode("apps.default", "error", 18, 12, 5, 45, '-t "Stable Error"')
		#self.newNode("apps.default", "log", 18, 12, 5, 45, '')
		#self.newNode("apps.default", "colortest", 23, 14, 0, 0, '')

		#window management
		self.moving_node = False
		self.move_type = -1

		#focus and focused input
		self.focus_id = 0

		#mouse
		self.isMouse = inpd.isMouse

		if self.isMouse:
			self.mouse = inpd.mouse_class
			self.cursor_symbol = {"base":"#", "select":"^", "text":"I", "resize_hor":"<>", "resize_ver":"|"}
			self.holdout = wg.hold_time * wg.inputrate
			self.mouse_cursor = "base"

			self.trailength = 2
			self.trail = [(0, 0) for i in range(self.trailength + 1)]

			self.mouse_buttons = [0, 0, 0]
			self.acc = 0
			self.hasDelta = False

			self.mouse_count = 1

			inpd.listen_to_mouse(self._mouse_input)
		else:
			self.mouse = 0
		
		#temp
		self.key = -1




	def _mouse_draw(self):
		#self.display.root.addstr(self.control.mouse_y, self.control.mouse_x, self.cursor_symbol[self.mouse_cursor])
		#self.display.root.addstr(self.control.mouse_y, self.control.mouse_x, ' ', Colors.FXReverse)
		for i in range(self.trailength, 0, -1):
			self.trail[i] = self.trail[i - 1]
		self.trail[0] = (self.control.mouse_y, self.control.mouse_x)
		r = self.trailength
		if self.trail[0] == self.trail[r]: r = 0
		for i in range(r + 1):
			if i > 0 and self.trail[i] == self.trail[i - 1]: continue
			mouse_last_y = self.trail[i][0]
			mouse_last_x = self.trail[i][1]
			self.display.root.addstr(mouse_last_y, mouse_last_x, self.display.root.instr(mouse_last_y, mouse_last_x, 1), Colors.FXReverse)
			#self.display.root.addstr(mouse_last_y, mouse_last_x, '#')
		return 0


#if mouse pressed (get mouse state from mouse class), do not handle clicked event until click ends
#increment self mouse state till it became greater than hold timeout
#if not pressed anymore, set event handler to certain state
#0 ("none"), 1 ("clicked"), 2 ("hold"), 3 ("release"), 4 ("dragstart"), 5 ("drag"), 6 ("enddrag")
#only 1, 3, 4 and 6 are handler events
#for all 3 mouse buttons
#mouse wheel is in the input class


	def _mouse_input(self, id):

		#mouse relativies

		dy = self.control.mouse_dy * self.control.mouse_speed
		dx = self.control.mouse_dx * self.control.mouse_speed

		self.control.mouse_dy, self.control.mouse_dx = 0, 0


		self.control.mouse_ry = max(min(self.control.mouse_ry + dy, self.screen_height - 1), 0)
		self.control.mouse_rx = max(min(self.control.mouse_rx + dx, self.screen_width - 1), 0)
		self.control.mouse_y = round(self.control.mouse_ry)
		self.control.mouse_x = round(self.control.mouse_rx)

		self.control.mouse_rdy = self.control.mouse_y - self.control.mouse_last_y
		self.control.mouse_rdx = self.control.mouse_x - self.control.mouse_last_x

		self.control.mouse_last_y = self.control.mouse_y
		self.control.mouse_last_x = self.control.mouse_x



		#self.mouse.speed = min(max(self.mouse_speed * 0.7 + self.acc, self.mouse_speed * 0.7), self.mouse_speed * 1.8) * 0.6
		#self.acc += (abs(self.mouse.dx + self.mouse.dy) * self.mouse_speed * 0.6 - self.acc) / 5

		self.hasDelta = abs(self.control.mouse_rdy) + abs(self.control.mouse_rdx) != 0

		#mouse buttons
		handler = [0, 0, 0]
		for i in range(3):
			if self.mouse.state[i] == 1:
				if self.control.mouse_buttons[i] == 0:
					self.mouse_buttons[i] = 1
					self.control.mouse_buttons[i] = 1
					handler[i] = 1
				elif self.control.mouse_buttons[i] == 1:
					self.mouse_buttons[i] = 2
					self.control.mouse_buttons[i] = 2
					self.holdout = wg.hold_time * wg.inputrate
				elif self.hasDelta or self.mouse_buttons[i] > self.holdout:
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
		for i in range(3):
			if handler[i] == 3:
				#mouse click
				for id in self.order[::-1]:
					node = self.nodes[id]
					if node:
						if self.control.mouse_y >= node.from_y - 1 and self.control.mouse_y <= node.to_y and self.control.mouse_x >= node.from_x and self.control.mouse_x <= node.to_x + 1:
							if self.focus_id != id:
								self.focus_id = id
								if id != 0:
									focus_changed = True
							if self.control.mouse_y >= node.from_y:
								#click
								node.click(id, i, self.control.mouse_y, self.control.mouse_x)
								break
							elif i == 0:
								if self.control.mouse_x == node.to_x:
									Loghandler.Log("close " + node.app.name)
									node.abort()
								elif self.control.mouse_x == node.to_x - 2:
									node.toggle_maximize()
								elif self.control.mouse_x == node.to_x - 4:
									pass
									#node.hide()
								break
			elif handler[i] == 4:
				if self.moving_node:
					if self.moving_node.is_maximized:
							self.moving_node.toggle_maximize()
							self.moving_node.moveTo(-1, self.control.mouse_x - (self.moving_node.width >> 1))
				for id in self.order[::-1]:
					node = self.nodes[id]
					if self.control.mouse_y >= node.from_y and self.control.mouse_y <= node.to_y and self.control.mouse_x >= node.from_x and self.control.mouse_x <= node.to_x:
						node.drag(id, i, self.control.startDragEvent, self.control.mouse_y, self.control.mouse_x)
						node.drag(id, i, self.control.dragEvent, self.control.mouse_rdy, self.control.mouse_rdx)
						self.drag_on_node[node.id] = id
						self.node_draglen += 1
			elif self.node_draglen > 0:
				for id in self.order[::-1]:
					node = self.nodes[id]
					if node.id in self.drag_on_node and self.drag_on_node[node.id] == id:
						if self.control.mouse_buttons[i] == 5 and self.hasDelta:
							node.drag(id, i, self.control.dragEvent, self.control.mouse_rdy, self.control.mouse_rdx)
						elif handler[i] == 6:
							node.drag(id, i, self.control.endDragEvent, self.control.mouse_rdy, self.control.mouse_rdx)
							del self.drag_on_node[node.id]
							self.node_draglen -= 1
			#if handler[i] == 6:

		if self.control.mouse_wheel != 0:
			for id in self.order[::-1]:
				node = self.nodes[id]
				if self.control.mouse_y >= node.from_y and self.control.mouse_y <= node.to_y and self.control.mouse_x >= node.from_x and self.control.mouse_x <= node.to_x + 1:
					node.scroll(id, self.control.mouse_wheel)
					break


		if handler[0] == 1:
			#start of drag
			for id in self.order[::-1]:
				node = self.nodes[id]
				if node and not node.is_fullscreen and node.windowed:
					if self.control.mouse_x >= node.from_x and self.control.mouse_y == node.from_y - 1 and self.control.mouse_x < node.to_x:
						#focus and move
						if self.focus_id != id:
								self.focus_id = id
								if id != 0:
									focus_changed = True
						self.moving_node = node
						self.move_type = 0

						#custom behaviour (like custom size) for startdrag event
						#if node.is_maximized:
						#	node.toggle_maximize()
						#	node.moveTo(-1, self.control.mouse_x - (node.width >> 1))
						break
					elif self.control.mouse_y >= node.from_y - 1 and self.control.mouse_y <= node.to_y + 1 and (self.control.mouse_x == node.to_x + 1 or self.control.mouse_x == node.from_x - 1):
						#focus and move right or left side
						if self.control.mouse_x == node.to_x + 1:
							self.move_type = 1
						else:
							self.move_type = 3

						if self.focus_id != id:
								self.focus_id = id
								if id != 0:
									focus_changed = True
						self.moving_node = node
						#break
					if self.control.mouse_x >= node.from_x - 1 and self.control.mouse_x <= node.to_x + 1 and self.control.mouse_y == node.to_y + 1:
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

		if self.moving_node and self.control.mouse_buttons[0] == 5 and self.hasDelta:
			if self.move_type == 0:
				#drag
				self.moving_node.move(self.control.mouse_rdy, self.control.mouse_rdx)
			elif self.move_type == 2:
				self.moving_node.reborder(2, self.control.mouse_rdy)
			else:
				self.moving_node.reborder(self.move_type % 10, self.control.mouse_rdx)
				if self.move_type > 20:
					self.moving_node.reborder(2, self.control.mouse_rdy)
		elif handler[0] == -1:
		#That is post-release
			if self.moving_node and self.move_type == 0 and self.control.mouse_y == 0 and self.control.mouse_x < self.screen_width - 5:
				if not self.moving_node.is_maximized:
					self.moving_node.toggle_maximize()
			self.moving_node = False
			self.move_type = -1


		if focus_changed:
			id_ind = self.order.index(self.focus_id)
			self.order[-1], self.order[id_ind] = self.order[id_ind], self.order[-1]

		return 0


	def decoration(self, node):
		if node and not node.is_fullscreen and node.windowed:
			if node.from_y - 1 < self.screen_height:
				bts = ''
				ln = 0
				if node.width >= 3:
					if node.width >= 5:
						ln = 5
						bts = "- m x"
					else:
						ln = 3
						bts = "m x"
				elif node.width > 1:
					bts = 'x'
					ln = 1
				
				if node.width >= 5:
					text = '_' * ln + node.name.center(node.width - ln * 2, '_') + bts
				else:
					text = '_' * (node.width - ln) + bts

				x_offcut = node.from_x
				mxln = min(self.screen_width - x_offcut, node.width)
				if x_offcut < 0:
					x_offcut *= -1
					self.display.root.addstr(max(node.from_y - 1, 0), 0, text[x_offcut:mxln])
				else:
					self.display.root.addnstr(max(node.from_y - 1, 0), x_offcut, text, mxln)

				#bottom decoration
				t = True
				if t and node.to_y + 1 < self.screen_height:
					text = '-' * node.width
					x_offcut = node.from_x
					mxln = min(self.screen_width - x_offcut, node.width)
					if x_offcut < 0:
						x_offcut *= -1
						self.display.root.addstr(max(node.to_y + 1, 0), 0, text[x_offcut:mxln])
					else:
						self.display.root.addnstr(max(node.to_y + 1, 0), x_offcut, text, mxln)


	def draw(self):
		#draw all nodes
		for id in self.order:
			node = self.nodes[id]
			if node:
				node.draw()
				self.decoration(node)
				#if node.is_maximized or node.is_fullscreen:
				#	break

		#draw mouse
		if self.isMouse:
			#self.display.root.addstr(10, 5, str(self.key))

			self.error += self._mouse_draw()

		return self.error

	def process(self):
		for id in self.order:
			node = self.nodes[id]
			if node:
				if node.ready_to_close:
					self.delNode(node)
				else:
					node.process()
		
		#temp
		#self.keyboard_temp()

		return self.error
	

	#very temportary
	#def keyboard_temp(self):
	#	key = self.display.root.getch()
	#	self.key = key
	#	self.control.key = key
