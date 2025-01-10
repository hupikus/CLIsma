from pympler import asizeof
import psutil

import threading
import time

from type.colors import Colors
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


		#self.node.ui.coloredTextBox("errormessage", "<tbold>THE END<endt> " + "IS NEVER THE <c2>END <endc>" * 20, 0, 0, self.height, self.width)
		self.mem = "0"
		self.cpu = "0"
		self.interval = 0.5

		self.shutdown = True
		thread = threading.Thread(target = self.statUpdate)
		thread.start()


		self.space = ' ' * self.width


	def draw(self):
		for y in range(self.height):
			self.node.appendStr(y, 0, self.space)
		self.node.appendStr(2, 0, self.mem)
		self.node.appendStr(3, 0, self.cpu)
	

	def onresize(self, height, width):
		self.height = height
		self.width = width
		self.space = ' ' * self.width
		#self.node.ui.resize("errormessage", height, width)
	
	def statUpdate(self):
		while self.shutdown:
			self.mem = str(asizeof.asizeof(self.node.wm)) + " B"
			self.cpu = str(psutil.cpu_percent()) + "% CPU used"
			time.sleep(self.interval)
	
	def abort(self):
		self.shutdown = False