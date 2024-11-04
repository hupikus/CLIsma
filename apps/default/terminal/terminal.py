from apps.apphabit import apphabit
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


		self.node.ui.coloredTextBox("errormessage", "<tbold>THE END<endt> " + "IS NEVER THE <c2>END <endc>" * 20, 0, 0, self.height, self.width)


	def draw(self):
		for y in range(5):
			self.node.appendStr(0, 0, ' ' * self.width)
	

	def onresize(self, height, width):
		self.height = height
		self.width = width
		self.node.ui.resizeTextBox("errormessage", height, width)