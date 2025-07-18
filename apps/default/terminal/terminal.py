import threading
import time
import integration.shell.shell as sh

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
		self.input_subscriptions = [controller.MouseEvents, controller.MouseWheelEvents, controller.KeyboardEvents]


		self.shutdown = True


		self.space = ' ' * self.width

		self.text = ""
		sh.redirect_print(self.addtext)
		self.shell_thread = threading.Thread(target=sh.shell)
		#self.shell_thread.start()


	def draw(self, delta):
		for y in range(self.height):
			self.node.appendStr(y, 0, self.space)
		self.node.writeStr(0, 0, self.text)


	def onresize(self, height, width):
		self.height = height
		self.width = width
		self.space = ' ' * self.width
		#self.node.ui.resize("errormessage", height, width)
	
	
	def abort(self):
		sh.running = False
		#self.shell_thread.join()
	

	def addtext(self, *args, **kwargs):
		self.text += ' '.join(args)
