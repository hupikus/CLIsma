import threading
import time
import math

from apps.apps import App
from apps.apphabit import apphabit
from type.colors import Colors
from singletons import Singletons

from userglobals import userglobals
from integration.loghandler import Loghandler

class desktop(apphabit):

	def gen_cache(self):
		fv = fv = self.greetmsg + ' ' * (self.width - len(self.greetmsg) - 1)
		if self.wm.isMouse:
			fv += 'x'
		else:
			fv += ' '
		self.dekstop_str = (fv, '#' * self.width, ' ' * self.width, '_' * self.width)

		self.range = tuple([range(3)] + [range(2 + a, self.height - 5, 3) for a in range(3)])


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



	def start(self):
		self.tick = 0
		#self.node.ui.clickArea("menu", self.menu, self.height - 4, 0, 3, 5)
		self.node.ui.clickArea("menu", self.menu, self.height - 4, 0, 3, 5)
		for i in range(self.applen):
			self.node.ui.clickArea("app" + str(i), self.dockapp_clicked, self.height - 4, self.space * (i + 1), 3, 5)

		#ticks and fps counter
		self.fpsc = 0
		self.tickc = 0
		self.fps_rate = "60"
		self.tick_rate = "40"
		counter_thread = threading.Thread(target=self.fpsleep)
		counter_thread.start()

		#window spawn
		self.spawny = round(self.height * 0.3)
		self.spawnx = round(self.width / 4)
		self.setmaxstep(0)

		#сache
		self.gen_cache()

	def fpsleep(self):
		while self.ready == 0:
			time.sleep(1)
			self.fps_rate = str(self.fpsc)
			self.tick_rate = str(self.tickc)
			self.fpsc = 0
			self.tickc = 0
		self.ready += 1
	

	def to_shutdown(self, name):
		self.state = "shutdown"
		self.ready = 1


	def recalculate_dock(self):
		self.applen = len(self.apps)
		self.maxtrey = round(self.width / 6 - 0.5)
		#self.space = round((self.width - 6) / (self.applen + 1) - 0.5) - 2
		self.rightfrom = min(round(self.width * 0.85), self.width - 12)
		self.space = round( ( self.rightfrom - (5 * self.applen)) / (self.applen + 0.5) ) - 5
		#                     right panel      apps itself         number of apps

	def __init__(self, id, node, controller, height, width, params):
		self.id = id
		self.node = node
		self.controller = controller
		self.wm = params
		#self.wm = Singletons.Wm
		self.width = width
		self.height = height
		
		self.preferred_height = 80
		self.preferred_width = 24
		self.ismenu = False
		

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
			self.apps = [App("default/settings"), App("default/colortest"), App("default/fileman"), App("default/terminal")]

		self.pinned = 3
			
		#App("default/terminal") App("default/colortest") App("default/log") App("default/textplayer")

		#constants
		self.recalculate_dock()

		self.ready = 0
		self.start()

	#def updateb(self, y):
		#self.node.appendStr(min(max(2, y), self.height - 6), 0, ' ' * self.width)


	def draw(self):
		self.tick = (self.tick + 1) % 3
		self.fpsc += 1
		#self.tick = (self.tick + 1) % (self.height - 8)

		if self.state == "regular":
			self.node.appendStr(0, 0, self.dekstop_str[0])
		elif self.state == "shutdown":
			self.node.appendStr(0, 0, "shutdown" + '.' * (self.width - 8))


		self.node.appendStr(1, 0, self.dekstop_str[1])

		for y in self.range[self.tick + 1]:
			self.node.appendStr(y, 0, self.dekstop_str[2])
		self.node.appendStr(self.height - 1, 0, self.dekstop_str[2])

		if self.state == "regular":
			self.node.appendStr(6, 0, f"{self.fps_rate} FPS, {self.tick_rate} TPS, frame {self.tick}")

		self.node.appendStr(self.height - 5, 0, self.dekstop_str[3])

		for y in self.range[0]:
			#line = ''
			self.node.appendStr(self.height - 4 + y, 0, self.menuapp.icon[y])
			for i in range(self.applen):
				self.node.appendStr(self.height - 4 + y, self.space * (i + 1), self.apps[i].icon[y])
				#line = line + (' ' * self.space) + str(self.apps[i].icon[y])
			#self.node.appendStr(self.height - 4 - 5 + y, 0, line)

		return 0

	def process(self):
		self.tickc += 1
		if self.ready == 2:
			self.wm.shutdown()

	def click(self, device_id, button, y, x):
		if x == self.width - 1 and y == 0:
			self.to_shutdown("user")



	def menu(self, name, button, device_id):
		if button == 0:
			if not self.ismenu:
				try:
					self.menunode = self.node.newNode("apps.default", "menu", self.height - 7 - round((self.height - 8) * 0.4), 0, round((self.height - 8) * 0.4), round(self.width / 4), '').node
					self.menunode.windowed = False
				finally:
					self.ismenu = True
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
