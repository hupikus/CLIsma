from type.inpevents import InputEvents

from InputSquad.controllers.midi_controller import MidiController

class Controller:

	def resize_pointers(self, size):
		if size <= 0: return
		if size > self.mouselen:
			for i in range(size - self.mouselen):
				self.minicontroller.append(miniMouseController(self.mouselen))
				self.mouselen += 1
				if self.mouselen == 1:
					self.fn = self.minicontroller[0]
		else:
			self.minicontroller = self.minicontroller[:size]
			self.mouselen = size

	def __init__(self):
		#raw
		self.mouselen = 0
		self.minicontroller = []

		self.fn = self

		#input types binds
		self.MouseEvents = InputEvents.MOUSE
		self.MouseWheelEvents = InputEvents.MOUSEWHEEL

		self.startDragEvent = 0
		self.dragEvent = 1
		self.endDragEvent = 2

		#temp
		self.key = -1


		#controller modules

		self.midi_listen = []
		self.midi = MidiController(self)
		self.MidiKeyboardEvents = InputEvents.MIDI

		self.keyboard_listen = []
		self.keyboard = None
		self.KeyboardEvents = InputEvents.KEYBOARD

		#add: self.touchscreen, self.gamepad, self.micro



	def __getitem__(self, id = None):
		if id is None or id > self.mouselen or id < 0:
			return self
		return self.minicontroller[id]

	#public

	def listenEvent(self, node, event):
		match event:
			case self.KeyboardEvents:
				self.keyboard_listen.append(node)
			case self.MidiKeyboardEvents:
				self.midi_listen.append(node)

	def getPlayerNumber(self):
		return self.mouselen

	def relMousePos(self, node):
		return self.mouse_y - node.from_y, self.mouse_x - node.from_x

	def isAtWindow(self, node):
		return self.mouse_y >= node.from_y and self.mouse_y <= node.to_y and self.mouse_x >= node.from_x and self.mouse_x <= node.to_x

	#properties (fucking abomination)

	@property
	def mouse_dy(self): return self.fn.mouse_dy
	@mouse_dy.setter
	def mouse_dy(self, val):
		self.fn.mouse_dy = val

	@property
	def mouse_dx(self): return self.fn.mouse_dx
	@mouse_dx.setter
	def mouse_dx(self, val):
		self.fn.mouse_dx = val

	@property
	def raw_mouse_buttons(self): return self.fn.raw_mouse_buttons
	@raw_mouse_buttons.setter
	def raw_mouse_buttons(self, val):
		self.fn.raw_mouse_buttons = val

	@property
	def mouse_wheel(self): return self.fn.mouse_wheel
	@mouse_wheel.setter
	def mouse_wheel(self, val):
		self.fn.mouse_wheel = val

	@property
	def mouse_ry(self): return self.fn.mouse_ry
	@mouse_ry.setter
	def mouse_ry(self, val):
		self.fn.mouse_ry = val

	@property
	def mouse_rx(self): return self.fn.mouse_rx
	@mouse_rx.setter
	def mouse_rx(self, val):
		self.fn.mouse_rx = val

	@property
	def mouse_rdy(self): return self.fn.mouse_rdy
	@mouse_rdy.setter
	def mouse_rdy(self, val):
		self.fn.mouse_rdy = val

	@property
	def mouse_rdx(self): return self.fn.mouse_rdx
	@mouse_rdx.setter
	def mouse_rdx(self, val):
		self.fn.mouse_rdx = val

	@property
	def mouse_y(self): return self.fn.mouse_y
	@mouse_y.setter
	def mouse_y(self, val):
		self.fn.mouse_y = val

	@property
	def mouse_x(self): return self.fn.mouse_x
	@mouse_x.setter
	def mouse_x(self, val):
		self.fn.mouse_x = val

	@property
	def mouse_last_y(self): return self.fn.mouse_last_y
	@mouse_last_y.setter
	def mouse_last_y(self, val):
		self.fn.mouse_last_y = val

	@property
	def mouse_last_x(self): return self.fn.mouse_last_x
	@mouse_last_x.setter
	def mouse_last_x(self, val):
		self.fn.mouse_last_x = val

	@property
	def mouse_buttons(self): return self.fn.mouse_buttons
	@mouse_buttons.setter
	def mouse_buttons(self, val):
		self.fn.mouse_buttons = val

	@property
	def mouse_speed(self): return self.fn.mouse_speed
	@mouse_speed.setter
	def mouse_speed(self, val):
		self.fn.mouse_speed = val

	#end of (fucking abomination)


class miniMouseController:

	def __init__(self, id):
		#raw
		self.id = id
		self.mouse_dy, self.mouse_dx = (0, 0)
		self.raw_mouse_buttons = [0, 0, 0]
		self.mouse_wheel = 0
		#from wm
		self.mouse_ry, self.mouse_rx = (0.0, 0.0)
		self.mouse_rdy, self.mouse_rdx = (0, 0)
		self.mouse_y, self.mouse_x = (0, 0)
		self.mouse_last_y, self.mouse_last_x = (0, 0)
		self.mouse_buttons = [0, 0, 0]
		self.mouse_speed = 0.35

		self.startDragEvent = 0
		self.dragEvent = 1
		self.endDragEvent = 2


	def relMousePos(node):
		return self.mouse_y - node.from_y, self.mouse_x - node.from_x

	def isAtWindow(self, node):
		return self.mouse_y >= node.from_y and self.mouse_y <= node.to_y and self.mouse_x >= node.from_x and self.mouse_x <= node.to_x
