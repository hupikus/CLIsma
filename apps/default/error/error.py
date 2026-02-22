from os import system
from type.colors import Colors

from NodeSquad.modules.window import Window
class error(Window):

	def __str__(self):
		return self.text

	def argparser(self, args):
		args = args.split()

		mode = ''
		for i in args:
			if i == "-t" and mode == '':
				mode = 't'
			elif mode == 't':
				if i[0] == "'" or i[0] == '"':
					if i[-1]== "'" or i[-1] == '"':
						self.text = i[1:-1]
						mode = ''
					else:
						self.text = i[1:]
						mode = "append"
				else:
					break
			elif mode == "append":
				self.text  = self.text + ' ' + i

		self.text = self.text[:-1]
		self.displaytext = self.text.center(self.width, ' ')
		mode = ''



	def __init__(self, node, args = None):
		self.node = node
		self.width = node.width
		self.height = node.height


		self.text = "Unstable Error"

		system('echo -e "\\a"')
		self.argparser(args)

		self.space = ' ' * self.width

		node.ui.coloredTextBox("errormessage", self.displaytext, 1, 0, self.height - 1, self.width)

	def draw(self, delta):
		self.node.clear()
		self.node.appendStr(0, 0, '-' * self.width)
		#self.node.writeStr(1, 0, self.text)

	def resize(self, height, width):
		self.height = height
		self.width = width
		self.displaytext = self.text.center(self.width, ' ')
		self.space = ' ' * self.width
		self.node.ui.resize("errormessage", height - 1, width, type = "coloredTextBoxes")
