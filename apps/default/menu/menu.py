from singletons import Singletons
from apps.app import App
from type.colors import Colors

from integration.loghandler import Loghandler

from NodeSquad.modules.window import Window
class menu(Window):

	def newapp(self, id):
		app = App(id)
		self.node.abort()

	def __init__(self, node, args = None):
		#base
		self.node = node
		self.controller = node.controller
		self.height = node.height
		self.width = node.width

		self.node.setDecoration(False)

		self.desktop = args

		#input
		self.input_subscriptions = [self.controller.MouseEvents, self.controller.MouseWheelEvents]

		self.apps = Singletons.appp.GetAppInstances()
		self.display = []
		self.clickapp = {}
		self.scrollpos = 0
		letter = ''
		self.line = 2
		for name in sorted(self.apps.keys()):
			#Loghandler.Log((self.apps[name].name))
			if name == "desktop": continue
			if name[0].capitalize() != letter:
				letter = name[0].capitalize()
				self.display.append(letter)
				self.line += 1
			self.display.append((self.apps[name].name))
			self.clickapp[self.line] = name
			self.line += 1
		self.viewlen = min(self.height, self.line - 2)



	def draw(self, delta):
		s = self.scrollpos
		d = self.display
		w = self.width
		node = self.node
		spaces = ' ' * w
		title = "CLIde menu"
		titwid = self.width - 10
		node.appendStr(0, 0, '-' * round(titwid >> 1) + title + '-' * ((titwid >> 1) + 1))
		node.appendStr(1, 0, spaces)
		if s < 2:
			title = "All apps"
			titwid = w - 8
			node.appendStr(2 - s, 0, ' ' * round(titwid >> 1) + title + ' ' * ((titwid >> 1) + 1))
		l = 3 - s
		for i in range(max(0, s - 2), self.height - 1 + s):
			if i > self.line - 3:
				node.appendStr(l + i - 1, 0, spaces)
			else:
				node.appendStr(l + i - 1, 0, d[min(i, self.line - 3)].ljust(w, ' '))



	def click(self, device_id, button, y, x):
		yr = y + self.scrollpos
		if button == 0:
			if yr in self.clickapp:
				self.desktop.launchApp(self.apps[self.clickapp[yr]])

	def scroll(self, id, delta):
		self.viewlen = min(self.height, self.line - 2)
		self.scrollpos = min(max(0, self.scrollpos + delta), self.line - 2 - round(self.height * 0.8))

	def process(self, delta):
		if not self.node.isActive():
			self.node.abort()

	def resize(self, height, width):
		self.height = height
		self.width = width
		self.viewlen = min(height, self.line - 2)
