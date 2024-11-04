import os
import struct
import evdev

EV_KEY = 0x01
EV_REL = 0x02

BTN_LEFT = 0x110
BTN_RIGHT = 0x111
BTN_MIDDLE = 0x112

REL_X = 0x00
REL_Y = 0x01

REL_WHEEL = 0x08

class Mice():
	def readevent(self):
		self.y = 0
		self.x = 0
		self.wheel = 0
		for dev in self.devices:
			try:
				events = dev.read()
				if events:
					for event in events:
						if event.type == EV_REL:
							if event.code == REL_Y:
			 					self.y += event.value * 0.67
							elif event.code == REL_X:
			 					self.x += event.value
							elif event.code == REL_WHEEL:
			 					self.wheel -= event.value
						if event.type == EV_KEY:
							if event.code >= BTN_LEFT and event.code <= BTN_MIDDLE:
								self.state[event.code - BTN_LEFT] = event.value
			except:
				continue

	def abort(self):
		self.mice.close()

	def __init__(self, inpd, id):
		self.inpd = inpd
		self.id = id
		self.y, self.x = 0, 0

		self.wheel = 0

		#mouse init
		self.speed = 1.0
		self.state = [0, 0, 0]
		if os.path.exists("/dev/input/mice"):
			self.mice = open("/dev/input/mice", "rb")
		elif os.path.exists("/dev/input/mouse0"):
#		else:
			self.mice = open("/dev/input/mouse0", "rb")

		self.devices = inpd.mouse_devices
		#self.mice = open("/dev/input/event3", "rb")

