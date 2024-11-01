import threading
import time

from apps.apps import App
from apps.apphabit import apphabit

from userglobals import userglobals
from loghandler import Loghandler

class desktop(apphabit):


	def start(self):
		self.tick = 0
		#self.node.ui.clickArea("menu", self.menu, self.height - 4, 0, 3, 5)
		self.node.ui.clickArea("menu", self.menu, self.height - 4, 0, 3, 5)
		for i in range(self.applen):
			self.node.ui.clickArea("app" + str(i), self.dockapp_clicked, self.height - 4, self.space * (i + 1), 3, 5)

		#desktop view allocation (static partst)
		self.dekstop_str = ["Bepis", "Bepis", "Bepis", "Bepis"]
		if self.controller.mouse:
			self.dekstop_str[0] = self.greetmsg + ' ' * (self.width - len(self.greetmsg) - 1) + 'x'
		else:
			self.dekstop_str[0] = self.greetmsg + ' ' * (self.width - len(self.greetmsg))
		self.dekstop_str[1] = '#' * self.width
		self.dekstop_str[2] = ' ' * self.width
		self.dekstop_str[3] = '_' * self.width

		#ticks and fps counter
		self.fpsc = 0
		self.tickc = 0
		self.fps_rate = "60"
		self.tick_rate = "90"
		counter_thread = threading.Thread(target=self.fpsleep)
		counter_thread.start()

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
			self.apps = [App("default/settings"), App("default/terminal")]
		else:
			self.greetmsg = "Welcome to CLI System Management Accompanier! (" + userglobals.username + " session)"
			self.apps = [App("default/settings"), App("default/terminal"), App("default/fileman")]

		self.pinned = 3
			
		#self.apps = [App("default/settings"), App("default/settings")]

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

		for y in range(2 + self.tick, self.height - 5, 3):
			self.node.appendStr(y, 0, self.dekstop_str[2])

		if self.state == "regular":
			self.node.appendStr(6, 0, self.fps_rate + " FPS, " + self.tick_rate + " TPS, tick " + str(self.tick))

		self.node.appendStr(self.height - 5, 0, self.dekstop_str[3])

		for y in range(3):
			#line = ''
			self.node.appendStr(self.height - 4 + y, 0, self.menuapp.icon[y])
			for i in range(self.applen):
				self.node.appendStr(self.height - 4 + y, self.space * (i + 1), self.apps[i].icon[y])
				#line = line + (' ' * self.space) + str(self.apps[i].icon[y])
			#self.node.appendStr(self.height - 4 - 5 + y, 0, line)

		#self.node.apply()

		return 0

	def process(self):
		self.tickc += 1
		if self.ready == 2:
			self.wm.shutdown()

	def click(self, button, y, x):
		if x == self.width - 1 and y == 0:
			self.to_shutdown("user")



	def menu(self, name, button):
		if button == 0:
			if not self.ismenu:
				self.menunode = self.node.newNode("apps.default", "menu", self.height - 7 - round((self.height - 8) * 0.4), 0, round((self.height - 8) * 0.4), round(self.width / 4), '').node
				self.menunode.windowed = False
			else:
				self.node.closeNode(self.menunode)
			self.ismenu = not self.ismenu


	def dockapp_clicked(self, name, button):
		if button == 0:
			Loghandler.Log("open " + self.apps[int(name[3:])].name)
			self.launchApp(self.apps[int(name[3:])])

	def launchApp(self, app, returned = False):
		if returned:
			app = self.node.newNode(app.parent_path, app.class_name, round(self.height * 0.3), round(self.width / 4), 0, 0, '')
			if app:
				return app.node
			else:
				return False
		else:
			self.node.newNode(app.parent_path, app.class_name, round(self.height * 0.3), round(self.width / 4), 0, 0, '')
