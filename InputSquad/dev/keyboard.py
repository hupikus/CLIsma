from integration.loghandler import Loghandler
from InputSquad.dev.device import Device

import struct
import os

EV_STRUCT = "llHHi"
EV_SIZE = struct.calcsize(EV_STRUCT)
EV_COUNT = 64


class Keyboard(Device):

	def readevent(self):
		for path in self.devices:
			device = self.devices[path]
			try:
				events = os.read(device, EV_SIZE * EV_COUNT)
				if not events:
					continue

				EV_ACTUAL_SIZE = len(events)

				for event in range(0, EV_ACTUAL_SIZE, EV_SIZE):
					_time, _time, EV_TYPE, EV_CODE, EV_VAL = struct.unpack(EV_STRUCT, events[event : event + EV_SIZE])

					if EV_TYPE == EV_KEY:
						if EV_VAL == 0:
							self.controller.keyRelease(EV_CODE)
						elif EV_VAL == 1:
							self.controller.keyPress(EV_CODE)
			except:
				continue

	def start(self):
		self.controller = self.controller.keyboard

