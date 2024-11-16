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
EV_REL = 0x02

BTN_MOUSE = 0x100
REL_X = 0x00
REL_Y = 0x01

KEY_Z = 44

fast_hexes = {'0':"0000", '1':"0001", '2':"0010", '3':"0011", '4':"0100", '5':"0101", '6':"0110", '7':"0111", '8':"1000", '9':"1001", 'a':"1010", 'b':"1011", 'c':"1100", 'd':"1101", 'e':"1110", 'f':"1111"}
reverse_hexes = {'0':"0000", '1':"1000", '2':"0100", '3':"1100", '4':"0010", '5':"1010", '6':"0110", '7':"1110", '8':"0001", '9':"1001", 'a':"0101", 'b':"1101", 'c':"0011", 'd':"1011", 'e':"0111", 'f':"1111"}


class DeviceHandler:

	def __init__(self):
		c = True
		self.mouses = []
		self.keyboards = []
		self._incall = self.passy

		#define avaliable keyboard and mouse and use first two
		i = 0
		while True:
			loc = "/dev/input/event" + str(i)
			if os.path.exists(loc):
				is_mouse = False
				is_keyboard = False
				type = "Unknown Device"
				ev = open(f"/sys/class/input/event{i}/device/capabilities/ev", 'r')
				capb = hex_to_bin(ev.read())
				ev.close()

				ln = len(capb)
				if ln >= EV_REL:
					rel = open(f"/sys/class/input/event{i}/device/capabilities/rel", 'r')
					relcapb = hex_to_bin(rel.read())
					rel.close()
					#type = "Mouse"
					if len (relcapb) >= REL_Y and relcapb[REL_Y] == '1' and relcapb[REL_X] == '1':
						type = "Mouse"
				elif ln >= EV_KEY:
					rel = open(f"/sys/class/input/event{i}/device/capabilities/rel", 'r')
					relcapb = hex_to_bin(rel.read())
					rel.close()
					#type = "Mouse"
					if len (relcapb) >= REL_Y and relcapb[REL_Y] == '1' and relcapb[REL_X] == '1':
						type = "Keyboard"


				if type == "Mouse":
					self.mouses.append(loc)
				elif type == "Keyboard":
					self.keyboards.append(loc)
			else: break
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
	bin = ''
	i = 0
	for c in str_hex[::-1]:
		if c == '\n':
			continue
		elif c  == ' ':
			bin += str(4 * (16 - i))
			i = 0
		else:
			bin += reverse_hexes[c]
			i += 1
	return bin