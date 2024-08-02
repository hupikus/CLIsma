from apps.apps import App

class desktop:

	def start(self):
		self.tick = 0
		#self.node.ui.clickArea("menu", self.menu, self.height - 4, 0, 3, 5)
		self.node.ui.clickArea("menu", self.menu, 0, self.height - 4, 3, 5)
		self.node.ui.slider("test", self.abort, 12, 8, 11)
		#for i in range(self.applen):
			#self.node.ui.clickArea()

	def abort(self):
		self.state = "shutdown"
		self.wm.shutdown()



	def __init__(self, id, node, controller, height, width):
		self.id = id
		self.node = node
		self.controller = controller
		self.width = width
		self.height = height
		self.ismenu = False
		self.start()

		if self.height < 10 or self.width < 27:
			self.state = "minimal"
		else:
			self.state = "regular"

		#subscribe to input
		self.input_subscriptions = [controller.MouseEvents, controller.KeyboardEvents]

		#configable
		self.menuapp = App("default/menu")

		if self.state != "minimal":
			self.greetmsg = "Welcome to CLI System Management Accompanier!"
			self.apps = [App("default/settings"), App("default/terminal")]
		else:
			self.greetmsg = "Minimal mode"
			self.apps = [App("default/settings"), App("default/terminal")]
		#self.apps = [App("default/settings"), App("default/settings")]

		#unconfigable
		self.applen = len(self.apps)
		self.maxtrey = round(self.width / 6 - 0.5)
		#self.space = round((self.width - 6) / (self.applen + 1) - 0.5) - 2
		self.space = round((self.width - (5 * self.applen)) / (self.applen + 0.5)) - 5

	#def updateb(self, y):
		#self.node.appendStr(min(max(2, y), self.height - 6), 0, ' ' * self.width)


	def draw(self):
		self.tick = (self.tick + 1) % 3
		#self.tick = (self.tick + 1) % (self.height - 8)

		if self.state == "regular":
			if self.controller.mode == "full":
				self.node.appendStr(0, 0, self.greetmsg + ' ' * (self.width - len(self.greetmsg) - 1) + 'x')
			else:
				self.node.appendStr(0, 0, self.greetmsg + ' ' * (self.width - len(self.greetmsg)))
		elif self.state == "shutdown":
			self.node.appendStr(0, 0, "shutdown" + '.' * (self.width - 8))


		self.node.appendStr(1, 0, '#' * self.width)

		for y in range(2 + self.tick, self.height - 5, 3):
			self.node.appendStr(y, 0, ' ' * self.width)

		if self.state == "regular":
			self.node.appendStr(6, 0, "tick " + str(self.tick))

		self.node.appendStr(self.height - 5, 0, '_' * self.width)

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
		#self.tick += 1
		pass

	def click(self, button, x, y):
		if x == self.width - 1 and y == 0:
			self.abort()



	def menu(self):
		if not self.ismenu:
			self.menunode = self.wm.newNode("apps.default", "menu", 22, 0, 10, round(self.width / 2)).node
			self.menunode.windowed = False
		else:
			self.wm.closeNode(self.menunode)
		self.ismenu = not self.ismenu
