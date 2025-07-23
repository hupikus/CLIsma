from type.colors import Colors
from type.permissions import Permisions

from integration.loghandler import Loghandler
from apps.apphabit import apphabit

class mouselock(apphabit):

	def __init__(self, id, node, controller, height, width, params):
		self.node = node
		self.controller = controller
		self.ui = self.node.ui
		self.active = False
		self.button = False
		self.height = height
		self.width = width
		self.input_subscriptions = [controller.MouseEvents]

		self.inpd = self.node.requestPermission(Permisions.INPUT_DEVICES)

		self.msg = "Waiting for the permission"

		if self.inpd:
			if self.inpd.mouse_class:
				self.msg = "Activate"
				self.button = True
			else:
				self.msg = "No mouse connected"
		else:
			self.msg = "Permission Denied"

	def draw(self, delta):
		w = self.width
		top = '-' * w
		center = '|' + (' ' * (w - 2)) + '|'
		text = self.msg.center(w - 2, ' ')

		textmode = Colors.FXRed
		bordermode = Colors.FXNormal
		if self.button:
			textmode = Colors.FXGreen

		for y in range(self.height):
			if y == 0 or y == self.height - 1:
				self.node.appendStr(y, 0, top, mode = bordermode)
			else:
				self.node.appendStr(y, 0, center, mode = bordermode)

			if y == self.height >> 1:
				self.node.appendStr(y, 1, text, mode = textmode)

	def click(self, button, device_id, y, x):
		if button == 0 and self.button:
			self.active = not self.active
			self.inpd.mouse_class.lock(self.inpd.mouse_class.devicelist[0], self.active)
			Loghandler.Log(f"Mouse lock set to {self.active}")
			self.msg = "Activate" if not self.active or "Deactivate"
