import os
import sys
import threading
import time
#import asyncio

from worldglobals import worldglobals

from InputSquad.controller import Controller
from InputSquad.mouse import Mice

from integration.loghandler import Loghandler

#define
EV_MSC = 0x04
EV_KEY = 0x01
EV_REL = 0x02

BTN_MOUSE = 0x100
REL_X = 0x00
REL_Y = 0x01

KEY_Z = 44

SEPARATE_DEBUG_CURSORS = False

reverse_hexes = {'0':"0000", '1':"1000", '2':"0100", '3':"1100", '4':"0010", '5':"1010", '6':"0110", '7':"1110", '8':"0001", '9':"1001", 'a':"0101", 'b':"1101", 'c':"0011", 'd':"1011", 'e':"0111", 'f':"1111"}

class DeviceHandler:

	def __init__(self):
		c = True
		self.mouses = []
		self.keyboards = []
		self._incall = []

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
					key = open(f"/sys/class/input/event{i}/device/capabilities/rel", 'r')
					keycapb = hex_to_bin(rel.read())
					key.close()
					#type = "Keyboard"
					if len(keycapb) >= KEY_Z and keycapb[KEY_Z] == '1':
						type = "Keyboard"


				if type == "Mouse":
					self.mouses.append(loc)
				elif type == "Keyboard":
					self.keyboards.append(loc)
			else: break
			i += 1

		self.mouselen = len(self.mouses)
		self.cursorlen = 0
		self.isMouse = self.mouselen > 0
		self.controller = Controller()

		if self.isMouse:
			self.mouse_class = Mice(self.mouses)

			self.pointer_events = [0 for i in range(self.mouselen)]
			self.fake_events = self.pointer_events[:]

			#cache
			self.mouse_range = range(self.mouselen)
			self.pointer_range = range(0)

			#thread
			self.queue_cursor = 0
			self.input_thread = threading.Thread(target = self._mouse)
			self.input_thread.start()


	def _mouse(self):
		while self.isMouse:
			if self.cursorlen > 0 and not self.queue_cursor:
				self.mouse_class.readevent()
				first = [True for i in self.pointer_range]

				for dev in self.mouse_range:
					id = self.pointer_events[dev]

					
					if first[id]:
						self.controller[id].mouse_dy = self.mouse_class.y[dev]
						self.controller[id].mouse_dx = self.mouse_class.x[dev]
						self.controller[id].mouse_wheel = self.mouse_class.wheel[dev]
						self.controller[id].raw_mouse_buttons = self.mouse_class.state[dev]
						#first[id] = False
					else:
						self.controller[id].mouse_dy += self.mouse_class.y[dev]
						self.controller[id].mouse_dx += self.mouse_class.x[dev]
						self.controller[id].mouse_wheel += self.mouse_class.wheel[dev]
						for i in range(3):
							self.controller[id].raw_mouse_buttons[i] = self.controller[id].raw_mouse_buttons[i] or self.mouse_class.state[dev][i]


					#Loghandler.Log(f"mouse {id} device {dev}: {self.controller[id].mouse_dy} {self.controller[id].mouse_dx} {self.controller[id].mouse_wheel}")
					#Loghandler.Log(f"mouse {id} device {dev}: {self.controller[id].raw_mouse_buttons}")


				for id in self.pointer_range:
					self._incall[id]()

			time.sleep(worldglobals.inputdelta)

			if self.queue_cursor:
				self.pointer_range = range(self.cursorlen)
				self.pointer_events = self.fake_events[:]

				Loghandler.Log("New pointer rules applied")
				self.queue_cursor = False
	
	def abort(self):
		self.isMouse = False
		self.mouse_class.abort()

	def listen_to_mouse(self, method, devs):
		self._incall.append(method)
		if not self.queue_cursor:
			self.fake_events = self.pointer_events[:]
		for i in devs:
			self.fake_events[i] = self.cursorlen

		Loghandler.Log(f"New pointer allocated, id: {self.cursorlen}")
		self.cursorlen += 1
		control = self.controller.connect_pointer()

		self.queue_cursor = True
		return control
	
	def connect_mouse(self):
		self.pointer_events.append(0)
		self.mouselen += 1
		self.mouse_range = range(self.mouselen)
		Loghandler.Log(f"New mouse device connected, binded to main pointer")

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