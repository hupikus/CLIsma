
class UI:

	def __init__(self, node):
		self.node = node

		self.ids = ["buttons", "sliders", "fields", "arts", "tapArts", "txts", "textBoxes"]

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
		for name in self.uis["arts"]:
			art = self.uis["arts"][name]
			content = art[0]
			for y in range(art[3]):
				self.node.appendStr(art[1] + y, art[2], content[y])
		for name in self.uis["tapArts"]:
			art = self.uis["tapArts"][name]
			content = art[5]
			for y in range(art[3] - art[1]):
				self.node.appendStr(art[1] + y, art[2], content[y])
		for name in self.uis["txts"]:
			text = self.uis["txts"][name]
			self.node.appendStr(text[1], text[2], text[0])
		for name in self.uis["textBoxes"]:
			text = self.uis["textBoxes"][name]
			content = text[6]
			for y in range(text[7]):
				self.node.appendStr(text[1] + y, text[2], content[y])




	def click(self, button, y, x):
		r = True
		arg_invoke = False
		for j in self.uis["buttons"]:
			butt = self.uis["buttons"][j]
			if y >= butt[1] and y < butt[3]:
				if x >= butt[2] and x < butt[4]:
					arg_invoke = [j, "buttons", button]
					r = False
					break
		if r:
			for j in self.uis["tapArts"]:
				abutt = self.uis["tapArts"][j]
				if y >= abutt[1] and y < abutt[3]:
					if x >= abutt[2] and x < abutt[4]:
						arg_invoke = [j, "tapArts", button]
						r = False
						break
		if button == 0:
			if r:
				for j in self.uis["sliders"]:
					slider = self.uis["sliders"][j]
					if y == slider[1]:
						if x >= slider[2] and x < slider[2] + slider[3]:
							slider[4] = x - slider[2]
							slider[0](slider[4])
							r = False
							break
			if r:
				for j in self.uis["fields"]:
					field = self.uis["fields"][j]
					if y == field[1]:
						if x >= field[2] and x <= field[2] + field[3]:
							self.active_field_name = j
							field[5] = x - field[2]
							r = False
							break
		if r:
			self.active_field_name = ''
		else:
			if arg_invoke != False:
				self.clicked(*arg_invoke)
		return r
		
	
	#creation

	def clickArea(self, name, event, y, x, height, width):
		#receive: event, yStart, xStart, height, width
		#write: event, yStart, xStart, yEnd, xEnd
		self.uis["buttons"][name] = [event, y, x, y + height, x + width]
	
	def art(self, name, content, y, x):
		#receive: content, yStart, xStart
		#write: content, yStart, xStart, height
		self.uis["arts"][name] = [content, y, x, len(content)]

	def clickableArt(self, name, event, y, x, content, width = 1):
		#receive: event, yStart, xStart, content, width (unnecessary)
		#write: event, yStart, xStart, yEnd, xEnd, content

		if width <= 1:
			for i in content:
				g = len(i)
				if g > width:
					width = g
		
		self.uis["tapArts"][name] = [event, y, x, y + len(content), x + width, content]

	def textLine(self, name, content, y, x):
		#receive: content, yStart, xStart
		#write: content, yStart, xStart
		self.uis["txts"][name] = [content, y, x]

	def textBox(self, name, content, y, x, height, width, align = 0):
		#receive: content, yStart, xStart, height, width, align mode
		#write: content, yStart, xStart, height, width, align mode, display text, height of display text
		if height == 0: height = -1
		if width == 0: width = 999
		if align > 2 or align < 0: align = 0
		words = content.split()
		display = self.arrangeTextBox(words, height, width, align)
		self.uis["textBoxes"][name] = [words, y, x, height, width, align, display, len(display)]

	def slider(self, name, event, y, x, width, srartPos):
		#receive: event, y, x, width, srartPosition
		#write: event, y, x, width, position
		self.uis["sliders"][name] = [event, y, x, width, srartPos]

	def textField(self, name, var, y, x, width, maxlen = -1):
		#receive: variable to write input to, y, x, width, max length of an input: -1 to disable
		#write: variable, y, x, width, max len, text cursor position
		self.uis["fields"][name] = [var, y, x, width, maxlen, cursorpos]


	#commands

	def move(self, name, y, x, type = ''):
		if type == '':
			for type in self.ids:
				if name in self.uis[type]:
					i = self.uis[type][name]
					break
		if i:
			i[1] += y
			i[2] += x

			if type in ["buttons", "tapArts"]:
				#adjust yEnd and xEnd
				i[3] += y
				i[4] += x
	
	def moveTo(self, name, y, x, type = ''):
		if type == '':
			for type in self.ids:
				if name in self.uis[type]:
					break

		if i:
			if type in ["buttons", "tapArts"]:
				#adjust yEnd and xEnd
				i[3] += y - i[1]
				i[4] += x - i[2]

			i[1] = y
			i[2] = x


	#custom events

	def clicked(self, name, type, button):
		self.uis[type][name][0](name, button)
	
	def resizeTextBox(self, name, height, width):
		text = self.uis["textBoxes"][name]
		if height != 0:
			text[3] = height
		text[4] = width
		text[6] = self.arrangeTextBox(text[0], text[3], text[4], text[5])
		text[7] = len(text[6])
		

	#public calculation events
	def arrangeTextBox(self, words, height, width, align):
		displays = ['']
		l = width + 1
		line = 0
		for w in words:
			size = len(w)
			if size <= l:
				#ok
				displays[line] = displays[line] + w + ' '
				l = l - size - 1
			elif size > width:
				#fat-wording (жирнословие) or keyspam
				wlen = len(w)

				while True:
					#word is (still) does not fit, cut
					part = w[:l]
					displays[line] = displays[line] + part
					wlen -= len(part)
					l = 0
					#then start new line
					if wlen == 0: break
					

					if line == height and height > 0: break
					line += 1
					l = width + 1
					displays.append('')

					if wlen <= width:
						#we can fit remains at the new line
						l -= wlen
						w = w[wlen:]
						displays[line] = displays[line] + w + ' '
						wlen = 0
						break
			else:
				#new line
				line += 1
				
				displays[line - 1] = displays[line - 1][:-1]
				if line == height and height > 0: break

				l = width + 1
				displays.append('')
				displays[line] = displays[line] + w + ' '
				l = l - size - 1
			
			if align > 0:
				if align == 1:
					for i in range(line):
						displays[i] = displays[i].center(width, ' ')
				else:
					for i in range(line):
						displays[i] = displays[i].rjust(width, ' ')
			

		return displays