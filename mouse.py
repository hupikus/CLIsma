import os
import struct

class Mice():

	def process(self):
		if self.isMouse:
			#buf = self.mice.read(3)
			buf = self.mice.read(3)
			button = ord(str(buf[0])[0])
			bleft = button & 0x1
			bmid = (button & 0x4)
			bright = (button & 0x2)

			self.state = [bleft, bmid, bright]

			self.dx, self.dy = struct.unpack("bb", buf[1:])
			#self.dy *= 1.25
			self.rx += self.dx
			self.ry -= self.dy
			self.ratx = max(min(self.ratx + self.dx * self.speed, self.width - 1), 0)
			self.raty = max(min(self.raty - self.dy * self.speed, self.height - 2), 0)
			self.x = round(self.ratx)
			self.y = round(self.raty)



	def abort(self):
		if self.isMouse:
			self.mice.close()




	def __init__(self, width, height, speed):
		self.width = width
		self.height = height
		self.x,  self.y = (0, 0)
		self.rx, self.ry = (0, 0)
		self.ratx, self.raty = (0.0, 0.0)
		self.dx, self.dy = (0, 0)
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
