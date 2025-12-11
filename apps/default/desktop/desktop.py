import math

from type.colors import Colors
from type.keys import Keys

from apps.apps import App
from apps.apphabit import apphabit
from singletons import Singletons

from userglobals import userglobals
from integration.loghandler import Loghandler

class desktop(apphabit):

	def gen_cache(self):
		header = self.greetmsg + ' ' * (self.width - len(self.greetmsg) - 1) + 'x'
		header_window = header[:-5] + "- m x"
		self.dekstop_str = (header, '─' * self.width, ' ' * self.width, header_window)

		self.range = tuple([range(3)] + [range(2 + a, self.height - 4, 3) for a in range(3)] + [range(2, self.height - 4)])


	def setmaxstep(self, step):
		self.spawnmode = step
		self.spawnstep = 0
		if step == 0:
			self.maxstep = min(9, round(self.width - self.spawnx) / 2, self.height - self.spawny)
		elif step == 1:
			self.maxstep = -min(self.width / 4, self.height / 9)

	def step(self):
		self.spawnstep += 1
		if self.spawnstep == self.maxstep:
			self.spawnstep = 0
			self.spawny = round(self.height * 0.3)
			self.spawnx = round(self.width / 4)
		if self.spawnmode == 0:
			self.spawny += 1
			self.spawnx += 2
		elif self.spawnmode == 1:
			self.spawnstep += 0.327
			if self.spawnstep > 6.3: self.spawnstep -= 6.3
			self.spawny = round(self.height * 0.3 + math.cos(self.spawnstep) * -self.maxstep)
			self.spawnx = round(self.width / 4 + math.sin(self.spawnstep) * -self.maxstep * 1.4)

	def abort(self):
		self.to_shutdown("code")

	def start(self):
		self.tick = 0
		self.refresh = False
		self.node.ui.clickArea("menu", self.menu, self.height - 3, 0, 3, 5)
		for i in range(self.applen):
			self.node.ui.clickArea("app" + str(i), self.dockapp_clicked, self.height - 3, self.space * (i + 1), 3, 5)

		#window spawn
		self.spawny = round(self.height * 0.3)
		self.spawnx = round(self.width / 4)
		self.setmaxstep(0)

		#cache
		self.gen_cache()

	def to_shutdown(self, name):
		self.state = "shutdown"
		self.ready = 1
		if name != "code":
			self.wm.shutdown()


	def recalculate_dock(self):
		self.applen = len(self.apps)
		self.maxtrey = round(self.width / 6 - 0.5)
		self.rightfrom = min(round(self.width * 0.85), self.width - 12)
		self.space = round( ( self.rightfrom - (5 * self.applen)) / (self.applen + 0.5) ) - 5
		#                     right panel       apps itself          number of apps

	def __init__(self, id, node, controller, height, width, params):
		self.id = id
		self.node = node
		self.controller = controller
		self.wm = params
		self.width = width
		self.height = height

		self.preferred_height = 80
		self.preferred_width = 24
		self.ismenu = False


		self.neotick = 0
		self.neofps = 0
		self.tick_rate = "0"
		self.fps_rate = "0"
		self.process_timer = 0.0
		self.draw_timer = 0.0

		if self.height < 14 or self.width < 27:
			self.state = "minimal"
		else:
			self.state = "regular"

		#subscribe to input
		self.input_subscriptions = [controller.MouseEvents, controller.KeyboardEvents]

		#configable
		self.menuapp = App("default/menu")

		if self.state == "minimal":
			self.greetmsg = "Minimal mode"
			self.apps = [App("default/settings"), App("default/fileman")]
		else:
			self.greetmsg = "Welcome to CLI System Management Accompanier! (" + userglobals.username + " session)"
			self.apps = [App("default/settings"), App("default/fileman"), App("default/log")]

		self.pinned = len(self.apps)

		#App("default/terminal") App("default/colortest") App("default/log") App("default/textplayer")

		#constants
		self.recalculate_dock()

		#self.ready = 0
		self.start()

	#def updateb(self, y):
		#self.node.appendStr(min(max(2, y), self.height - 5), 0, ' ' * self.width)


	def draw_header(self, isMax):
		self.tick = (self.tick + 1) % 3
		#self.tick = (self.tick + 1) % (self.height - 7)

		if self.state == "regular":
			if isMax:
				self.node.appendStr(0, 0, self.dekstop_str[3] + self.wm.nodes[self.wm.order[-1]].name)
			else:
				self.node.appendStr(0, 0, self.dekstop_str[0], Colors.colorPair(2))
		elif self.state == "shutdown":
			self.node.appendStr(0, 0, "shutdown" + '.' * (self.width - 8), Colors.colorPair(2))
		return isMax


	def draw(self, delta):

		appendStr = self.node.appendStr

		self.neofps += 1
		self.draw_timer += delta

		if self.draw_timer >= 1.0:
			self.draw_timer -= 1.0
			self.fps_rate = str(self.neofps)
			self.neofps = 0

		refresh = 0
		if  self.refresh:
			refresh = 1
		if self.draw_header(self.wm.draw_as_maximized): #force interlace refresh when maximized or fullscreen window exists
			refresh = 2

		###################
		appendStr(1, 0, self.dekstop_str[1])

		if refresh > 0:
			#interlace refresh
			if refresh == 1 or self.neofps % 12 == 1:
				for y in self.range[self.tick + 1]:
					appendStr(y, 0, self.dekstop_str[2])
				appendStr(3, 0, "Lazy refresh enabled")
		else:
			for y in self.range[4]:
				appendStr(y, 0, self.dekstop_str[2])

		#appendStr(self.height, 0, self.dekstop_str[2])

		if self.state == "regular":
			appendStr(6, 0, f"{self.fps_rate} FPS, {self.tick_rate} TPS")

		#__________________
		appendStr(self.height - 4, 0, self.dekstop_str[1], Colors.FXNormal)

		for y in self.range[0]:
			#line = ''
			appendStr(self.height - 3 + y, 0, self.menuapp.icon[y], Colors.colorPair(6) | Colors.FXBold)
			for i in range(self.applen):
				appendStr(self.height - 3 + y, self.space * (i + 1), self.apps[i].icon[y], Colors.colorPair(6))
				#line = line + (' ' * self.space) + str(self.apps[i].icon[y])
			#self.node.appendStr(self.height - 3 - 5 + y, 0, line)

	def onresize(self, height, width):
		self.height = height
		self.width = width
		self.gen_cache()

	def keyPress(key):
		print(key)

	def process(self, delta):
		self.neotick += 1
		self.process_timer += delta

		if self.process_timer >= 1.0:
			self.process_timer -= 1.0
			self.tick_rate = str(self.neotick)
			self.neotick = 0

		#if self.ready == 2:
			#self.wm.shutdown()

	def click(self, device_id, button, y, x):
		if x == self.width - 1 and y == 0:
			self.to_shutdown("user")



	def menu(self, name, button, device_id):
		if button == 0:
			if not self.ismenu:
				try:
					h = round((self.height - 7) * 0.4)
					self.menunode = self.node.newNode("apps.default", "menu", self.height - 4 - h, 0, h, round(self.width / 4), '').node
					self.menunode.windowed = False
				except:
					pass
			else:
				self.node.closeNode(self.menunode)
			self.ismenu = not self.ismenu


	def dockapp_clicked(self, name, button, device_id):
		if button == 0:
			Loghandler.Log("open " + self.apps[int(name[3:])].name)
			node = self.launchApp(self.apps[int(name[3:])])
			if node:
				self.wm.pointers[device_id].focus_id = node.id

	def launchApp(self, app, returned = False):
		app = self.node.newNodeByApp(app, self.spawny, self.spawnx, 0, 0, '')
		self.step()
		if returned and app: return app.node
		else: return False
