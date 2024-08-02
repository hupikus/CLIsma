class default:
	
	def abort(self):
		pass

	def __init__(self, id, node, controller, height, width):
		#base
		self.id = id
		self.node = node
		self.controller = controller
		self.height = height
		self.width = width


		self.preferred_height = 4
		self.preferred_width = 45

		#input
		#self.input_subscriptions = [controller.MouseEvents, controller.KeyboardEvents]


	def draw(self):
		self.node.appendStr(0, 0, '*' * self.width)
		self.node.appendStr(1, 0, '*' * self.width)
		self.node.appendStr(0, 0, "This is default window")
		self.node.appendStr(2, 0, "Default window contains minimal api usage")


	def process(self):
		pass
