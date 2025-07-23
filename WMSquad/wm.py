import os
import gc

from WMSquad.screen import Screen
from NodeSquad.node import Node
from apps.apps import App
from WMSquad.wmouse import WmMouse

from integration.loghandler import Loghandler
from type.colors import Colors

from worldglobals import worldglobals as wg

class Wm:

	def newNode(self, parent_path, class_name, y, x, height, width, params, parent = None):
		#sync active window
		if self.isMouse:
			self.active[self.last_clicked] = self.id
			self.pointers[self.last_clicked].focus_id = self.id
		#node owes a window class
		parent_path += '.' + class_name + '.' + class_name
		if parent:
			node = Node(self.id, self, self.display, y, x, height, width, parent_path, class_name, params, parent = parent)
		else:
			node = Node(self.id, self, self.display, y, x, height, width, parent_path, class_name, params)
		self.nodes.append(node)
		self.order.append(self.id)
		#self.focus_id = self.id
		self.id += 1
		self.orderlen += 1
		return node.win

	def newNodeByApp(self, app, y, x, height, width, params, parent = None):
		#sync active window
		if self.isMouse:
			self.active[self.last_clicked] = self.id
			self.pointers[self.last_clicked].focus_id = self.id

		if parent:
			node = Node(self.id, self, self.display, y, x, height, width, app.parent_path, app.class_name, params, app = app, parent = parent)
		else:
			node = Node(self.id, self, self.display, y, x, height, width, app.parent_path, app.class_name, params, app = app)
		self.nodes.append(node)
		self.order.append(self.id)
		#self.focus_id = self.id
		self.id += 1
		self.orderlen += 1
		return node.win

	def closeNode(self, node):
		if not node.ready_to_close:
			node.win.abort()

	def delNode(self, node):
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



	def __init__(self, display, inpd, desktop):

		#display
		self.screen_height = display.height
		self.screen_width = display.width
		self.display = display
		self.inpd = inpd

		self.shutdown_ready = False

		#auto
		self.nodes = []
		self.id = 0
		self.error = 0
		self.control = inpd.controller

		#draw and click order
		self.order = []
		self.orderlen = 0

		self.draw_as_maximized = False

		#mouse
		self.isMouse = False


		self.last_clicked = 0
		self.pointers = []
		self.active = []

		#prefs
		self.trailength = 2

		#cursor
		self.pointer_count = 0
		inpd.listen_to_mouse(event_func = self.mouseinput, update_func = self.resize_pointers)

		#startup nodes
		#self.newNode(&Desktop)
		if desktop == "default":
			desktop = "desktop"
		self.desktop = self.newNode("apps.default", desktop, 0, 0, self.screen_height, self.screen_width, self)
		self.desktop.wm = self
		self.desktop.node.is_fullscreen = True
		Loghandler.Log("WM initialized")

		#self.newNode("apps.default", "default", 7, 7, 2, 65, '')
		self.newNode("apps.default", "log", 18, 12, 5, 45, '')
		#self.newNode("apps.default", "error", 18, 12, 5, 45, '-t "Stable Error"')

		#init finished


	def resize_pointers(self, size):
		self.isMouse = size > 0
		self.pointer_count = size - 1
		if self.isMouse:
			ln = len(self.active)

			self.control.resize_pointers(size)

			if ln < size:
				for id in range(ln, size):
					self.pointers.append(WmMouse(id, self.control, self.display, self, self.trailength))
					self.active.append(0)
				if size - ln == 1:
					Loghandler.Log(f"Cursor with id {size - 1} connected")
				else:
					Loghandler.Log(f"Cursors with id [{ln}:{size - 1}] connected")
			elif ln > size:
				for id in range(size, ln):
					self.pointers[id].abort()
				self.active = self.active[:size]
				self.pointers = self.pointers[:size]
				if ln - size == 1:
					Loghandler.Log(f"Cursor with id {size} disconnected")
				else:
					Loghandler.Log(f"Cursors with id [{size}:{ln - 1}] disconnected")

	def mouseinput(self):
		for pointer in self.pointers:
			pointer.input()


	def decoration(self, node):
		#top decoration
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
					#sys.stdout.write(f"\033[{max(node.from_y - 1, 0)};{0}H{text[x_offcut:mxln]}")
					self.display.root.addstr(max(node.from_y - 1, 0), 0, text[x_offcut:mxln])
				else:
					self.display.root.addnstr(max(node.from_y - 1, 0), x_offcut, text, mxln)
					#sys.stdout.write(f"\033[{max(node.from_y - 1, 0)};{x_offcut}H{text[:mxln]}")

				#bottom decoration
				t = True
				if t and node.to_y + 1 < self.screen_height:
					text = '-' * node.width
					x_offcut = node.from_x
					mxln = min(self.screen_width - x_offcut, node.width)
					if x_offcut < 0:
						x_offcut *= -1
						#sys.stdout.write(f"\033[{max(node.to_y + 1, 0)};{0}H{text[x_offcut:mxln]}")
						self.display.root.addstr(max(node.to_y + 1, 0), 0, text[x_offcut:mxln])
					else:
						#sys.stdout.write(f"\033[{max(node.to_y + 1, 0)};{x_offcut}H{text[:mxln]}")
						self.display.root.addnstr(max(node.to_y + 1, 0), x_offcut, text, mxln)


	def draw(self, delta):
		#draw all nodes
		if self.shutdown_ready: return 0
		self.draw_as_maximized = self.nodes[self.order[-1]].is_maximized
		if self.draw_as_maximized:
			self.nodes[self.order[-1]].draw(delta)
			self.desktop.draw(delta)
		else:
			for id in self.order:
				node = self.nodes[id]
				if node and not node.hidden:
					node.draw(delta)
					#if node.is_maximized or node.is_fullscreen:
					#	continue
					self.decoration(node)
		#draw mouse
		if self.isMouse:
			#self.display.root.addstr(10, 5, str(self.active))
			for pointer in self.pointers:
				self.error += pointer.draw()

		return self.error

	def process(self, delta):
		for id in self.order:
			node = self.nodes[id]
			if node:
				if node.ready_to_close:
					self.delNode(node)
				else:
					node.process(delta)

		return self.error
