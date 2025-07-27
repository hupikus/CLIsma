from type.colors import Colors
from type.descriptor import Descriptor

from integration.loghandler import Loghandler, Lolhandler
from integration.appconfig import Appconfig

from utils.music_theory import noteName, getOctave

from apps.apphabit import apphabit

note_type_shapes = [0, 2, 1, 2, 0, 0, 2, 1, 2, 1, 2, 0]

class midiplayer(apphabit):

	def __init__(self, id, node, controller, height, width, params):
		#base
		self.id = id
		self.node = node
		self.ui = node.ui
		self.controller = controller

		#input
		self.input_subscriptions = [controller.MouseEvents, controller.MidiKeyboardEvents]


		#self.descriptor = Appconfig.OpenConfig(node.app)

		#self.config = Appconfig.ReadConfig(self.descriptor)

		self.note = "Play a note with your midi keyboard"

		self.blackcolor = Colors.getColorPair(Colors.FXWhite, Colors.FXBlue)
		self.whitecolor = Colors.getColorPair(Colors.FXBlack, Colors.FXWhite)
		self.bgcolor = Colors.getColorPair(Colors.FXBlack, Colors.FXYellow)
		self.cursorcolor = Colors.getColorPair(Colors.FXWhite, Colors.FXBlue)


		#magic numbers
		self.blacks = (1, 3, 7, 9, 11)
		self.max_keyboard_width = 14 * 9 # 9 octaves
		self.keyboard_height = 7

		self.onresize(height, width)

		#cache
		self.pressed_keys = {}
		height = self.keyboard_height
		rng1 = range((height >> 1) + 1)
		rng2 = range((height >> 1) + 1, height)

		#for y in range(4, 150, 33):
		#	self.highlight(y)
		#self.highlight(10)


		self.note_shapes = [ 	tuple(['░' for i in rng1] + ['░░' for i in rng2]),
								tuple(['' for i in rng1] + ['░░' for i in rng2]),
								tuple(['░░' for i in rng1] + ['' for i in rng2])
							]

		# generating click areas


		#note descriptions
		self.ui.textLine("desc", "C D E F G A B " * 9, self.height - height - 1, 0, attr = self.bgcolor)



	def draw(self, delta):
		self.node.clear(attr = self.bgcolor, char = '░', margin_bottom = 7)

		#self.node.appendStr(0, 0, self.note)

		height = self.keyboard_height
		width = min(self.keyboard_width, self.width)

		xstart = (self.width >> 1) - (self.keyboard_width >> 1)

		#draw note guide
		self.ui.moveTo("desc", self.height - height - 1, xstart, type = "txts")
		n = getOctave(self.start_note)
		x = 0
		while x < width:
			self.node.appendStr(self.height - height - 2, xstart + x, str(n) + ' ' * 13, mode = self.bgcolor)
			n += 1
			x += 14

		for y in range(height):
			self.node.appendStr(self.height - height + y, xstart, self.space, mode = self.whitecolor)
			fx, fy = self.node.from_x, self.node.from_y
			if y <= height >> 1:
				x = 0
				while x < width:
					for px in self.blacks:
						t = '  '
						t = '││'
						if y == height >> 1:
							t = '└┘'
						self.node.appendStr(self.height - height + y, x + px + xstart, t, mode = self.blackcolor)

					x += 14
			elif y == height - 1:
				pass


			# draw pressed notes over
			for tone in self.pressed_keys:
				if tone < self.start_note or tone < 0: continue
				note = self.pressed_keys[tone]

				posx = tone - self.start_note + xstart
				tone_offset = max(0, tone - self.start_note)

				posx += round(max(0, tone_offset - 4) / 12 + 0.5) #every E->F compensation
				posx += round((tone_offset - 11) / 12 + 0.5) #every B->C compensation

				if posx < 0: continue
				right_align = note[1]
				shape = self.note_shapes[note[0]]
				for y in range(height):
					char = shape[y]
					dx = 0
					if right_align and len(char) == 1:
						dx = 1
					self.node.appendStr(self.height - height + y, posx + dx, char, mode = self.cursorcolor)

	def onresize(self, height, width):
		self.height = height
		self.width = width


		self.keyboard_width = min(self.max_keyboard_width, self.width)
		self.space = ' ' * self.keyboard_width

		self.start_note = 6 * ((self.max_keyboard_width - self.keyboard_width) // 14) # half of: hidden semitones in a octave. That means keyboard will likely show the center of avaliable note list.

	#def abort(self):
		#Appconfig.CloseConfig(self.descriptor)

	def midikeyPress(self, note, presure):
		self.note = noteName(note)

	def highlight(self, note):
		height = self.keyboard_height
		keytype = note % 12
		shape = note_type_shapes[keytype]
		right_align = False
		if keytype in (4, 11):
			right_align = True # align to the right
		self.pressed_keys[note] = (shape, right_align)







