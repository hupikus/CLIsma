import os
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
				if i[-1]== "'" or i[-1] == '"':
					self.text = self.text[:-1].center(self.width, ' ')
					mode = ''
				
		

	def __init__(self, id, node, controller, height, width, params):
		self.id = id
		self.node = node
		self.width = width
		self.height = height

		self.preferred_height = 3
		self.preferred_width = 60


		self.text = "Unstable Error"

		os.system('echo -e "\\a"')
		self.argparser(params)



	def draw(self):
		self.node.appendStr(0, 0, '-' * self.width)
		self.node.appendStr(1, 0, self.text)
		self.node.appendStr(2, 0, '-' * self.width)