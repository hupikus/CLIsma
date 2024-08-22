import os
class Error:


	def start(self):
		os.system('echo -e "\\a"')




	def __init__(self, id, node, controller, height, width):
		self.id = id
		self.node = node
		self.width = width
		self.height = height

		self.preferred_height = 3
		self.preferred_width = 60


		self.text = "Unstable Error"
		self.start()



	def draw(self):
		self.node.appendStr(0, 0, "-------------ERROR------------")
		self.node.appendStr(1, 0, self.text)
		self.node.appendStr(2, 0, "-" * self.width)


	def process(self):
		pass

	def abort(self):
		pass