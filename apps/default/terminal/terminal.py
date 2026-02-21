import threading
import time
import integration.shell.shell as sh

from type.colors import Colors

from NodeSquad.modules.window import Window
class terminal(Window):

	def __init__(self, node, args = ''):
		#base
		self.node = node
		self.controller = node.controller
		self.height = node.height
		self.width = node.width

		#input
		self.input_subscriptions = [
			self.controller.MouseEvents,
			self.controller.MouseWheelEvents,
			self.controller.KeyboardEvents
		]


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
