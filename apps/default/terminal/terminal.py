from apps.apphabit import apphabit
from pympler import asizeof
class terminal(apphabit):

	def __init__(self, id, node, controller, height, width, params):
		#base
		self.id = id
		self.node = node
		self.controller = controller
		self.height = height
		self.width = width

		#input
		#self.input_subscriptions = [controller.MouseEvents, controller.KeyboardEvents]


		#self.node.ui.coloredTextBox("errormessage", "<tbold>THE END<endt> " + "IS NEVER THE <c2>END <endc>" * 20, 0, 0, self.height, self.width)


	def draw(self):
		for y in range(self.height):
			self.node.appendStr(0, 0, ' ' * self.width)
		self.node.appendStr(2, 0, str(asizeof.asizeof(self.node.wm)))
	

	def onresize(self, height, width):
		self.height = height
		self.width = width
		#self.node.ui.resize("errormessage", height, width)