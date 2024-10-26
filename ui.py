
class UI:

	def __init__(self, node):
		self.node = node
		self.els = {"buttons":{}, "sliders":{}}
		self.hsh = {"buttons":[], "sliders":[]}
		self.active = False


	def draw(self):
		for name in self.hsh["sliders"]:
			slider = self.els["sliders"][name]
			self.node.appendStr(slider[1], slider[2], '-' * (slider[4]) + '*' + '-' * (slider[3] - slider[4] - 1))



	def clicked(self, name):
		self.els["buttons"][name][0](name)
		#self.node.win.state = "shutdown"



	def click(self, button, y, x):
		r = True
		for j in self.hsh["buttons"]:
			button = self.els["buttons"][j]
			if y >= button[1] and y <= button[3]:
				if x >= button[2] and x <= button[4]:
					self.clicked(j)
					r = False
		if r:
			for j in self.hsh["sliders"]:
				slider = self.els["sliders"][j]
				if y == slider[1]:
					if x >= slider[2] and x <= slider[3]:
						#self.clicked(j)
						slider[4] = x - slider[2]
						r = False
		return r

	def clickArea(self, name, event, y, x, height, width):
		#event, yStart, xStart, yEnd, xEnd
		self.els["buttons"][name] = [event, y, x, y + height, x + width]
		self.hsh["buttons"].append(name)



	def slider(self, name, event, y, x, width):
		#event, y, x, xEnd, position
		self.els["sliders"][name] = [event, y, x, x + width, 5]
		self.hsh["sliders"].append(name)


	def move(self, name, y, x):
		i = self.els["buttons"][name]
		if i:
			i[0] += y
			i[1] += x
