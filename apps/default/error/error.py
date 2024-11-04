from os import system
from type.colors import Colors
from apps.apphabit import apphabit
class error(apphabit):


	def argparser(self, params):
		args = params.split()

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
				
		

	def __init__(self, id, node, controller, height, width, params):
		self.id = id
		self.node = node
		self.width = width
		self.height = height


		self.text = "Unstable Error"

		system('echo -e "\\a"')
		self.argparser(params)

		self.space = ' ' * self.width

		self.node.ui.coloredTextBox("errormessage", self.displaytext, 1, 0, self.height - 1, self.width)

	def draw(self):
		self.node.appendStr(0, 0, '-' * self.width)
		for y in range(self.height - 1):
			self.node.appendStr(y + 1, 0, self.space)
	
	def onresize(self, height, width):
		self.height = height
		self.width = width
		self.displaytext = self.text.center(self.width, ' ')
		self.space = ' ' * self.width
		self.node.ui.resizeTextBox("errormessage", height - 1, width)