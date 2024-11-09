import sys
import os
import pydoc
from ui import UI
from apps.apps import App
from type.colors import Colors
import curses

class Node:

	def __init__(self, id, wm, display, from_y, from_x, height, width, class_path, class_name, params, app = None, parent = None):
		self.id = id
		self.wm = wm
		self.controller = wm.control
		self.display = display
		self.from_x = from_x
		self.from_y = from_y
		self.height = height
		self.width = width

		#avoid dumb crashes when smart developer is trying to call the node of the node
		self.node = self

		self.child_nodes = []

		self.parent = parent

		#app
		if app == None:
			if class_path[:12] == "apps.default":
				self.app = App("default/" + class_name)
			else:
				self.app = App(class_name)
		else:
			self.app = app

		if self.app.valid:
			self.name = self.app.name
		else:
			self.name = "App " + str(id)


		#auto
		self.to_y = self.from_y + self.height - 1
		self.to_x = self.from_x + self.width - 1


		if height == 0 and width == 0:
			if "prefHeight" in self.app.data and "prefWidth" in self.app.data:
				self.preferred_height = self.app.data["prefHeight"]
				self.preferred_width = self.app.data["prefWidth"]
			else:
				self.preferred_height, self.preferred_width, = 8, 45

			self.to_x = self.preferred_width + from_x - 1
			self.to_y = self.preferred_height + from_y - 1
			self.height = self.preferred_height
			self.width = self.preferred_width


		self.process_running = False
		self.ui = UI(self)
		self.is_fullscreen = False
		self.is_verfull = False


		#window class
		#cls = getattr(__import__(class_path), class_name)
		#mod = exec("from " + class_path + " import " + class_name)
		cls = pydoc.locate(class_path + '.' + class_name)
		self.win = cls(id, self, self.controller, self.height, self.width, params)
		

		self.min_height = 1
		self.max_height = self.wm.screen_height
		self.min_width = 1
		self.max_width = self.wm.screen_width
		#TODO: minimal size should be in .app file

		self.windowed = True
		if "windowed" in self.app.data:
			self.windowed = self.app.data["windowed"] == 1 and True or 0


		#controller
		controller = self.controller
		self.win.controller = controller
		if hasattr(self.win, "input_subscriptions"):
			subdata = self.win.input_subscriptions
			self.sub = {controller.MouseEvents:False, controller.MouseWheelEvents:False, controller.KeyboardEvents:False}

			for type in subdata:
				self.sub[type] = True
		else:
			self.sub = False


		#finished
		self.ready_to_close = False



	def clear(self):
		self.tasks = []

	#that sh is broken
	def appendStr_new(self, y, x, text, mode = Colors.FXNormal):
		if y >= 0 and y <= self.height and y >= -self.from_y and y + self.from_y < self.display.height - 1 and x < self.width and x + self.from_x < self.display_width - 1:
			if not self.isActive() and not self.isChildActive():
				mode = Colors.FXPale

			oblen = min(len(text), self.width - x, self.display.width - x - self.from_x)
			ln = len(text)
			x_offcut = -min(0, x)
			if self.from_x + x < 0:
				x_offcut -= self.from_x - 1

			if x_offcut < ln and oblen > x_offcut:
				self.display.root.addstr(self.from_y + y, self.from_x + x + x_offcut, text[x_offcut:oblen])
	
	def appendStr(self, y, x, text, mode = Colors.FXNormal):
		if y >= 0 and y <= self.height and y >= -self.from_y and y + self.from_y < self.display.height and x <= self.width and x + self.from_x < self.display.width - 1:

			if not self.isActive() and not self.isChildActive():
				mode = Colors.FXPale
			#x_offcut = -min(0, x)
			x_offcut = 0
			ln = len(text)
			oblen = max(min(ln, self.width - x, self.display.width - x - self.from_x), 1)

			if x < 0 or self.from_x + x < 0:
				if x < 0:
					x_offcut = -x
				if self.from_x + x < 0:
					x_offcut -= self.from_x - 1
				if x_offcut < ln:
					self.display.root.addstr(self.from_y + y, self.from_x + x + x_offcut, text[x_offcut:oblen], mode)
			else:
				self.display.root.addnstr(self.from_y + y, self.from_x + x, text, oblen, mode)

			#if x_offcut < ln and oblen > x_offcut:
				#self.display.root.addstr(self.from_y + y, self.from_x + x + x_offcut, text[x_offcut:oblen], mode)

	def move(self, y, x):
		self.from_y = min(max(self.from_y + y, 2), self.display.height - 1)
		self.from_x = min(max(self.from_x + x, 1 - self.width), self.display.width - 1)
		self.to_y = self.from_y + self.height - 1
		self.to_x = self.from_x + self.width - 1


	def reborder(self, side, delta):
		if side == 1:
			dd = max(min(self.width + delta, self.max_width), self.min_width)
			self.to_x += dd - self.width
			self.width = dd
		elif side == 2:
			dd = max(min(self.height + delta, self.max_height), self.min_height)
			self.to_y += dd - self.height
			self.height = dd
		elif side == 3:
			dd = max(min(self.width - delta, self.max_width), self.min_width)
			self.from_x -= dd - self.width
			self.width = dd
		self.win.onresize(self.height, self.width)


	def process(self):
		if not self.process_running:
			self.process_running = True
			try:
				self.win.process()
			except Exception as ex:
				self.abort()
				self.wm.newNode("apps.default", "error", 18, 12, 5, 45, f'-t "{self.app.name} process event closed with internal error: <c2> <tbold>' + str(ex) + '<endt> <endc>"')
			self.process_running = False

	def draw(self):
		try:
			self.win.draw()
			self.ui.draw()
		except Exception as ex:
			self.abort()
			self.wm.newNode("apps.default", "error", 18, 12, 5, 45, f'-t "{self.app.name} draw closed with internal error: <c2> <tbold>' + str(ex) + '<endt> <endc>"')



#Window Manager
	def newNode(self, parent_path, class_name, y, x, height, width, params):
		if len(self.child_nodes) > 13: return False

		if self.id != 0:
			newin = self.wm.newNode(parent_path, class_name, y, x, height, width, params, parent = self)
		else:
			newin = self.wm.newNode(parent_path, class_name, y, x, height, width, params)
		self.child_nodes.append(newin.node)
		return newin
	
	def newNodeByApp(self, app, y, x, height, width, params):
		if len(self.child_nodes) > 13: return False

		if self.id != 0:
			newin = self.wm.newNodeByApp(app, y + self.from_y, x + self.from_x, height, width, params, parent = self)
		else:
			newin = self.wm.newNodeByApp(app, y + self.from_y, x + self.from_x, height, width, params)
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

	def click(self, id, button, y, x):
		if self.sub:
			if self.ui.click(id, button, y - self.from_y, x - self.from_x):
				if self.sub[self.controller.MouseEvents]:
					self.win.click(id, button,  y - self.from_y, x - self.from_x)
	
	def drag(self, id, button, stage, y, x):
		if stage == 0:
			y -= self.from_y
			x -= self.from_x
		if self.sub:
			if self.ui.drag(id, button, stage, y, x):
				if self.sub[self.controller.MouseEvents]:
					self.win.drag(id, button, stage, y, x)
	
	def scroll(self, id, delta):
		if self.sub:
			#if self.ui.scroll(id, delta):
			if self.sub[self.controller.MouseWheelEvents]:
				self.win.scroll(id, delta)

	def abort(self):
		if self.parent and self in self.parent.child_nodes:
			self.parent.child_nodes.remove(self)
		self.win.abort()
		self.ready_to_close = True
	
#Conditions

	def isActive(self):
		return self.id == 0 or self.wm.focus_id == self.id
	
	def isChildActive(self):
		ret = False
		fi = self.wm.focus_id
		for node in self.child_nodes:
			if node:
				ret = ret or node.id == fi
		return ret

