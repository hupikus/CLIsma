class terminal:



	def abort(self):
		pass

	def __init__(self, id, node, controller, height, width):
		#base
		self.id = id
		self.node = node
		self.controller = controller
		self.height = height
		self.width = width


		self.preferred_height = 15
		self.preferred_width = 15

		#input
		#self.input_subscriptions = [controller.MouseEvents, controller.KeyboardEvents]


	def draw(self):
		for y in range(5):
			self.node.appendStr(0, 0, ' ' * self.width)




	def process(self):
		pass
