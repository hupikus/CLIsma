import os
import struct

from InputSquad.device import Device
from integration.loghandler import Loghandler

EV_KEY = 0x01
EV_REL = 0x02

BTN_LEFT = 0x110
BTN_RIGHT = 0x111
BTN_MIDDLE = 0x112

BTN_SIDE = 0x113
BTN_EXTRA = 0x114

BTN_BACK = 0x115
BTN_FORWARD = 0x116

REL_X = 0x00
REL_Y = 0x01

REL_WHEEL = 0x08

EV_STRUCT = "llHHi"
EV_SIZE = struct.calcsize(EV_STRUCT)
EV_COUNT = 64

USE_EVDEV = False



def resize_array(arr, size, fill = 0):
    arrlen = len(arr)
    if arrlen >= size:
        return arr[:size]
    return arr + [fill] * (size - arrlen)



class Mice(Device):

	def readevent_os(self):
		for id in self.devicerange:
			try:
				self.y[id] = 0
				self.x[id] = 0
				self.wheel[id] = 0
				events = os.read(self.devicelist[id], EV_SIZE * EV_COUNT)
				if not events:
					continue

				EV_ACTUAL_SIZE = len(events)

				for event in range(0, EV_ACTUAL_SIZE, EV_SIZE):
					_time, _time, EV_TYPE, EV_CODE, EV_VAL = struct.unpack(EV_STRUCT, events[event : event + EV_SIZE])

					if EV_TYPE == EV_REL:
						if EV_CODE == REL_Y:
							self.y[id] = EV_VAL * 0.67
						elif EV_CODE == REL_X:
							self.x[id] = EV_VAL
						elif EV_CODE == REL_WHEEL:
							self.wheel[id] -= EV_VAL
					elif EV_TYPE == EV_KEY:
						if BTN_LEFT <= EV_CODE <= BTN_MIDDLE:
							self.state[id][EV_CODE - BTN_LEFT] = EV_VAL
			except:
				continue

	def readevent_evdev(self):
		for id in self.devicerange:
			try:
				events = self.devicelist[id].read()
				self.y[id] = 0
				self.x[id] = 0
				self.wheel[id] = 0
				if events:
					for event in events:
						if event.type == EV_REL:
							if event.code == REL_Y:
								self.y[id] = event.value * 0.67
							elif event.code == REL_X:
								self.x[id] = event.value
							elif event.code == REL_WHEEL:
								self.wheel[id] -= event.value
						elif event.type == EV_KEY:
							if event.code >= BTN_LEFT and event.code <= BTN_MIDDLE:
								self.state[id][event.code - BTN_LEFT] = event.value
			except:
				continue

	def open(self, device):
		if USE_EVDEV:
			return evdev.InputDevice(device)
		else:
			return os.open(device, os.O_RDONLY | os.O_NONBLOCK)

	def close(self, device):
		if USE_EVDEV:
			device.close()
		else:
			os.close(device)


	def edit(self, devices):
		newdevices = {}
		#newpaths = []
		for path in self.devices:
			device = self.devices[path]
			if path in devices:
				newdevices[path] = device
			else:
				self.close(device)
		self.devices = newdevices

		for path in devices:
			if path not in self.devices:
				self.devices[path] = self.open(path)
				#newpaths.append(path)
		self.devicelist = list(self.devices.values())

		#cache
		self.devicelen = len(self.devicelist)
		self.devicerange = range(self.devicelen)
		nir = [0 for i in self.devicerange]

		resize_array(self.y, self.devicelen)
		resize_array(self.x, self.devicelen)
		resize_array(self.wheel, self.devicelen)
		resize_array(self.state, self.devicelen, [0, 0, 0])


	def start(self):

		if USE_EVDEV:
			import evdev
			self.readevent = self.readevent_evdev
		else:
			self.readevent = self.readevent_os

		self.devicelen = len(self.devicelist)

		#cache
		self.devicerange = range(self.devicelen)
		nir = [0 for i in self.devicerange]

		self.y, self.x = nir[:], nir[:]
		self.wheel = nir[:]
		self.state = [[0, 0, 0] for i in self.devicerange]


