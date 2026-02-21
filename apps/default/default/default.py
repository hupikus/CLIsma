from type.colors import Colors
from type.descriptor import Descriptor

from integration.loghandler import Loghandler
from integration.appconfig import Appconfig

from NodeSquad.modules.window import Window
class default(Winddow):

	def __init__(self, node, args = ''):
		# Base
		self.node = node
		self.controller = node.controller
		self.height = node.height
		self.width = node.width

		# Input (Node class reads this field)
		self.input_subscriptions = [self.controller.MouseEvents, self.controller.KeyboardEvents]

		# Non api
		self.counter = 1

		if Colors.colorlen == 256:
			self.colorPairs = [
				Colors.colorPair(13),
				Colors.colorPair(35),
				Colors.colorPair(55),
				Colors.colorPair(41)
			]
		else:
			self.colorPairs = [
				Colors.colorPair(1),
				Colors.colorPair(4),
				Colors.colorPair(7),
				Colors.colorPair(5)
			]

		self.descriptor = Appconfig.OpenConfig(node.app)

		Loghandler.Log(Descriptor.GetType(self.descriptor))

		self.config = Appconfig.ReadConfig(self.descriptor)

		Loghandler.Log(self.config)

		ui = self.node.ui

		ui.textLine("description", "Hello world!", 2, 0)


	def draw(self, delta):
		node = self.node
		node.appendStr(0, 0, '-' * self.width)
		node.appendStr(1, 0, str(self.counter).center(self.width, '-'))
		node.appendStr(0, 0, "Default window", self.colorPairs[self.counter % 4])
		node.appendStr(3, 0, '-' * self.width)

	def click(self, device_id, button, y, x):
		self.counter += 1

	def abort(self):
		Appconfig.CloseConfig(self.descriptor)
