
class UI:

	def __init__(self, node):
		self.node = node

		self.ids = ["buttons", "sliders", "fields"]

		#self.uis = {"buttons":{}, "sliders":{}, "fields":{}} #e.t.c.
		self.uis = {i:{} for i in self.ids}

		self.active = False


		self.active_field_name = ''


	def draw(self):
		for name in self.uis["sliders"]:
			slider = self.uis["sliders"][name]
			self.node.appendStr(slider[1], slider[2], '-' * (slider[4]) + '*' + '-' * (slider[3] - slider[4] - 1))
		for name in self.uis["fields"]:
			field = self.uis["fields"][name]
			self.node.appendStr(field[1], field[2], '_' * field[3])



	def clicked(self, name):
		self.uis["buttons"][name][0](name)



	def click(self, button, y, x):
		r = True
		if button == 0:
			for j in self.uis["buttons"]:
				butt = self.uis["buttons"][j]
				if y >= butt[1] and y <= butt[3]:
					if x >= butt[2] and x <= butt[4]:
						self.clicked(j)
						r = False
			if r:
				for j in self.uis["sliders"]:
					slider = self.uis["sliders"][j]
					if y == slider[1]:
						if x >= slider[2] and x <= field[2] - slider[3]:
							#self.clicked(j)
							slider[4] = x - slider[2]
							r = False
			if r:
				for j in self.uis["fields"]:
					field = self.uis["fields"][j]
					if y == field[1]:
						if x >= field[2] and x <= field[2] - field[3]:
							self.active_field_name = j
							field[5] = x - field[2]
							r = False
		if r:
			self.active_field_name = ''
		return r
		
	
	#creation

	def clickArea(self, name, event, y, x, height, width):
		#receive: event, yStart, xStart, height, width
		#write: event, yStart, xStart, yEnd, xEnd
		self.uis["buttons"][name] = [event, y, x, y + height, x + width]

	def slider(self, name, event, y, x, width):
		#receive: event, y, x, width
		#write: event, y, x, width, position
		self.uis["sliders"][name] = [event, y, x, width, 5]

	def textField(self, name, var, y, x, width, maxlen = -1):
		#receive: variable to write input to, y, x, width, max length of an input: -1 to disable
		#write: variable, y, x, width, max len, text cursor position
		self.uis["fields"][name] = [var, y, x, width, maxlen, cursorpos]

	#commands

	def move(self, name, y, x):
		
		i = self.uis["buttons"][name]
		if not i:
			for id in self.ids[1:]:
				i = self.uis[id][name]
				if i:
					break
		if i:
			i[0] += y
			i[1] += x
