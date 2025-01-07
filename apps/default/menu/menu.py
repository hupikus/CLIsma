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

		self.apps = (
		App("default/bangerplayer"),
		App("default/colortest"),
		App("default/default"),
		App("default/fileman"),
		App("default/log"),
		App("default/settings"),
		App("default/terminal"),
		App("default/textplayer"),
		)
		self.possis = (4, 6, 8, 10, 12, 14, 16, 17)


	def draw(self):
		title = "CLIde menu"
		titwid = self.width - 10
		self.node.appendStr(0, 0, '-' * round(titwid >> 1) + title + '-' * ((titwid >> 1) + 1))
		#self.node.appendStr(1, 0, ' ' * self.width)
		title = "All apps"
		titwid = self.width - 8
		self.node.appendStr(2, 0, ' ' * round(titwid >> 1) + title + ' ' * ((titwid >> 1) + 1))
		self.node.appendStr(3, 0, 'B', Colors.FXBold)
		self.node.appendStr(4, 0, "Bangerplayer")
		self.node.appendStr(5, 0, 'С', Colors.FXBold)
		self.node.appendStr(6, 0, "Color Test")
		self.node.appendStr(7, 0, 'D', Colors.FXBold)
		self.node.appendStr(8, 0, "Default App")
		self.node.appendStr(9, 0, 'F', Colors.FXBold)
		self.node.appendStr(10, 0, "Fileman")
		self.node.appendStr(11, 0, 'L', Colors.FXBold)
		self.node.appendStr(12, 0, "Log")
		self.node.appendStr(13, 0, 'S', Colors.FXBold)
		self.node.appendStr(14, 0, "Settings")
		self.node.appendStr(15, 0, 'T', Colors.FXBold)
		self.node.appendStr(16, 0, "Terminal")
		self.node.appendStr(17, 0, "Text Player")
	

	def click(self, device_id, button, y, x):
		if button == 0:
			if y in self.possis:
				self.desktop.launchApp(self.apps[self.possis.index(y)])

	def process(self):
		if not self.node.isActive():
			self.desktop.ismenu = False
			self.node.abort()