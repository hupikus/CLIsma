from apps.apphabit import apphabit
from log import loghandler
class log(apphabit):

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

		#preferences
		self.MaxLen = 20


	def draw(self):
		if loghandler.loglen == 0:
			self.node.appendStr(0, 0, "Nothing yet...".center(self.width, ' '))
			for y in range(self.height - 1):
				self.node.appendStr(0, 0, ' ' * self.width)
		else:
			column = min(self.height, self.loglen)
			for y in range(column):
				self.node.appendStr(y, 0, loghandler.log[-column + y].center(self.width, ' '))

		
