from type.colors import Colors
from type.descriptor import Descriptor

from integration.loghandler import Loghandler
from integration.appconfig import Appconfig

from apps.apphabit import apphabit
class default(apphabit):

	def __init__(self, id, node, controller, height, width, params):
		#base
		self.id = id
		self.node = node
		self.controller = controller
		self.height = height
		self.width = width

		#input
		self.input_subscriptions = [controller.MouseEvents, controller.KeyboardEvents]

		#non api
		self.counter = 1

		if Colors.colorlen == 256:
			self.colorPairs = [Colors.colorPair(13), Colors.colorPair(35), Colors.colorPair(180), Colors.colorPair(220)]
		else:
			self.colorPairs = [Colors.colorPair(1), Colors.colorPair(4), Colors.colorPair(7), Colors.colorPair(5)]

		self.descriptor = Appconfig.OpenConfig(node.app)

		ui = self.node.ui

		ui.textLine("description", "Default window contains minimal api usage", 2, 0)


	def draw(self, delta):
		self.node.appendStr(0, 0, '-' * self.width)
		self.node.appendStr(1, 0, str(self.counter).center(self.width, '-'))
		self.node.appendStr(0, 0, "This is default window", self.colorPairs[self.counter % 4])
		self.node.appendStr(3, 0, '-' * self.width)

	def click(self, device_id, button, y, x):
		self.counter += 1
