import os
import gc
import threading

from WMSquad.decoration import *
from type.permissions import Permisions

from WMSquad.screen import Screen
from NodeSquad.node import Node
from apps.app import App
from WMSquad.wmouse import WmMouse

from integration.loghandler import Loghandler

from worldglobals import worldglobals as wg

class Wm:

	def newNode(self, path, y, x, height, width, args = '', parent = None):
		# Focus to the new window
		if self.isMouse:
			self.active[self.last_clicked] = self.id
			self.pointers[self.last_clicked].focus_id = self.id

		node = Node(self.id, self, self.display, y, x, height, width, path, args, parent)
		with self.lock:
			self.order.append(node)
			self.id += 1
		return node

	def newNodeByApp(self, app, y, x, height, width, args = '', parent = None):
		# Focus to the new window
		if self.isMouse:
			self.active[self.last_clicked] = self.id
			self.pointers[self.last_clicked].focus_id = self.id

		node = Node(self.id, self, self.display, y, x, height, width, app.path, args, app, parent)
		with self.lock:
			self.order.append(node)
			self.id += 1
		return node

	def closeNode(self, node):
		if not node: return
		if not node.ready_to_close:
			node.win.abort()
		if node not in self.order: return

	def shutdown(self):
		for node in self.order:
			if node:
				node.abort()
		self.shutdown_ready = True


	def __init__(self, display, inpd, desktop):

		# Display
		self.screen_height = display.height
		self.screen_width = display.width
		self.display = display
		self.inpd = inpd

		self.shutdown_ready = False

		self.id = 0
		self.control = inpd.controller

		# Draw and click order
		self.order = []

		# Thread safety
		self.lock = threading.Lock()
		self.close_queue = []

		self.draw_as_maximized = False

		# Mouse
		self.isMouse = False

		self.last_clicked = 0
		self.pointers = []
		self.active = []

		# Prefs
		self.trailength = 2

		# Cursor
		self.pointer_count = 0
		inpd.listen_to_input(event_func = self.input, mouse_update_func = self.resize_pointers)
		self.hide_mouse_frames = 0

		# Effects
		self.transparent_effects = False
		self.decoration_preset = DecorationPreset()

		self.decoration_preset.SetStyle(DecorationStyle.all_sides)
		#self.decoration_preset.SetStyle(DecorationStyle.thick)

		self.accent = Colors.FXTextCyan

		# Compatibility
		self.fbmode = False


		# Startup nodes
		if desktop == "default":
			desktop = "default/desktop"
		self.desktop_name = desktop
		self.desktop = self.newNode(desktop, 0, 0, self.screen_height, self.screen_width, args = self)
		self.desktop.wm = self
		self.desktop.node.is_fullscreen = True




		Loghandler.Log("WM initialized")

		self.newNode("default/log", 18, 12, 8, 45, '')
		self.newNode("default/neoui", 4, 65, 25, 125)
		#self.newNode("default/default", 7, 7, 2, 65, '')
		#self.newNode("default/error", 18, 12, 5, 45, '-t "Stable Error"')

		# Init finished



	def getLock(self):
		return self.lock

	def resize_pointers(self, size):
		with self.lock:
			self.isMouse = size > 0
			self.pointer_count = size
			if self.isMouse:
				ln = len(self.active)

				self.control.resize_pointers(size)

				if ln < size:
					for id in range(ln, size):
						self.pointers.append(WmMouse(id, self))
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


	def requestPermission(self, permission):
		if permission == Permisions.INPUT_DEVICES:
			return self.inpd


	def resize_screen(self):
		height = self.display.height
		width = self.display.width
		self.draw_mouse = False
		self.screen_height = height
		self.screen_width = width

		for pointer in self.pointers:
			pointer.screen_height = height
			pointer.screen_width = width



		des = Node(0, self, self.display, 0, 0, height, width, "default/desktop", self)
		with self.lock:
			self.order[0] = des
		#self.delNode(self.desktop)
		self.desktop = des.win
		self.desktop.wm = self
		self.desktop.node.is_fullscreen = True


	def decoration(self, node):
		#top decoration
		if node and not node.is_fullscreen:
			if node.from_y - 1 < self.screen_height:
				self.decoration_preset.Draw(node, self)


	def draw(self, delta):
		# Draw all nodes
		if self.shutdown_ready: return 0
		if self.display.resize_wm_signal:
			self.resize_screen()
			self.display.resize_wm_signal = False
			self.hide_mouse_frames = 7
		elif self.hide_mouse_frames > 0:
			self.hide_mouse_frames -= 1

		self.draw_as_maximized = self.order[-1].is_maximized
		if self.draw_as_maximized:
			self.desktop.draw(delta)
			self.order[-1].draw(delta)
		else:
			for node in self.order:
				if node.from_x > self.screen_width - 1: continue
				if node and not node.hidden:
					node.draw(delta)
					#if node.is_maximized or node.is_fullscreen:
					#	continue
					self.decoration(node)

		# Compat
		if self.fbmode:
			y = 0
			addstr = self.display.root.addstr
			while y < self.screen_height:
				addstr(y, 0, '│')
				addstr(y, self.screen_width - 1, '│')
				y += 1


		# Draw mouse
		if self.isMouse and self.hide_mouse_frames == 0:
			try:
				for pointer in self.pointers:
					pointer.draw()
			except Exception as ex:
				Loghandler.Log(ex)

	def process(self, delta):
		for node in self.order:
			if node:
				if node.ready_to_close:
					pass
				else:
					node.process(delta)

	def input(self, delta):
		for pointer in self.pointers:
			pointer.input(delta)
