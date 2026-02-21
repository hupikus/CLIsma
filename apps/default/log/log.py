from integration.loghandler import Loghandler

from NodeSquad.modules.window import Window
class log(Window):

	def __init__(self, node, args = ''):
		# Base
		self.node = node
		self.controller = node.controller
		self.height = node.height
		self.width = node.width


		self.preferred_height = 4
		self.preferred_width = 45

		#input
		#self.input_subscriptions = [controller.MouseEvents, controller.KeyboardEvents]

		#preferences
		self.MaxLen = 20

	def draw(self, delta):
		if Loghandler.loglen == 0:
			self.node.appendStr(0, 0, "Nothing yet...".center(self.width, ' '))
			for y in range(self.height - 1):
				self.node.appendStr(y + 1, 0, ' ' * self.width)
		else:
			column = min(self.height, Loghandler.loglen)
			for y in range(column):
				self.node.writeStr(y, 0, Loghandler.history[-(y + 1)].center(self.width, ' '))
			for y in range(column - 1, self.height - 1):
				self.node.appendStr(y + 1, 0, ' ' * self.width)


