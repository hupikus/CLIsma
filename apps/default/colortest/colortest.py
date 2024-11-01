from type.colors import Colors
from apps.apphabit import apphabit

class colortest(apphabit):

	def __init__(self, id, node, controller, height, width, params):
		#base
		self.id = id
		self.node = node
		self.controller = controller
		self.height = height
		self.width = width


		self.preferred_height = 6
		self.preferred_width = 45

		text = ''

		for i in range(Colors.colorlen):
			text += f"<c{i}>{i}<endc> "
		#text = "Example <c4>TextBox Text<endc> <n> <c77>PRIVET<endc>"

		self.node.ui.coloredTextBox("Colors", text, 0, 0, self.preferred_height, self.preferred_width)

	def onresize(self, height, width):
		self.height = height
		self.width = width
		self.node.ui.resizeTextBox("Colors", height, width - 1)
