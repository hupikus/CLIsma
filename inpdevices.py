import os
import sys
class DeviceHandler:

	def hex_to_inv_bin(self):
		pass





	def __init__(self):
		c = True
		self.devnum = -1
		while c:
			c = os.path.isfile("/dev/input/event" + str(self.devnum))
			self.devnum += 1

		#define first avaliable keyboard and mouse
		for i in range(self.devnum):
			poss = file.open("/sys/class/input/event" + str(i) + "/device/capabilities/ev")
			print(poss)
