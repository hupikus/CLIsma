import os
import sys
import threading
import time

from worldglobals import worldglobals
from integration.loghandler import Loghandler

from InputSquad.controller import Controller
from InputSquad.mouse import Mice
from InputSquad.midi import Midi
from InputSquad.keyboard import Keyboard


#define
EV_MSC = 0x04
EV_KEY = 0x01
EV_REL = 0x02

BTN_MOUSE = 0x100
REL_X = 0x00
REL_Y = 0x01

KEY_Z = 44
KEY_ENTER = 28
KEY_SPACE = 57

RESCAN_INTERVAL_SEC = 5


reverse_hexes = {'0':"0000", '1':"1000", '2':"0100", '3':"1100", '4':"0010", '5':"1010", '6':"0110", '7':"1110", '8':"0001", '9':"1001", 'a':"0101", 'b':"1101", 'c':"0011", 'd':"1011", 'e':"0111", 'f':"1111"}

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

class DeviceHandler:

	def device_scan(self):
		c = True
		self.mouses = []
		self.keyboards = []
		self.midi = []

		i = 0
		with threading.Lock():
			while True:
				loc = "/dev/input/event" + str(i)
				if os.path.exists(loc):
					is_mouse = False
					is_keyboard = False
					type = ""
					ev = open(f"/sys/class/input/event{i}/device/capabilities/ev", 'r')
					capb = hex_to_bin(ev.read())
					ev.close()

					ln = len(capb)
					if type == '' and ln >= EV_REL:
						rel = open(f"/sys/class/input/event{i}/device/capabilities/rel", 'r')
						relcapb = hex_to_bin(rel.read())
						rel.close()
						#type = "Mouse"
						if len (relcapb) >= REL_Y and relcapb[REL_Y] == '1' and relcapb[REL_X] == '1':
							type = "Mouse"
					if type == '' and ln >= EV_KEY:
						key = open(f"/sys/class/input/event{i}/device/capabilities/key", 'r')
						keycapb = hex_to_bin(key.read())
						key.close()
						#type = "Keyboard"
						if len(keycapb) >= KEY_SPACE and keycapb[KEY_ENTER] == '1':
							if keycapb[KEY_SPACE] == '1':
								type = "Keyboard"


					if type == "Mouse":
						self.mouses.append(loc)
					elif type == "Keyboard":
						self.keyboards.append(loc)
				else: break
				i += 1

			midi = "/dev/snd/"
			if os.path.exists(midi):
				for dev in os.listdir(midi):
					if dev[:4] == "midi":
						devpath = midi + dev
						if os.access(devpath, os.R_OK):
							self.midi.append(devpath)



	def __init__(self):

		self._event_incall = False
		self._update_incall = False


		self.isMouse = False
		self.isKeyboard = False
		self.isMidi = False
		self.working = False
		self.not_abort = True

		self.controller = Controller()

		self.mouse_class = False
		self.keyboard_class = False
		self.midi_class = False

		self.modules =  [self._mouse,      self._midi,      self._keyboard]


		self.scan_exit = threading.Event()
		self.scan_thread = threading.Thread(target = self.scan)
		self.scan_thread.start()




	def scan(self):
		Loghandler.Log(f"Rescan set to every {RESCAN_INTERVAL_SEC} seconds")
		while self.not_abort:
			with threading.Lock():
				self.device_scan()

				self.mouselen = len(self.mouses)
				isMouse = self.mouselen > 0
				isKeyboard = len(self.keyboards) > 0
				isMidi = len(self.midi) > 0
				working = isMouse or isKeyboard or isMidi

				self.modules =  [self._mouse,      self._midi,      self._keyboard]

				if not self.isMouse and isMouse:
					self.isMouse = True
					self.mouse_class = Mice(self.mouses, self.controller)
					self.mouse_range = range(0)
					Loghandler.Log("Initialized input modult: mouse")

				if not self.isKeyboard and isKeyboard:
					self.isKeyboard = True
					self.keyboard_class = Keyboard(self.keyboards, self.controller)
					Loghandler.Log("Initialized input module: keyboard")
					Loghandler.Log("Keyboard connected")

				if not self.isMidi and isMidi:
					self.isMidi = True
					self.midi_class = Midi(self.midi, self.controller)
					Loghandler.Log("Initialized input module: midi")
					Loghandler.Log("Midi keyboard connected")



				if self.mouse_class:
					self.mouse_class.edit(self.mouses)
					if self._update_incall:
						self._update_incall(self.mouselen)
					#cache
					self.mouse_range = range(self.mouselen)

				if self.midi_class:
					self.midi_class.edit(self.midi)
				if self.keyboard_class:
					self.keyboard_class.edit(self.keyboards)



				if not self.working and working:
					self.working = True
					self.input_thread = threading.Thread(target = self._input_loop)
					self.input_thread.start()

			self.scan_exit.wait(RESCAN_INTERVAL_SEC)





	def _input_loop(self):
		timestamp = time.time()
		deltaTime = 0
		while self.working:

			deltaTime = time.time() - timestamp
			timestamp += deltaTime

			if self.isMouse:
				self._mouse()

			if self.isKeyboard:
				self._keyboard()

			if self.isMidi:
				self._midi()

			time.sleep(worldglobals.inputdelta)

			if self._event_incall:
				self._event_incall(deltaTime)




	def _mouse(self):
		self.mouse_class.readevent()

		mouselen = self.controller.mouselen
		# Loghandler.Log(mouselen)
		id = 0
		while id < mouselen:
			controller = self.controller[id]

			controller.mouse_dy = self.mouse_class.y[id]
			controller.mouse_dx = self.mouse_class.x[id]
			controller.mouse_wheel = self.mouse_class.wheel[id]
			controller.raw_mouse_buttons = self.mouse_class.state[id]


			#Loghandler.Log(f"mouse {id} device {dev}: {self.controller[id].mouse_dy} {self.controller[id].mouse_dx} {self.controller[id].mouse_wheel}")
			#Loghandler.Log(f"mouse {id} device {dev}: {self.controller[id].raw_mouse_buttons}")

			id += 1


	def _midi(self):
		self.midi_class.readevent()

	def _keyboard(self):
		self.keyboard_class.readevent()

	def abort(self):
		if self.working:
			self.working = False
			if self.mouse_class: self.mouse_class.abort()
			if self.midi_class: self.midi_class.abort()
			if self.keyboard_class: self.keyboard_class.abort()
			self.scan_exit.set()
		self.not_abort = False

	def listen_to_input(self, event_func, mouse_update_func):
		self._event_incall = event_func
		self._update_incall = mouse_update_func

