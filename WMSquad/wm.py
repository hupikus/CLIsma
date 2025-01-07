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

				#mouse
		self.isMouse = inpd.isMouse


		if self.isMouse:
			#prefs
			self.trailength = 2

			#cursor
			self.pointer_count = 1
			self.pointers = []
			self.active = []

			for id in range(self.pointer_count):
				self.pointers.append(WmMouse(id, inpd, display, self, self.trailength))
				self.active.append(0)
		else:
			self.active = [0]

		#startup nodes
		#self.newNode(&Desktop)
		self.desktop = self.newNode("apps.default", "desktop", 0, 0, self.screen_height, self.screen_width, self)
		self.desktop.wm = self
		self.desktop.node.is_fullscreen = True

		#self.newNode("apps.default", "default", 7, 7, 2, 65, '')
		self.newNode("apps.default", "log", 18, 12, 5, 45, '')
		#self.newNode("apps.default", "error", 18, 12, 5, 45, '-t "Stable Error"')
		#self.newNode("apps.default", "colortest", 23, 14, 0, 0, '')


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
			self.display.root.addstr(10, 5, str(self.active))

			for pointer in self.pointers:
				self.error += pointer.draw()

		return self.error

	def process(self):
		for id in self.order:
			node = self.nodes[id]
			if node:
				if node.ready_to_close:
					self.delNode(node)
				else:
					node.process()

		return self.error
	
