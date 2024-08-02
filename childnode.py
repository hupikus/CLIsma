import sys
import os
import asyncio
import pydoc
from ui import UI
from apps.apps import App

class ChildNode:

	def __init__(self, id, wm, display, from_y, from_x, to_y, to_x, class_path, class_name):
		self.id = id
		self.wm = wm
		self.controller = self.wm.control
		self.display = display
		self.from_x = from_x
		self.from_y = from_y
		self.to_x = to_x
		self.to_y = to_y

		#app
		if class_path[:12] == "apps.default":
			self.app = App("default/" + class_name)
		else:
			self.app = App(class_name)


		#auto
		self.width = self.to_x - self.from_x
		self.height = self.to_y - self.from_y
		self.process_running = False
		self.ui = UI(self)
		self.is_fullscreen = False
		self.is_verfull = False


		#window class
		#cls = getattr(__import__(class_path), class_name)
		#mod = exec("from " + class_path + " import " + class_name)
		cls = pydoc.locate(class_path + '.' + class_name)
		self.win = cls(id, self, self.controller, self.height, self.width)
		if to_x == 0 and to_y == 0:
			self.to_x = self.win.preferred_width + from_x
			self.to_y = self.win.preferred_height + from_y

		self.windowed = True


		#controller
		controller = self.controller
		self.win.controller = controller
		if hasattr(self.win, "input_subscriptions"):
			subdata = self.win.input_subscriptions
			self.sub = {controller.MouseEvents:False, controller.KeyboardEvents:False}

			for type in subdata:
				self.sub[type] = True
		else:
			self.sub = False
		#finished

	def clear(self):
		self.tasks = []

	def appendStr(self, y, x, text):
		if y >= 0 and y <= self.height:
			oblen = min(len(text), self.width - x)
			if x >= 0 and x <= self.width:
				self.display.root.addstr(self.from_x + y, self.from_x + x, text[:oblen])
			elif x < 0:
				self.display.root.addstr(self.from_y + y, self.from_x, text[-x:oblen])

	def apply(self):
		self.display.root.refresh()


	def draw(self):
		try:
			self.win.draw()
		except:
			return 1
		return 0

	async def process(self):
		if not self.process_running:
			self.process_running = True

			try:
				self.win.process()
			except:
				return 1
			self.process_running = False
		return 0


#Window Manager Decoration

	def setKindness(self, id):
		if id == 0:
			self.windowed = False


#input listeners

	def click(self, button, x, y):
		if self.sub:
			if self.sub[self.controller.MouseEvents]:
				if self.ui.click(button, x, y):
					self.win.click(button, x, y)


