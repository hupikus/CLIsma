from singletons import Singletons
from apps.apps import App
from type.colors import Colors

from apps.apphabit import apphabit
class menu(apphabit):
	
	def newapp(self, id):
		app = App(id)
		self.node.abort()

	def __init__(self, id, node, controller, height, width, params):
		#base
		self.id = id
		self.node = node
		self.controller = controller
		self.height = height
		self.width = width



		self.node.setKindness(0)

		self.desktop = Singletons.Wm.desktop

		#input
		self.input_subscriptions = [controller.MouseEvents, controller.MouseWheelEvents]

		self.apps = Singletons.appp.GetAppInstances()
		self.display = []
		self.clickapp = {}
		self.scrollpos = 0
		letter = ''
		self.line = 3
		for name in sorted(self.apps.keys()):
			if name == "desktop": continue
			if name[0].capitalize() != letter:
				letter = name[0].capitalize()
				self.display.append(letter)
				self.line += 1
			self.display.append((self.apps[name].name))
			self.clickapp[self.line] = name
			self.line += 1
		self.viewlen = min(self.height, self.line - 3)
			


	def draw(self):
		s = self.scrollpos
		d = self.display
		w = self.width
		title = "CLIde menu"
		titwid = self.width - 10
		self.node.appendStr(0, 0, '-' * round(titwid >> 1) + title + '-' * ((titwid >> 1) + 1))
		#self.node.appendStr(1, 0, ' ' * self.width)
		if s < 2:
			title = "All apps"
			titwid = self.width - 8
			self.node.appendStr(2 - s, 0, ' ' * round(titwid >> 1) + title + ' ' * ((titwid >> 1) + 1))
		l = 3 - s
		for i in range(max(0, s - 2), self.viewlen):
			self.node.appendStr(l + i, 0, d[i].ljust(w, ' '))
	
	def click(self, device_id, button, y, x):
		yr = y + self.scrollpos
		if button == 0:
			if yr in self.clickapp:
				self.desktop.launchApp(self.apps[self.clickapp[yr]])
	
	def scroll(self, id, delta):
		self.viewlen = min(self.height, self.line - 3)
		self.scrollpos = min(max(0, self.scrollpos + delta), self.line - 3 - round(self.height * 0.8))

	def process(self):
		if not self.node.isActive():
			self.desktop.ismenu = False
			self.node.abort()
	
	def resize(self, height, width):
		self.height = height
		self.width = width
		self.viewlen = min(height, self.line - 3)