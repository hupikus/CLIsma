import sys
import os
import pydoc
from ui import UI
from apps.apps import App


class Node:

	def __init__(self, id, wm, display, from_y, from_x, height, width, class_path, class_name):
		self.id = id
		self.wm = wm
		self.controller = self.wm.control
		self.display = display
		self.from_x = from_x
		self.from_y = from_y
		self.height = height
		self.width = width

		self.child_nodes = []
		
		#app
		if class_path[:12] == "apps.default":
			self.app = App("default/" + class_name)
		else:
			self.app = App(class_name)


		#auto
		self.to_y = self.from_y + self.height - 2
		self.to_x = self.from_x + self.width - 2
		self.process_running = False
		self.ui = UI(self)
		self.is_fullscreen = False
		self.is_verfull = False


		#window class
		#cls = getattr(__import__(class_path), class_name)
		#mod = exec("from " + class_path + " import " + class_name)
		cls = pydoc.locate(class_path + '.' + class_name)
		self.win = cls(id, self, self.controller, self.height, self.width)
		if height == 0 and width == 0:
			self.to_x = self.win.preferred_width + from_x - 1
			self.to_y = self.win.preferred_height + from_y - 1
			self.height = self.win.preferred_height
			self.width = self.win.preferred_width
		#TODO: preferred size should be in .app file

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
		self.ready_to_close = False



	def clear(self):
		self.tasks = []

	def appendStr(self, y, x, text):
		if y >= 0 and y <= self.height and y >= -self.from_y and y + self.from_y < self.display.height - 1:
			oblen = min(len(text), self.width - x, self.display.width - x - self.from_x)
			ln = len(text)
			x_offcut = -min(0, x)
			if self.from_x + x < 0:
				x_offcut -= self.from_x - 1

			if x_offcut < ln and oblen > x_offcut:
				self.display.root.addstr(self.from_y + y, self.from_x + x + x_offcut, text[x_offcut:oblen])

	def apply(self):
		self.display.root.refresh()


	def draw(self):
		#try:
		self.win.draw()
		#except:
		#	return 1
		self.ui.draw()
		return 0

	def move(self, y, x):
		self.from_y = min(max(self.from_y + y, 2), self.display.height - 1)
		self.from_x = min(max(self.from_x + x, 1 - self.width), self.display.width - 1)
		self.to_y = self.from_y + self.height - 1
		self.to_x = self.from_x + self.width - 1





	def process(self):
		if not self.process_running:
			self.process_running = True

			try:
				self.win.process()
			except:
				return 1
			self.process_running = False
		return 0



#Window Manager
	def newNode(self, parent_path, class_name, y, x, height, width):
		if len(self.child_nodes) > 13: return False

		newin = self.wm.newNode(parent_path, class_name, y, x, height, width)
		self.child_nodes.append(newin.node)
		return newin


	def closeNode(self, node):
		self.child_nodes.remove(node)
		if node != self:
			node.abort()

#Window Manager Decoration

	def setKindness(self, id):
		if id == 0:
			self.windowed = False


#input listeners

	def click(self, button, x, y):
		if self.sub:
			if self.sub[self.controller.MouseEvents]:
				if self.ui.click(button, x - self.from_x, y - self.from_y):
					self.win.click(button, x - self.from_x, y - self.from_y)



	def abort(self):
		self.win.abort()
		self.ready_to_close = True

