from type.colors import Colors
class UI:

	def __init__(self, node):
		self.node = node

		self.ids = ["buttons", "sliders", "fields", "arts", "tapArts", "txts", "textBoxes", "coloredTextBoxes"]

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
			self.node.appendStr(text[1], text[2], text[0], text[3])
		for name in self.uis["textBoxes"]:
			text = self.uis["textBoxes"][name]
			content = text[6]
			for y in range(text[7]):
				self.node.appendStr(text[1] + y, text[2], content[y], text[8])
		#colored text boxes is hell
		for name in self.uis["coloredTextBoxes"]:
			text = self.uis["coloredTextBoxes"][name]
			content = text[5]
			x = 0
			y = 0
			colorMode = Colors.colorPair(0)
			attrMode = Colors.FXNormal
			mode = 'read'
			#for i in content:
			#	self.node.appendStr(text[1] + y, text[2] + x, str(i), colorMode)
			#	x += len(str(i)) + 1
			#break
			for i in content:
				if mode == 'read':
					if i == "<!C":
						mode = 'cread'
					elif i == "<!T":
						mode = 'tread'
					elif i == "<n>":
						y += 1
						x = 0
						if y == text[3]: break
					elif i == "<endc>":
						colorMode = Colors.colorPair(0)
					elif i == "<endt>":
						attrMode = Colors.FXNormal
					else:
						self.node.appendStr(text[1] + y, text[2] + x, i, colorMode)
						x += len(i)
				elif mode == 'cread':
					colorMode = Colors.colorPair(i)
					mode = 'read'
				elif mode == 'tread':
					attrMode = Colors.FXHash[i]
					mode = 'read'



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

	def textLine(self, name, content, y, x, attr = Colors.FXNormal):
		#receive: content, yStart, xStart, attr
		#write: content, yStart, xStart, attr
		self.uis["txts"][name] = [content, y, x, attr]

	def textBox(self, name, content, y, x, height, width, align = 0, attr = Colors.FXNormal):
		#receive: content, yStart, xStart, height, width, align mode, attr
		#write: content, yStart, xStart, height, width, align mode, display text, height of display text, attr
		if height == 0: height = -1
		if width == 0: width = 999
		if align > 2 or align < 0: align = 0
		words = content.replace('\n', '').split()
		display = self.arrangeTextBox(words, height, width, align)
		self.uis["textBoxes"][name] = [words, y, x, height, width, align, display, len(display), attr]
	
	def coloredTextBox(self, name, content, y, x, height, width):
		#receive: content, yStart, xStart, height, width
		#write: content, yStart, xStart, height, width, display text
		if height == 0: height = -1
		if width == 0: width = 999
		words = content.split()
		cache = self.generatecachedtextbox(words, height, width)
		self.uis["coloredTextBoxes"][name] = [words, y, x, height, width, cache]

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
		if name in self.uis["textBoxes"]:
			text = self.uis["textBoxes"][name]
			if height != 0:
				text[3] = height
			text[4] = width
			text[6] = self.arrangeTextBox(text[0], text[3], text[4], text[5])
			text[7] = len(text[6])
		elif name in self.uis["coloredTextBoxes"]:
			text = self.uis["coloredTextBoxes"][name]
			if height != 0:
				text[3] = height
			text[4] = width
			text[5] = self.generatecachedtextbox(text[0], text[3], text[4])
		

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
				startlen = 0
				while True:
					#word is (still) does not fit, cut
					part = w[:l]
					displays[line] = displays[line] + part
					wlen -= l
					startlen = l

					#then start new line
					if wlen == 0: break
					

					if line == height and height > 0: break
					line += 1
					l = width + 1
					displays.append('')

					w = w[startlen:]
					if wlen <= width:
						#we can fit remains at the new line
						displays[line] = w + ' '
						l -= wlen
						break
			else:
				#new line
				line += 1
				
				displays[line - 1] = displays[line - 1][:-1]
				if line == height and height > 0: break

				l = width + 1
				displays.append('')
				displays[line] = w + ' '
				l = l - size - 1
			
			if align > 0:
				if align == 1:
					for i in range(line):
						displays[i] = displays[i].center(width, ' ')
				else:
					for i in range(line):
						displays[i] = displays[i].rjust(width, ' ')
			

		return displays
	
	#private calculation methods

	def generatecachedtextbox(self, words, height, width):
		displays = []
		l = width + 1
		line = 0
		for w in words:
			#size = len(w)
			size = self.tagsoverheadcount(w)
			if size <= l:
				#ok
				#method that divides a word to flags and line break
				newline = self.keepappending(w, displays)
				#instead of #displays.append(w + ' ')
				#if newline >= 0:
				#	l = width + 1 - newline
				#else:
				l = l - size - 1
			elif size > width:
				#fat-wording (жирнословие) or keyspam
				wlen = self.tagsoverheadcount(w)
				startlen = 0
				while True:
					#word is (still) does not fit, cut
					part = w[:l]
					newline = self.keepappending(part, displays)
					
					#if newline >= 0:
					#	l = width + 1 - newline
					displays[-1] = (displays[-1])[:-1]
					#wlen -= len(part)
					wlen -= self.tagsoverheadcount(part)
					startlen = l
					#then start new line
					if wlen == 0: break
					
					line += 1
					l = width + 1
					displays.append("<n>")
					if displays.count("<n>") == height - 1 and height > 0: break
					

					w = w[startlen:]
					if wlen <= width:
						#we can fit remains at the new line
						l -= wlen
						
						self.keepappending(w, displays)
						wlen = 0
						break
			else:
				#new line
				line += 1
				
				if displays.count("<n>") == height - 1 and height > 0: break

				l = width + 1
				displays.append("<n>")
				
				newline = self.keepappending(w, displays)
				#if newline >= 0:
				#	l = width + 1 - newline
				#else:
				l = l - size - 1
			

		return displays
	
	def keepappending(self, w, displays):
		#displays (array) is linked, w (text) is not
		ind = -1
		minlen = 0
		newline = -1
		while True:
			#search for color and attribute tags
			tags = ["<c", "<t", "<endc>", "<endt>", "<n>"]
			indn = [w.find(i) for i in tags]
			temp_lw = len(w)
			if sum(indn) == -5:
				#no more tags
				displays.append(w + ' ')
				newline += temp_lw + 1
				break

			for i in range(5):
				if indn[i] == -1: indn[i] = temp_lw + 1

			ind = min(indn)
			displays.append(w[:ind])
			if newline >= 0:
				newline += len(w[:ind])


			key = tags[indn.index(ind)]
			indend = ind
			if key == "<c":
				minlen += 2
				displays.append('<!C')
				indend = w.find(">")

				if indend == -1:
					#syntax error
					displays.append(0)
				else:
					number = int( w[ind + 2:indend] )
					displays.append(number)
			elif key == "<t":
				minlen += 2
				displays.append('<!T')
				indend = w.find(">")

				if indend == -1:
					#syntax error
					displays.append(normal)
				else:
					displays.append(w[ind + 2:indend])
			else:
				lk = len(key)
				displays.append(key)
				minlen += lk
				indend += lk
				if key == "<n>":
					newline = 0

			#cut a word:
			w = w[indend + 1:]

		return newline
	
	def tagsoverheadcount(self, string):
		d = len(string)
		string = string.replace("<endc>", '').replace("<endt>", '').replace("<n>", '')
		c = len(string)
		if d != c:
			mode = False
			for i in string:
				if i == '<':
					mode = True
				elif i == '>':
					c -= 1
					mode = False
				if mode:
					c -= 1
		return c

