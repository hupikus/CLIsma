from integration.loghandler import Loghandler
from InputSquad.device import Device

import os

STATUS_BYTE = 0x80

NOTE_PLAY = 0x90
NOTE_RELEASE = 0x80

def msg_len(status):
    if 0x80 <= status <= 0xEF:
        return 3
    elif 0xF0 <= status <= 0xF7:
        return 0
    elif 0xF8 <= status <= 0xFF:
        return 1
    return 0

class Midi(Device):

	def readevent(self):
		disconnected = []
		for path in self.devices:
			device = self.devices[path]
			try:
				#event = device.read(1)
				event = os.read(device, 1) #FINALY, NON BLOCKING READ
				if not event:
					continue
				b = event[0]
				if b & STATUS_BYTE == 0: # doesnt have a status byte
					self.buffer.append(b)
				else:
					self.buffer = [b]
					#if msg_len(b) == 1:



				if len(self.buffer) == 3: #standard midi event
					data, note, pressure = self.buffer
					channel = data & 0x0F
					msg_type = data & 0xF0

					#Loghandler.Log(note)

					if msg_type == NOTE_PLAY:
						self.controller.keyPress(note, pressure)
					if msg_type == NOTE_RELEASE or pressure == 0:
						self.controller.keyRelease(note)

					self.buffer = []
			except OSError as ex:
				if ex.errno == 19: # device disconnected
					disconnected.append(path)
					Loghandler.Log("Midi keyboard disconnected")
					continue
			except:
				continue

		for path in disconnected:
			self.devicelist.remove(self.devices[path])
			del self.devices[path]

	def start(self):
		self.controller = self.controller.midi
		self.buffer = []

