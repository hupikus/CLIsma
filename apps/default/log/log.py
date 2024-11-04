from apps.apphabit import apphabit
from loghandler import Loghandler
class log(apphabit):

	def __init__(self, id, node, controller, height, width, params):
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
		if Loghandler.loglen == 0:
			self.node.appendStr(0, 0, "Nothing yet...".center(self.width, ' '))
			for y in range(self.height - 1):
				self.node.appendStr(y + 1, 0, ' ' * self.width)
		else:
			column = min(self.height, Loghandler.loglen)
			for y in range(column):
				self.node.appendStr(y, 0, Loghandler.history[-(y + 1)].center(self.width, ' '))

		
