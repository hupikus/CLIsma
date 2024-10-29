from singletons import Singletons

from apps.apphabit import apphabit
class menu(apphabit):
	
	def start(self):
		self.node.ui.clickArea("default/settings", self.newapp, 5, 0, 1, self.width)
	
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

		self.preferred_height = 18
		self.preferred_width = 45


		self.node.setKindness(0)

		self.wm = Singletons.Wm

		#input
		#self.input_subscriptions = [controller.MouseEvents, controller.KeyboardEvents]
		self.start()


	def draw(self):
		title = "CLIde menu"
		titwid = self.width - 10
		self.node.appendStr(0, 0, '-' * round(titwid >> 1) + title + '-' * ((titwid >> 1) + 1))
		#self.node.appendStr(1, 0, ' ' * self.width)
		title = "All apps"
		titwid = self.width - 8
		self.node.appendStr(2, 0, ' ' * round(titwid >> 1) + title + ' ' * ((titwid >> 1) + 1))
		self.node.appendStr(3, 0, 'S')
		self.node.appendStr(5, 0, "Settings")

	def process(self):
		if self.wm.focus_id != self.id:
			self.wm.desktop.ismenu = False
			self.node.abort()