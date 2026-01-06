from type.colors import Colors
from type.descriptor import Descriptor
from type.keys import Keys

from integration.loghandler import Loghandler

from apps.apphabit import apphabit
class neoui(apphabit):

	def __init__(self, id, node, controller, height, width, params):
		#base
		self.id = id
		self.node = node
		self.controller = controller
		self.height = height
		self.width = width

		#input
		self.input_subscriptions = [controller.MouseEvents, controller.KeyboardEvents]

		self.neoui = node.neoui

		ui = self.neoui

		self.canvas = ui.CreateCanvas()

		txt = ui.TextLine(5, 0, "Hello World!", attr = Colors.FXTextGreen)

		txt.align = 1

		self.canvas.Add(txt)

		#txt1 = ui.TextLine(self.canvas, 6, 3, "Hello 2orld!", attr = Colors.FXNormal)

		self.button_style = ui.UIStyle(
			normal = ui.StylePack(normal = Colors.FXTextGreen, hover = Colors.FXTextGreen, interact = Colors.FXTextGreen),

			background = ui.StylePack(normal = Colors.FXNormal, hover = Colors.FXNormal, interact = Colors.FXNormal),

			border = ui.StylePack(normal = Colors.FXTextRed, hover = Colors.FXNormal, interact = Colors.FXTextBlue)
		)

		btn = ui.Button(self.button, 7, 3, 12, 11, "Hello\n World!", align = 1, style = self.button_style, atlas = "┌┐└┘│─ ")
		self.canvas.Add(btn)

		txt.align = 0

		slider = ui.Slider(None, y = 2, x = 8)
		self.canvas.Add(slider)

		slider = ui.Slider(None, y = 2, x = 20, vertical = True, length = 5, default = 3)
		self.canvas.Add(slider)

		btn = ui.RadioButton(None, y = 4, x = 10)
		self.canvas.Add(btn)


		field = ui.InputField()
		self.canvas.Add(field)


	def draw(self, delta):
		self.node.clear()
		self.node.appendStr(0, 0, "TEST" + ' ' * self.width)


	def button(self, widget, action, button, device):
		widget.Remove()
