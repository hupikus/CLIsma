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

		text = ''

		for i in range(Colors.colorlen):
			text += f"<c{i}>{i}<endc> "
		#text = "Example <c4>TextBox Text<endc> <n> <c77>PRIVET<endc>"
		#text = "<c7> <treverse> Hello <tbold>World! <endc> <endt>"

		self.node.ui.coloredTextBox("Colors", text, 0, 0, self.height, self.width)
		#self.node.ui.textLine("name", "Hello World!", 0, 0, attr = Colors.FXItalic | Colors.FXBlink | Colors.FXReverse | Colors.FXBold | Colors.colorPair(7))

	def onresize(self, height, width):
		self.height = height
		self.width = width
		self.node.ui.resize("Colors", height, width - 1, type = "coloredTextBoxes")
