import os
import sys
import evdev
import threading
import time
#import asyncio

from worldglobals import worldglobals

from controller import Controller
from mouse import Mice

from loghandler import Loghandler


EV_MSC = 0x04
EV_KEY = 0x01
BTN_MOUSE = 0x100


fast_hexes = {'0':"0000", '1':"0001", '2':"0010", '3':"0011", '4':"0100", '5':"0101", '6':"0110", '7':"0111", '8':"1000", '9':"1001", 'a':"1010", 'b':"1011", 'c':"1100", 'd':"1101", 'e':"1110", 'f':"1111"}


class DeviceHandler:

	def __init__(self):
		c = True
		self.mouses = []
		self._incall = self.passy

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
				#self.mouses.append("/dev/input/event5")
			i += 1

		self.isMouse = len(self.mouses) > 0
		self.controller = Controller(self.isMouse)

		if self.isMouse:
			self.mouse_devices = [evdev.InputDevice(device) for device in self.mouses]
			self.mouse_class = Mice(self, worldglobals.pointers_count)

			worldglobals.pointers_count += 1

			self.input_thread = threading.Thread(target = self._mouse)
			#self.input_thread = threading.Thread(target = self.mouse_class.readevent)
			self.input_thread.start()
	
		

	def _mouse(self):
		while self.isMouse:
			self.mouse_class.readevent()
			#self.mouse_class.process()
			self.controller.mouse_dy = self.mouse_class.y
			self.controller.mouse_dx = self.mouse_class.x
			self.controller.raw_mouse_buttons = self.mouse_class.state
			self.controller.mouse_wheel = self.mouse_class.wheel
			#Loghandler.Log(f"{self.controller.mouse_dy} {self.controller.mouse_dx} {self.controller.mouse_wheel}")
			time.sleep(worldglobals.inputdelta)
			self._incall(self.mouse_class.id)
	
	def abort(self):
		self.isMouse = False
		self.mouse_class.abort()

	def listen_to_mouse(self, method):
		self._incall = method
	
	def passy(self, mouse_class):
		pass


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

