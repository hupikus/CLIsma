import os
import struct
import evdev

class Mice():


	#for /dev/input/mice
	def process(self):
		buf = self.mice.read(3)

		self.x, self.y = struct.unpack("bb", buf[1:])
		#self.ratx = max(min(self.ratx + self.dx * self.speed, self.width - 1), 0)
		#self.raty = max(min(self.raty - self.dy * self.speed, self.height - 2), 0)


	def state_update(self):
		self.state = [0, 0, 0]
		#keys = self.devices[0].active_keys()
		#self.state = [272 in keys, 273 in keys,  274 in keys]

		#272 - 274: mouse buttons (left, middle, right)
		for dev in self.devices:
			keys = dev.active_keys()
			self.state = [self.state[0] or 272 in keys, self.state[1] or 273 in keys, self.state[2] or 274 in keys]
			for q in range(3):
				if self.state[q] == 0:
					self.state[q] = self.state[q] or (272 + q) in keys

	def readevent(self):
		self.relstate = [6 in keys]
		try:
			for event in dev.read():
				self.relstate = self.relstate + event
		except:
			self.relstate = [3]

	def abort(self):
		self.mice.close()

	def __init__(self, inpd):
		self.y,  self.x = 0, 0

		self.relstate = [6]
		self.wheel = 0

		#mouse init
		self.speed = 1.0
		self.state = [0, 0, 0]
		if os.path.exists("/dev/input/mice"):
			self.mice = open("/dev/input/mice", "rb")
		elif os.path.exists("/dev/input/mouse0"):
#		else:
			self.mice = open("/dev/input/mouse0", "rb")

		self.devices = [evdev.InputDevice(device) for device in inpd.mouses]
		#self.mice = open("/dev/input/event3", "rb")

