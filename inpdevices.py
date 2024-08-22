import os
import sys
import evdev


EV_MSC = 0x04
EV_KEY = 0x01
BTN_MOUSE = 0x100


fast_hexes = {'0':"0000", '1':"0001", '2':"0010", '3':"0011", '4':"0100", '5':"0101", '6':"0110", '7':"0111", '8':"1000", '9':"1001", 'a':"1010", 'b':"1011", 'c':"1100", 'd':"1101", 'e':"1110", 'f':"1111"}


class DeviceHandler:

	def __init__(self):
		c = True
		self.mouses = []

		#define avaliable keyboard and mouse and use first two
		i = 0
		while c:
			try:
				c = evdev.InputDevice("/dev/input/event" + str(i))
			except:
				c = False
			if c:
				is_mouse = False
				#is_keyboard = False
				poss = open("/sys/class/input/event" + str(i) + "/device/capabilities/ev", 'r')
				capb = hex_to_bin(poss.read())
				if len(capb) >= EV_KEY:
					is_mouse = capb[EV_KEY] == '1'
				#poss = open("/sys/class/input/event" + str(i) + "/device/capabilities/ev", 'r')
				#capb = hex_to_bin(poss.read())
				#if len(capb) > EV_KEY:
				#	is_keyboard = capb[EV_KEY] == '1'
				if is_mouse:
					self.mouses.append("/dev/input/event" + str(i))
					#self.mouses.append(i)
			i += 1
		#input(self.mouses)
		#self.mouses = ["/dev/input/event3"]
		#the code above is half legacy, but intended as a main in the future
		


def hex_to_bin(str_hex):
	num = ''
	i = 0
	for c in str_hex:
		if c == '\n':
			pass
		elif c == ' ':
			num = '0' * (16 - i) + num
			i = 0
		else:
			num = fast_hexes[c] + num
			i += 1
	return num

