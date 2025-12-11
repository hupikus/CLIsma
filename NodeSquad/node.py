import sys
import os
import pydoc
import traceback

from type.colors import Colors
from type.permissions import Permisions

from NodeSquad.ui import UI
from NodeSquad.ui_new import UI as neoUI
from apps.apps import App
from integration.loghandler import Loghandler

class Node:

	__slots__ = ("id", "name", "wm", "controller", "display", "hidden", "from_y", "from_x", "to_y", "to_x", "height", "width", "preferred_height", "preferred_width", "display_height", "display_width", "node", "child_nodes", "parent", "app", "process_running", "ui", "neoui", "is_fullscreen", "is_maximized", "win", "min_height", "max_height", "min_width", "max_width", "windowed", "sub", "ready_to_close", "closing", "tasks", "oldsize", "root", "addstr", "addnstr", "chgat", "accent") #fixed size fields is faster
	def __init__(self, id, wm, display, from_y, from_x, height, width, class_path, class_name, params, app = None, parent = None):
		self.id = id
		self.wm = wm
		self.controller = wm.control
		self.display = display
		self.hidden = False
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
			elif class_path[:13] == "apps.external":
				self.app = App("external/" + class_name)
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
				self.preferred_height, self.preferred_width, = 14, 45

			self.to_x = self.preferred_width + from_x - 1
			self.to_y = self.preferred_height + from_y - 1
			self.height = self.preferred_height
			self.width = self.preferred_width


		self.process_running = False
		self.is_fullscreen = False
		self.is_maximized = False


		# Appearance
		self.accent = wm.accent

		# Modules
		self.ui = UI(self)
		self.neoui = neoUI(self)


		# Window class
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
				self.win = cls(id, self, self.controller, self.height, self.width, f'-t "{self.app.name} closed at start with internal error: <c2> <tbold>' + str(traceback.format_exc()) + '<endt> <endc> (at line ' + str(tb.tb_lineno) + ')"')
				Loghandler.Log(str(tb.tb_lineno))
		else:
			cls = pydoc.locate("apps.default" + ".error" * 3)
			self.win = cls(id, self, self.controller, self.height, self.width, f'-t "{self.app.name} is unreachable: <c2> <tbold>' + "Class " + class_path + " does not exist (" + str(traceback.format_exc()) + ')' + '<endt> <endc>"')


		self.min_height = 1
		self.max_height = 999
		self.min_width = 9
		self.max_width = 999
		# TODO: size constrains should be in .app file

		self.windowed = True
		if "windowed" in self.app.data:
			self.windowed = self.app.data["windowed"] == 1 and True or 0


		# Controller
		controller = self.controller
		self.sub = {}
		if hasattr(self.win, "input_subscriptions"):
			subdata = self.win.input_subscriptions
			for type in subdata:
				self.sub[type] = True
				controller.listenEvent(self, type)


		# Cache
		self.root = self.display.root
		self.addstr = self.root.addstr
		self.addnstr = self.root.addnstr
		self.chgat = self.root.chgat

		# Finished
		self.ready_to_close = False
		self.closing = False

	#public

	def errorMessage(self, eventname, ex):
		write_error = True
		if write_error:
			try:
				with open("error.txt", "w") as f:
					f.write(str(traceback.format_exc()))
			except:
				pass
		self.wm.newNode("apps.default", "error", 18, 12, 5, 45, f'-t "{self.app.name} {eventname} event closed with internal error: <c2> <tbold>' + str(traceback.format_exc()) + '<endt> <endc>"')
		self.abort()


	def clear(self, attr = Colors.FXNormal, char = ' ', margin_top = 0, margin_bottom = 0):
		fx = max(0, self.from_x)
		w = self.display_width
		if fx > w - 1: return
		s = char * (min(self.to_x - fx, w - 1 - fx) + 1)
		y = max(0, self.from_y + margin_top)
		my = min(self.to_y + 1 - margin_bottom,  self.display_height)
		while y < my:
			self.root.addstr(y, fx, s, attr)
			y += 1


	# assembly code will only make positive difference by referencing "var = self.var" 4 and more uses

	def appendStr_old(self, y, x, text, attr = Colors.FXNormal):
		fromy = self.from_y
		fy = y + fromy
		fromx = self.from_x
		fx = x + fromx

		if 0 <= y < self.height and 0 <= fy < self.display_height and x <= self.width and fx < self.display_width - 1:
			x_offcut = 0
			ln = len(text)
			oblen = max(min(ln, self.width - x, self.display_width - x - fromx), 1)


			if x < 0 or fx < 0:
				#if x < 0:
				#	x_offcut = -x
				if fx < 0:
					x_offcut -= fx
				else:
					x_offcut = -x
				if x_offcut < ln:
					self.root.addstr(fy, fx + x_offcut, text[x_offcut:oblen], attr)
			else:
				self.root.addnstr(fy, fx, text, oblen, attr)

	# This refactor is generally 1.5-2 times faster but may contain bugs

	def appendStr(self, y, x, text, attr = Colors.FXNormal):
		if y < 0 or y >= self.height: return
		fromy = y + self.from_y
		if fromy < 0 or fromy >= self.display_height: return
		if x >= self.width: return
		fromx = self.from_x + x
		if fromx >= self.display_width: return

		ln = len(text)
		new_ln = ln

		l_offcut = 0
		r_offcut = ln

		if fromx < 0:
			l_offcut -= fromx
			x -= fromx
			new_ln += fromx
			fromx = 0

		if fromx + new_ln >= self.display_width:
			d = (fromx + new_ln) - self.display_width
			r_offcut -= d
			new_ln -= d


		if x < 0:
			l_offcut -= x
			fromx -= x
			new_ln += x
			x = 0

		if x + new_ln >= self.width:
			r_offcut -= (x + new_ln) - self.width
			# new_ln -= (x + new_ln) - self.width ; but this is unneccesary


		if l_offcut == 0 and r_offcut == ln:
			self.addstr(fromy, fromx, text, attr)
		if l_offcut >= r_offcut:
			return
		else:
			self.addstr(fromy, fromx, text[l_offcut:r_offcut], attr)




	# Method looks finished but isnt tested

	def setAttr(self, y, x, num, attr):
		if y < 0 or y >= self.height: return
		fromy = y + self.from_y
		if fromy < 0 or fromy >= self.display_height: return
		if x >= self.width: return
		fromx = self.from_x + x
		if fromx >= self.display_width: return

		if fromx < 0:
			x -= fromx
			num += fromx
			fromx = 0

		if fromx + num >= self.display_width:
			num = self.display_width - fromx


		if x < 0:
			fromx -= x
			num += x
			x = 0

		if x + num >= self.width:
			num = self.width - x

		if num <= 0: return

		self.chgat(fromy, fromx, num, attr)


	def setAttr_old(self, y, x, num, attr):
		fromy = self.from_y
		fy = y + fromy
		fromx = self.from_x
		fx = x + fromx

		if 0 <= y < self.height and 0 <= fy < self.display_height and x <= self.width and fx < self.display_width - 1:
			x_offcut = 0
			oblen = max(min(num, self.width - x, self.display_width - x - fromx), 1)


			if x < 0 or fx < 0:
				if fx < 0:
					x_offcut = -fx
				else:
					x_offcut = -x
				if x_offcut < num:
					self.root.chgat(fy, fx + x_offcut, oblen - x_offcut, attr)
			else:
				self.root.chgat(fy, fx, oblen, attr)



	def writeStr(self, y, x, text, attr = Colors.FXNormal):
		nfo = text.count('\n')
		if nfo > 0:
			calls = text.split('\n')
			if y <= self.height:
				i = 0
				if y < 0:
					lc = min(nfo + 1, self.height)
					if -y < lc: return 0
					i = -y
				else:
					lc = min(nfo + 1, self.height - y)

				for n in range(i, lc):
					self.appendStr(y + n, x, '', attr)
					sys.stdout.write(calls[n])
					#self.appendStr(y + n, x, calls[n].expandtabs(), attr)

		else:
			self.appendStr(y, x, text, attr)


	def requestPermission(self, permission):
		return self.wm.requestPermission(permission)


	def isActive(self):
		return self.id in self.wm.active

	def isChildActive(self):
		ret = False
		fi = self.wm.active
		for node in self.child_nodes:
			if node:
				ret = ret or node.id in fi
		return ret


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
		if self.closing: return 0
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

	def resize(self, height, width):
		self.to_y = self.from_y + height - 1
		self.to_x = self.from_x + width - 1
		self.height = height
		self.width = width


	def process(self, delta):
		if self.closing: return 0
		if not self.process_running:
			self.process_running = True
			try:
				self.win.process(delta)
			except Exception as ex:
				self.errorMessage("process", ex)
			self.process_running = False

	def draw(self, delta):
		if self.closing or self.hidden: return 0
		try:
			self.win.draw(delta)
			self.ui.draw()
			self.neoui.draw(delta)
		except Exception as ex:
			self.errorMessage("draw", ex)

	def input(self, delta, controller):
		if self.closing or self.hidden: return False
		mx = controller.mouse_x
		my = controller.mouse_y
		if mx > self.to_x or mx < self.from_x or my < self.from_y or my > self.to_y:
			return False

		try:
			self.win.mouse(delta, controller)
			self.neoui.input(delta, controller)
		except Exception as ex:
			self.errorMessage("input", ex)
		return True



	def toggle_maximize(self):
		if self.closing: return 0
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


	def hide(self, state):
		if self.closing: return 0
		self.hidden = state
		try:
			self.win.oncollapse(state)
		except Exception as ex:
			self.errorMessage("collapse", ex)

#Window Manager
	def newNode(self, parent_path, class_name, y, x, height, width, params):
		if self.closing: return 0
		if self.id > 0 and len(self.child_nodes) > 13: return False

		if self.id != 0:
			newin = self.wm.newNode(parent_path, class_name, y, x, height, width, params, parent = self)
		else:
			newin = self.wm.newNode(parent_path, class_name, y, x, height, width, params)
		self.child_nodes.append(newin.node)
		return newin

	def newNodeByApp(self, app, y, x, height, width, params):
		if self.closing: return 0
		if self.id > 0 and len(self.child_nodes) > 13: return False

		if self.id != 0:
			newin = self.wm.newNodeByApp(app, y + self.from_y, x + self.from_x, height, width, params, parent = self)
		else:
			newin = self.wm.newNodeByApp(app, y + self.from_y, x + self.from_x, height, width, params)
		self.child_nodes.append(newin.node)
		return newin


	def closeNode(self, node):
		if self.closing: return 0
		self.child_nodes.remove(node)
		if node != self:
			node.abort

	def abort(self):
		if self.closing: return 0
		self.closing = True
		if self.parent and self in self.parent.child_nodes:
			self.parent.child_nodes.remove(self)
		try:
			self.win.abort()
		except Exception as ex:
			self.errorMessage("abort", ex)
		try:
			if hasattr(self, "win"):
				del self.win
		finally:
			if hasattr(self, "ui"):
				del self.ui
			if hasattr(self, "neoui"):
				self.neoui.abort()
				del self.neoui
		self.ready_to_close = True

#Window Manager Decoration

	def setKindness(self, id):
		if id == 0:
			self.windowed = False

#input listeners

	def click(self, device_id, button, y, x):
		if self.closing: return 0
		if self.ui.click(device_id, button, y - self.from_y, x - self.from_x):
			if self.controller.MouseEvents in self.sub:
				try:
					self.win.click(device_id, button,  y - self.from_y, x - self.from_x)
				except Exception as ex:
					self.errorMessage("click", ex)

	def drag(self, id, button, stage, y, x):
		if self.closing: return 0
		if stage == 0:
			y -= self.from_y
			x -= self.from_x
		try:
			if self.ui.drag(id, button, stage, y, x):
				if self.controller.MouseEvents in self.sub:
					self.win.drag(id, button, stage, y, x)
		except Exception as ex:
			self.errorMessage("drag", ex)

	def scroll(self, id, delta):
		if self.closing: return 0
		#if self.ui.scroll(id, delta):
		if self.controller.MouseWheelEvents in self.sub:
			try:
				self.win.scroll(id, delta)
			except Exception as ex:
				self.errorMessage("scroll", ex)

	def midikeyPress(self, note, pressure):
		if self.closing: return 0
		try:
			self.win.midikeyPress(note, pressure)
		except Exception as ex:
			self.errorMessage("midi", ex)

	def midikeyRelease(self, note):
		if self.closing: return 0
		try:
			self.win.midikeyRelease(note)
		except Exception as ex:
			self.errorMessage("midi", ex)


