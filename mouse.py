import os
import struct
import evdev

class Mice():


	#for /dev/input/mice
	def process(self):
		if self.isMouse:
			buf = self.mice.read(3)

			self.dx, self.dy = struct.unpack("bb", buf[1:])
			#self.dy *= 1.25
			self.rx += self.dx
			self.ry -= self.dy
			self.ratx = max(min(self.ratx + self.dx * self.speed, self.width - 1), 0)
			self.raty = max(min(self.raty - self.dy * self.speed, self.height - 2), 0)
			self.x = round(self.ratx)
			self.y = round(self.raty)


	def state_update(self):
		self.state = [0, 0, 0]
		#keys = self.devices[0].active_keys()
		#self.state = [272 in keys, 273 in keys,  274 in keys]

		#272 - 274: mouse buttons (left, middle, right)
		for dev in self.devices:
			keys = dev.active_keys()
			self.state = [self.state[0] or 272 in keys, self.state[1] or 273 in keys, self.state[2] or 274 in keys]

			self.relstate = [6 in keys]
			for q in range(3):
				if self.state[q] == 0:
					self.state[q] = self.state[q] or (272 + q) in keys

	def abort(self):
		pass
	#	if self.isMouse:
	#		self.mice.close()




	def __init__(self, width, height, speed, inpd):
		self.width = width
		self.height = height
		self.x,  self.y = (0, 0)
		self.rx, self.ry = (0, 0)
		self.ratx, self.raty = (0.0, 0.0)
		self.dx, self.dy = (0, 0)
		

		self.wheel = 0

		self.isMouse = True


		#mouse init
		self.speed = speed
		self.state = [0, 0, 0]
		if os.path.exists("/dev/input/mice"):
			self.mice = open("/dev/input/mice", "rb")
		elif os.path.exists("/dev/input/mouse0"):
#		else:
			self.mice = open("/dev/input/mouse0", "rb")
		else:
			self.isMouse = False

		self.devices = inpd.mouses
		n = 0
		for device in self.devices:
			self.devices[n] = evdev.InputDevice(device)
			n += 1
		#self.mice = open("/dev/input/event3", "rb")
