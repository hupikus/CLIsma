class menu:

	def abort(self):
		pass

	def __init__(self, id, node, controller, height, width):
		#base
		self.id = id
		self.node = node
		self.controller = controller
		self.height = height
		self.width = width

		self.preferred_height = 18
		self.preferred_width = 45


		self.node.setKindness(0)

		#input
		#self.input_subscriptions = [controller.MouseEvents, controller.KeyboardEvents]


	def draw(self):
		title = "CLIde menu"
		titwid = self.width - 10
		self.node.appendStr(0, 0, '-' * round(titwid / 2 - 0.5) + title + '-' * round(titwid / 2 + 0.5))
		self.node.appendStr(2, 0, ' ' * self.width)


	def process(self):
		pass