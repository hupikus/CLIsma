import sys
import os
import pydoc
import traceback

from NodeSquad.ui import UI
from apps.apps import App
from type.colors import Colors
from integration.loghandler import Loghandler

class Node:

	__slots__ = ("id", "name", "wm", "controller", "display", "from_y", "from_x", "to_y", "to_x", "height", "width", "preferred_height", "preferred_width", "display_height", "display_width", "node", "child_nodes", "parent", "app", "process_running", "ui", "is_fullscreen", "is_maximized", "win", "min_height", "max_height", "min_width", "max_width", "windowed", "sub", "ready_to_close", "isDoomed", "tasks", "oldsize", "root")
	def __init__(self, id, wm, display, from_y, from_x, height, width, class_path, class_name, params, app = None, parent = None):
		self.id = id
		self.wm = wm
		self.controller = wm.control
		self.display = display
		self.from_y = from_y
		self.from_x = from_x
		self.height = height
		self.width = width

		self.oldsize = (self.height, self.width, self.from_y, self.from_x)

		self.display_height = self.display.height
		self.display_width = self.display.width

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
		self.is_maximized = False


		#window class
		#cls = getattr(__import__(class_path), class_name)
		#mod = exec("from " + class_path + " import " + class_name)	
		cls = False
		ex = False
		try:
			cls = pydoc.locate(class_path + '.' + class_name)
		except Exception as exc:
			ex = exc
		if cls:
			try:
				self.win = cls(id, self, self.controller, self.height, self.width, params)
			except Exception as ex:
				_, _, tb = sys.exc_info()
				cls = pydoc.locate("apps.default" + ".error" * 3)
				self.win = cls(id, self, self.controller, self.height, self.width, f'-t "{self.app.name} closed at start with internal error: <c2> <tbold>' + str(ex) + '<endt> <endc> (at line ' + str(tb.tb_lineno) + ')"')
				Loghandler.Log(str(tb.tb_lineno))
		else:
			cls = pydoc.locate("apps.default" + ".error" * 3)
			self.win = cls(id, self, self.controller, self.height, self.width, f'-t "{self.app.name} is unreachable: <c2> <tbold>' + "Class " + class_path + " does not exist (" + str(ex) + ')' + '<endt> <endc>"')
			

		self.min_height = 1
		self.max_height = 999
		self.min_width = 1
		self.max_width = 999
		#TODO: minimal size should be in .app file

		self.windowed = True
		if "windowed" in self.app.data:
			self.windowed = self.app.data["windowed"] == 1 and True or 0


		#controller
		controller = self.controller
		if hasattr(self.win, "input_subscriptions"):
			subdata = self.win.input_subscriptions
			self.sub = {controller.MouseEvents:False, controller.MouseWheelEvents:False, controller.KeyboardEvents:False}
			for type in subdata:
				self.sub[type] = True
		else:
			self.sub = False


		#cache
		self.root = self.display.root

		#finished
		self.ready_to_close = False
		self.isDoomed = False



	def clear(self):
		self.tasks = []


	#classic
	def appendStr_old(self, y, x, text, mode = Colors.FXNormal):
		fromy = self.from_y
		fy = y + fromy
		fromx = self.from_x
		fx = x + fromx
		if y >= 0 and y <= self.height and fy >= 0 and fy < self.display_height and x <= self.width and fx < self.display_width - 1:

			if self.id != 0 and not self.isActive() and not self.isChildActive():
				mode = Colors.FXPale
			#x_offcut = -min(0, x)
			x_offcut = 0
			ln = len(text)
			oblen = max(min(ln, self.width - x, self.display.width - x - fromx), 1)

			if x < 0 or fx < 0:
				if x < 0:
					x_offcut = -x
				else:
					x_offcut -= fromx
				if x_offcut < ln:
					self.display.root.addstr(fy, fx + x_offcut, text[x_offcut:oblen], mode)
			else:
				self.display.root.addnstr(fy, fx, text, oblen, mode)


	#i tried to over-optimize
	def appendStr(self, y, x, text, mode = Colors.FXNormal):
		fromy = self.from_y
		fy = y + fromy
		fromx = self.from_x
		fx = x + fromx

		#if y >= 0 and y <= self.height and fy >= 0 and fy < self.display_height and x <= self.width and fx < self.display_width - 1:
		if 0 <= y <= self.height and 0 <= fy < self.display_height and x <= self.width and fx < self.display_width - 1:
			if self.id != 0 and not self.isActive() and not self.isChildActive():
				mode = Colors.FXPale
			x_offcut = 0
			ln = len(text)
			oblen = max(min(ln, self.width - x, self.display_width - x - fromx), 1)


			if x < 0 or fx < 0:
				if x < 0:
					x_offcut = -x
				else:
					x_offcut -= fromx
				if x_offcut < ln:
					self.root.addstr(fy, fx + x_offcut, text[x_offcut:oblen], mode)
			else:
				self.root.addnstr(fy, fx, text, oblen, mode)



	#properties

	def move(self, y, x):
		self.from_y = min(max(self.from_y + y, 2), self.display.height - 1)
		self.from_x = min(max(self.from_x + x, 1 - self.width), self.display.width - 1)
		self.to_y = self.from_y + self.height - 1
		self.to_x = self.from_x + self.width - 1
	
	def moveTo(self, y, x):
		if y >= 0:
			self.from_y = min(y, self.display.height - 1)
			self.to_y = self.from_y + self.height - 1
		if x > -1798:
			self.from_x = min(max(x, 1 - self.width), self.display.width - 1)
			self.to_x = self.from_x + self.width - 1


	def reborder(self, side, delta):
		if self.isDoomed: return 0
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
		if self.isDoomed: return 0
		if not self.process_running:
			self.process_running = True
			try:
				self.win.process()
			except Exception as ex:
				self.abort()
				self.wm.newNode("apps.default", "error", 18, 12, 5, 45, f'-t "{self.app.name} process event closed with internal error: <c2> <tbold>' + str(ex) + '<endt> <endc>"')
			self.process_running = False

	def draw(self):
		if self.isDoomed: return 0
		try:
			self.win.draw()
			self.ui.draw()
		except Exception as ex:
			self.abort()
			self.wm.newNode("apps.default", "error", 18, 12, 5, 45, f'-t "{self.app.name} draw closed with internal error: <c2> <tbold>' + str(ex) + '<endt> <endc>"')
	
	def toggle_maximize(self):
		if self.is_maximized:
			self.height, self.width, self.from_y, self.from_x = self.oldsize
		else:
			self.oldsize = (self.height, self.width, self.from_y, self.from_x)
			self.height = self.wm.screen_height - 1
			self.width = self.wm.screen_width
			self.from_y = 1
			self.from_x = 0

		self.to_y = self.from_y + self.height - 1
		self.to_x = self.from_x + self.width - 1

		self.is_maximized = not self.is_maximized
		self.win.onresize(self.height, self.width)



#Window Manager
	def newNode(self, parent_path, class_name, y, x, height, width, params):
		if self.isDoomed: return 0
		if self.id > 0 and len(self.child_nodes) > 13: return False

		if self.id != 0:
			newin = self.wm.newNode(parent_path, class_name, y, x, height, width, params, parent = self)
		else:
			newin = self.wm.newNode(parent_path, class_name, y, x, height, width, params)
		self.child_nodes.append(newin.node)
		return newin
	
	def newNodeByApp(self, app, y, x, height, width, params):
		if self.isDoomed: return 0
		if self.id > 0 and len(self.child_nodes) > 13: return False

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

	def click(self, device_id, button, y, x):
		if self.sub:
			if self.ui.click(device_id, button, y - self.from_y, x - self.from_x):
				if self.sub[self.controller.MouseEvents]:
					self.win.click(device_id, button,  y - self.from_y, x - self.from_x)
	
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
		self.isDoomed = True
		if self.parent and self in self.parent.child_nodes:
			self.parent.child_nodes.remove(self)
		self.win.abort()
		try:
			del self.win
		finally:
			del self.ui
		self.ready_to_close = True
	
#Conditions

	def isActive(self):
		return self.id in self.wm.active
	
	def isChildActive(self):
		ret = False
		fi = self.wm.active
		for node in self.child_nodes:
			if node:
				ret = ret or node.id in fi
		return ret

